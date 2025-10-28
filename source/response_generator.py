"""
Response generator for user question response generation

"""

import random
import pandas as pd

class ResponseGenerator:
    def __init__(self):
        self.templates = self.parse_response_bank()

    def parse_response_bank(self, response_bank_path='config/response_bank.md'):
        with open(response_bank_path, 'r') as file:
            content = file.read()
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
        lookup_value = str(result['lookup_value'])
        answer_value = result['answer_value']
        is_fruit_patch = result.get('is_fruit_patch', False)

        # Create patch name for patch-based queries
        if intent in ['transportation', 'patch_requirements']:
            patch_name = f'{lookup_value} fruit tree patch' if is_fruit_patch else f'{lookup_value} patch'
        
        # Special handling for patch requirement queries
        if intent == 'patch_requirements':
            recommended = result.get('recommended')
            recommended = None if pd.isna(recommended) else str(recommended)
            answer_value = None if pd.isna(answer_value) else str(answer_value)

            if answer_value is None and recommended is None:
                return f"The {patch_name} has no requirements."
            elif answer_value is None and recommended is not None:
                return f"The {patch_name} has no requirements, but {recommended} is recommended."
            elif answer_value is not None and recommended is not None:
                return f"Using the {patch_name} requires {answer_value}, and {recommended} is also recommended."
            else:
                return f"Using the {patch_name} requires {answer_value}."

        # Special handling for transportation queries
        if intent == 'transportation':
            location_detailed = result.get('location_detailed')
            location_detailed = None if pd.isna(location_detailed) else str(location_detailed)
            methods = [method.strip() for method in str(answer_value).split(',')]
            intro = f"The {patch_name} can be found {location_detailed}.\n"

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
        response = template.replace('{lookup_value}', lookup_value)
        response = response.replace('{answer_value}', str(answer_value))

        return response


if __name__ == '__main__':
    generator = ResponseGenerator()
    question = "What level do I need for magic trees?"
    intent = "tree_requirements"
    result = {'lookup_value': 'magic', 'answer_value': '75'}
    response = generator.generate_response(intent, result)
    print(f'Question: {question}')
    print(f'Intent: {intent}')
    print(f'Lookup: {result["lookup_value"]}')
    print(f'Answer: {result["answer_value"]}')
    print(f'Response: {response}')