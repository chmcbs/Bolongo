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
        # Get the lookup column and create a list of values
        lookup_column = self.intent_mapping[intent]['lookup_column']
        lookup_column_values = list(set(lookup_column.astype(str).tolist()))

        # Find matching lookup value using word boundaries to avoid partial matches    
        lookup_value = next((value for value in lookup_column_values 
                           if re.search(rf'\b{re.escape(value.lower())}\b', question.lower())), None)

        # Determine which dataframe to search based on the lookup column
        if lookup_column.name in self.trees_df.columns:
            df_to_search = self.trees_df
        else:
            df_to_search = self.patches_df

        # Special handling for tree recommendations
        if intent == 'tree_recommendations':
            # Extract numbers from the question
            numbers = re.findall(r'\b\d+\b', question)
            # Set the lookup value to the first number found
            lookup_value = numbers[0]
            # Find the row with the highest level requirement less than or equal to the lookup value
            lookup_float = float(lookup_value)
            valid_rows = df_to_search[df_to_search[lookup_column.name] <= lookup_float]
            matching_row_index = valid_rows[lookup_column.name].idxmax()
            matching_row = valid_rows.loc[[matching_row_index]]
        else:
            # Find the row where the value in the lookup column matches the lookup value
            matching_row = df_to_search[df_to_search[lookup_column.name].astype(str).str.lower() == lookup_value.lower()]

        # Get the answer column
        answer_column = self.intent_mapping[intent]['answer_column']

        # Get the value from the answer column
        answer_value = matching_row.iloc[0][answer_column.name]
        
        return lookup_value, answer_value


if __name__ == '__main__':
    retriever = AnswerRetriever()
    question = "What level do I need for magic trees?"
    intent = "level_requirements"
    lookup_value, answer_value = retriever.get_answer(question, intent)
    print(f'Question: {question}')
    print(f'Lookup: {lookup_value}')
    print(f'Intent: {intent}')
    print(f'Answer: {answer_value}')