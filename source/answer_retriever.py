"""
Answer retriever for user question response generation

"""

import pandas as pd
import re
from config.intent_mapping import get_intent_mapping


class AnswerRetriever:
    def __init__(self, trees_csv_path='data/trees_df.csv', patches_csv_path='data/patches_df.csv'):
        self.trees_df = pd.read_csv(trees_csv_path)
        self.patches_df = pd.read_csv(patches_csv_path)
        self.intent_mapping = get_intent_mapping(self.trees_df, self.patches_df)
    
    def get_answer(self, question, intent):
        # Get the lookup value from the question
        lookup_column = self.intent_mapping[intent]['lookup_column']
        lookup_column_values = list(set(lookup_column.astype(str).tolist()))  
        lookup_value = next((value for value in lookup_column_values 
                           if re.search(rf'\b{re.escape(value.lower())}\b', question.lower())), None)
        # Get the answer column from the intent mapping
        answer_column = self.intent_mapping[intent]['answer_column']

        # Determine which dataframe to search based on the lookup column
        if lookup_column.name in self.trees_df.columns:
            df_to_search = self.trees_df
        else:
            df_to_search = self.patches_df

        # Special handling for tree recommendations
        if intent == 'tree_recommendations':
            # Extract numbers from the question
            numbers = re.findall(r'\b\d+\b', question)
            lookup_value = numbers[0]
            lookup_float = float(lookup_value)

            # Split the df_to_search into regular trees and fruit trees
            regular_trees = df_to_search[df_to_search['is_fruit_tree'] == False]
            fruit_trees = df_to_search[df_to_search['is_fruit_tree'] == True]

            # Find the best regular tree for the lookup value
            valid_rows_regular = regular_trees[regular_trees[lookup_column.name] <= lookup_float]
            if len(valid_rows_regular) > 0:
                best_tree_index_regular = valid_rows_regular[lookup_column.name].idxmax()
                best_tree_regular = valid_rows_regular.loc[best_tree_index_regular][answer_column.name]
            else:
                best_tree_regular = None

            # Find the best fruit tree for the lookup value
            valid_rows_fruit = fruit_trees[fruit_trees[lookup_column.name] <= lookup_float]
            if len(valid_rows_fruit) > 0:
                best_tree_index_fruit = valid_rows_fruit[lookup_column.name].idxmax()
                best_tree_fruit = valid_rows_fruit.loc[best_tree_index_fruit][answer_column.name]
            else:
                best_tree_fruit = None

            # Create result dictionary with both types of trees
            result = {
                'lookup_value': lookup_value,
                'regular_tree': best_tree_regular,
                'fruit_tree': best_tree_fruit
            }

            return result

        else:
            # Find the row where the value in the lookup column matches the lookup value
            matching_row = df_to_search[df_to_search[lookup_column.name].astype(str).str.lower() == lookup_value.lower()]
        
        # Get the answer value from the matching row
        answer_value = matching_row.iloc[0][answer_column.name]

        # Special handling for growth time
        if intent == 'growth_time':
            minutes = int(answer_value)
            hours = minutes / 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                answer_value = f'{int(hours)} hours'
            else:
                answer_value = f'{int(hours)} hours and {int(remaining_minutes)} minutes'

        # Build result dictionary
        result = {
            'lookup_value': lookup_value,
            'answer_value': answer_value
        }
        
        # Special handling for transportation queries
        if intent == 'transportation':
            result['location_detailed'] = matching_row.iloc[0]['location_detailed']
        
        # Special handling for quest requirement queries
        if intent == 'quest_requirements':
            result['recommended'] = matching_row.iloc[0]['patch_recommended']

        return result


if __name__ == '__main__':
    retriever = AnswerRetriever()
    question = "What level do I need for magic trees?"
    intent = "level_requirements"
    result = retriever.get_answer(question, intent)
    print(f'Question: {question}')
    print(f'Intent: {intent}')
    print(f'Lookup: {result["lookup_value"]}')
    print(f'Answer: {result["answer_value"]}')