"""
Response generator for user question response generation

"""

import random
from re import X
import pandas as pd

class ResponseGenerator:
    def __init__(self):
        self.templates = self.parse_response_bank()

    def parse_response_bank(self, response_bank_path='config/response_bank.md'):
        # Read the response bank file
        with open(response_bank_path, 'r') as file:
            content = file.read()
        
        # Initialize templates dictionary and current intent
        templates = {}
        current_intent = None

        # Iterate through each line
        for line in content.split('\n'):
            # Handle section headers
            if line.startswith('# '):
                current_intent = line[2:].strip().lower().replace(' ', '_')
                templates[current_intent] = []
        
            # Handle template lines
            elif line.strip().startswith('-') and current_intent:
                template = line.strip()[1:].strip()
                templates[current_intent].append(template)
        
        return templates

    def generate_response(self, intent, result):
        # Special handling for tree recommendations
        if intent == 'tree_recommendations':
            lookup_value = result['lookup_value']
            regular_tree = result['regular_tree']
            fruit_tree = result['fruit_tree']

            if regular_tree and fruit_tree:
                return f"The best trees to grow at level {lookup_value} Farming are {regular_tree} and {fruit_tree}."
            elif regular_tree:
                return f"The best tree to grow at level {lookup_value} Farming is {regular_tree}."
            elif fruit_tree:
                return f"The best tree to grow at level {lookup_value} Farming is {fruit_tree}."
            else:
                return f"You can't grow any trees at level {lookup_value} Farming. Try planting something else instead!"

        # Unpack result dictionary for other intents
        lookup_value = result['lookup_value']
        answer_value = result['answer_value']

        # Special handling for quest requirement queries
        if intent == 'quest_requirements':
            recommended = result.get('recommended')
            # No requirement, no recommendation
            if pd.isna(answer_value) and pd.isna(recommended):
                return f"The {str(lookup_value)} patch has no quest requirements."
            # No requirement but has a recommendation
            elif pd.isna(answer_value) and not pd.isna(recommended):
                return f"The {str(lookup_value)} patch has no quest requirements, but {str(recommended)} is recommended."
            # Requirement and recommendation
            elif not pd.isna(answer_value) and not pd.isna(recommended):
                return f"Using the {str(lookup_value)} patch requires {str(answer_value)}, and {str(recommended)} is also recommended."
            # Requirement but no recommendation
            else:
                return f"Using the {str(lookup_value)} patch requires {str(answer_value)}."

        # Special handling for transportation queries
        if intent == 'transportation':
            methods = [method.strip() for method in str(answer_value).split(',')]
            location_detailed = result.get('location_detailed')
            intro = f"The {str(lookup_value)} patch can be found {str(location_detailed)}.\n"
            # Single method (simple sentence)
            if len(methods) == 1:
                response = f"{intro}To get there, use a {methods[0]}."
            # Multiple methods (bullet points)
            else:
                response = f"{intro}To get there, you have a few options:\n"
                for method in methods:
                    response += f"• {method}\n"
                response = response.rstrip()
            
            return response

        # Regular template handling
        template = random.choice(self.templates[intent])
        response = template.replace('{lookup_value}', str(lookup_value))
        response = response.replace('{answer_value}', str(answer_value))

        return response


if __name__ == '__main__':
    generator = ResponseGenerator()
    question = "What level do I need for magic trees?"
    intent = "level_requirements"
    result = {'lookup_value': 'magic', 'answer_value': '75'}
    response = generator.generate_response(intent, result)
    print(f'Question: {question}')
    print(f'Intent: {intent}')
    print(f'Lookup: {result["lookup_value"]}')
    print(f'Answer: {result["answer_value"]}')
    print(f'Response: {response}')