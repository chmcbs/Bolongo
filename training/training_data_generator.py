"""
Template-based training data generator for intent classification

Note: This module was generated with AI assistance, but the rest of the project was written by hand unless otherwise specified
"""

import re
import random
import pandas as pd
from typing import List, Dict, Tuple


class TrainingDataGenerator:
    def __init__(self, question_bank_path: str, 
                 trees_csv_path: str, 
                 patches_csv_path: str):
        self.question_bank_path = question_bank_path
        self.trees_csv_path = trees_csv_path
        self.patches_csv_path = patches_csv_path
        self.intents = {}
        self.trees_df = None
        self.patches_df = None
        
    def load_data(self):
        self.trees_df = pd.read_csv(self.trees_csv_path)
        self.patches_df = pd.read_csv(self.patches_csv_path)
        
    def parse_question_bank(self) -> Dict[str, Dict[str, any]]:
        with open(self.question_bank_path, 'r') as f:
            content = f.read()
        sections = re.split(r'^# ', content, flags=re.MULTILINE)[1:]
        intents = {}
        
        for section in sections:
            lines = section.strip().split('\n')
            intent_name = lines[0].strip().lower().replace(' ', '_')
            fill_with = None
            templates = []

            if len(lines) > 1 and lines[1].startswith('Fill with:'):
                fill_with = lines[1].replace('Fill with:', '').strip()

            for line in lines[2:]:
                if line.strip().startswith('- '):
                    templates.append(line.strip()[2:])

            if templates:
                intents[intent_name] = {
                    'fill_with': fill_with,
                    'templates': templates
                }
        
        self.intents = intents
        return intents
    
    def get_fill_values(self, fill_instruction: str) -> List[str]:
        if 'level numbers' in fill_instruction.lower():
            return [str(level) for level in sorted(self.trees_df['level_requirement'].unique())]

        elif 'tree names' in fill_instruction.lower():
            return self.trees_df['tree_name'].tolist()

        elif 'patch names' in fill_instruction.lower() or 'location names' in fill_instruction.lower():
            return self.patches_df['location_simple'].tolist()

        elif 'static values' in fill_instruction.lower():
            match = re.search(r'\[(.*?)\]', fill_instruction)

            if match:
                values_str = match.group(1)
                return [v.strip().strip('"') for v in values_str.split(',')]
        
        return []
    
    def generate_training_data(self, samples_per_intent: int = None) -> Tuple[List[str], List[str]]:
        texts = []
        labels = []

        for intent, config in self.intents.items():
            intent_texts = []
            
            fill_instruction = config['fill_with']
            templates = config['templates']

            if intent == 'list_regular_patches' or intent == 'list_fruit_patches':
                intent_texts = templates.copy()
                
            else:
                fill_values = self.get_fill_values(fill_instruction)
        
                for template in templates:
                    for value in fill_values:
                        filled = template.replace('___', value)
                        intent_texts.append(filled)
            
            intent_texts = list(set(intent_texts))
            
            if samples_per_intent and len(intent_texts) > samples_per_intent:
                intent_texts = random.sample(intent_texts, samples_per_intent)
            
            texts.extend(intent_texts)
            labels.extend([intent] * len(intent_texts))

        return texts, labels
    
    def generate_dataset(self, samples_per_intent: int = None) -> pd.DataFrame:
        self.load_data()
        self.parse_question_bank()
        
        texts, labels = self.generate_training_data(samples_per_intent)
        
        df = pd.DataFrame({
            'text': texts,
            'intent': labels
        })
        
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return df


if __name__ == '__main__':
    generator = TrainingDataGenerator(
        question_bank_path='training/question_bank.md',
        trees_csv_path='data/trees_df.csv',
        patches_csv_path='data/patches_df.csv'
    )
    df = generator.generate_dataset()
    print(f"Generated {len(df)} training examples")
    print(f"\n{df['intent'].value_counts()}")