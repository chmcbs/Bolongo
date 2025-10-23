"""
Response generator for user question response generation

"""

import random


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

    def generate_response(self, intent, lookup_value, answer_value):
        template = random.choice(self.templates[intent])
        response = template.replace('{lookup_value}', str(lookup_value).title())

        # Special handling for tree recommendations
        if intent == 'tree_recommendations':
            response = response.replace('{answer_value}', str(answer_value).title())
        else:
            response = response.replace('{answer_value}', str(answer_value))

        return response


if __name__ == '__main__':
    generator = ResponseGenerator()
    question = "What level do I need for magic trees?"
    intent = "level_requirements"
    lookup_value = "magic"
    answer_value = "75"
    response = generator.generate_response(intent, lookup_value, answer_value)
    print(f'Question: {question}')
    print(f'Lookup: {lookup_value}')
    print(f'Intent: {intent}')
    print(f'Answer: {answer_value}')
    print(f'Response: {response}')