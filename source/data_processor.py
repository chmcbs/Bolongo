"""
Data processor for intent classification training data generation.

This module handles:
- Parsing question templates from question_bank.md
- Loading tree and patch data from CSV files
- Generating training examples by filling templates with real data
"""

import re
import random
import pandas as pd
from typing import List, Dict, Tuple
from itertools import product


class DataProcessor:
    """Processes question bank templates and CSV data to generate training examples."""
    
    def __init__(self, question_bank_path: str, trees_csv_path: str, patches_csv_path: str):
        """
        Initialize the data processor.
        
        Args:
            question_bank_path: Path to question_bank.md
            trees_csv_path: Path to trees_df.csv
            patches_csv_path: Path to patches_df.csv
        """
        self.question_bank_path = question_bank_path
        self.trees_csv_path = trees_csv_path
        self.patches_csv_path = patches_csv_path
        
        self.intents = {}
        self.trees_df = None
        self.patches_df = None
        
    def load_data(self):
        """Load CSV data files."""
        self.trees_df = pd.read_csv(self.trees_csv_path)
        self.patches_df = pd.read_csv(self.patches_csv_path)
        
    def parse_question_bank(self) -> Dict[str, List[str]]:
        """
        Parse question bank markdown file to extract templates for each intent.
        
        Returns:
            Dictionary mapping intent names to lists of template strings
        """
        with open(self.question_bank_path, 'r') as f:
            content = f.read()
        
        # Split by intent sections (marked by # headers)
        sections = re.split(r'^# ', content, flags=re.MULTILINE)[1:]  # Skip empty first element
        
        intents = {}
        
        for section in sections:
            lines = section.strip().split('\n')
            intent_name = lines[0].strip().lower().replace(' ', '_')
            
            # Extract templates
            templates = []
            in_templates = False
            
            for line in lines:
                if 'Templates:' in line:
                    in_templates = True
                    continue
                elif line.strip().startswith('Keywords:') or line.strip().startswith('Data'):
                    in_templates = False
                    
                if in_templates and line.strip().startswith('- '):
                    template = line.strip()[2:]  # Remove '- '
                    templates.append(template)
            
            intents[intent_name] = templates
        
        self.intents = intents
        return intents
    
    def expand_template(self, template: str) -> List[str]:
        """
        Expand a template with parenthetical options into multiple variations.
        
        Example:
            "(What / Which) tree" -> ["What tree", "Which tree"]
        
        Args:
            template: Template string with (option1 / option2) syntax
            
        Returns:
            List of expanded template strings
        """
        # Find all parenthetical groups
        pattern = r'\(([^)]+)\)'
        matches = list(re.finditer(pattern, template))
        
        if not matches:
            return [template]
        
        # Extract all option groups
        option_groups = []
        for match in matches:
            options = [opt.strip() for opt in match.group(1).split('/')]
            option_groups.append(options)
        
        # Generate all combinations
        expanded = []
        for combination in product(*option_groups):
            result = template
            # Replace from right to left to maintain positions
            for match, replacement in zip(reversed(matches), reversed(combination)):
                result = result[:match.start()] + replacement + result[match.end():]
            expanded.append(result)
        
        return expanded
    
    def fill_template(self, template: str, intent: str) -> List[str]:
        """
        Fill template placeholders with real data from CSVs.
        
        Args:
            template: Template string with ___ placeholders
            intent: Intent category name
            
        Returns:
            List of filled templates
        """
        filled_templates = []
        
        if intent == 'level_requirement':
            # Fill with tree names and levels
            for _, tree in self.trees_df.iterrows():
                # Templates asking about best tree at level (fill with level numbers)
                if 'level ___' in template:
                    filled = template.replace('___', str(tree['level_requirement']))
                    filled_templates.append(filled)
                # Templates asking about level for a tree (fill with tree names)
                elif '___' in template:
                    filled = template.replace('___', tree['tree_name'])
                    filled_templates.append(filled)
                    
        elif intent == 'payment':
            # Fill with tree names
            for _, tree in self.trees_df.iterrows():
                if '___' in template:
                    filled = template.replace('___', tree['tree_name'])
                    filled_templates.append(filled)
                    
        elif intent == 'growth_time':
            # Fill with tree names
            for _, tree in self.trees_df.iterrows():
                if '___' in template:
                    filled = template.replace('___', tree['tree_name'])
                    filled_templates.append(filled)
                    
        elif intent == 'patches':
            # Fill with patch locations
            for _, patch in self.patches_df.iterrows():
                if '___' in template:
                    filled = template.replace('___', patch['location_simple'])
                    filled_templates.append(filled)
            # Also add "tree" as a generic
            if '___' in template:
                filled = template.replace('___', 'tree')
                filled_templates.append(filled)
                filled = template.replace('___', 'fruit tree')
                filled_templates.append(filled)
                    
        elif intent == 'transportation':
            # Fill with patch locations
            for _, patch in self.patches_df.iterrows():
                if '___' in template:
                    filled = template.replace('___', patch['location_simple'])
                    filled_templates.append(filled)
                    filled = template.replace('___', patch['location_detailed'])
                    filled_templates.append(filled)
        
        return filled_templates
    
    def generate_training_data(self, samples_per_intent: int = None) -> Tuple[List[str], List[str]]:
        """
        Generate training data by expanding templates and filling with CSV data.

        Args:
            samples_per_intent: Optional limit on samples per intent (for balancing)

        Returns:
            Tuple of (texts, labels) lists
        """
        texts = []
        labels = []

        for intent, templates in self.intents.items():
            intent_texts = []

            for template in templates:
                # Expand parenthetical options
                expanded = self.expand_template(template)

                for exp_template in expanded:
                    # Fill with real data
                    filled = self.fill_template(exp_template, intent)

                    if filled:
                        for f in filled:
                            # Add the filled template
                            intent_texts.append(f)
                    else:
                        # Template has no placeholders
                        intent_texts.append(exp_template)

            # Remove duplicates
            intent_texts = list(set(intent_texts))

            # Sample if requested
            if samples_per_intent and len(intent_texts) > samples_per_intent:
                intent_texts = random.sample(intent_texts, samples_per_intent)

            # Add to training data
            texts.extend(intent_texts)
            labels.extend([intent] * len(intent_texts))

        return texts, labels
    
    def generate_dataset(self, samples_per_intent: int = None) -> pd.DataFrame:
        """
        Generate complete training dataset.
        
        Args:
            samples_per_intent: Optional limit on samples per intent
            
        Returns:
            DataFrame with 'text' and 'intent' columns
        """
        self.load_data()
        self.parse_question_bank()
        
        texts, labels = self.generate_training_data(samples_per_intent)
        
        df = pd.DataFrame({
            'text': texts,
            'intent': labels
        })
        
        # Shuffle the dataset
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return df


if __name__ == '__main__':

    processor = DataProcessor(
        question_bank_path='../question_bank.md',
        trees_csv_path='../data/trees_df.csv',
        patches_csv_path='../data/patches_df.csv'
    )
    
    df = processor.generate_dataset()
    
    print(f"Generated {len(df)} training examples")
    print(f"\nIntent distribution:")
    print(df['intent'].value_counts())
    print(f"\nSample examples:")
    for intent in df['intent'].unique():
        print(f"\n{intent.upper()}:")
        samples = df[df['intent'] == intent].head(3)
        for _, row in samples.iterrows():
            print(f"  - {row['text']}")