"""
Answer retriever for user question response generation

"""

import pandas as pd
import re
from source.intent_classifier import IntentClassifier
from config.intent_mapping import get_intent_mapping


class AnswerRetriever:
    def __init__(self, trees_csv_path='data/trees_df.csv', patches_csv_path='data/patches_df.csv'):
        self.trees_df = pd.read_csv(trees_csv_path)
        self.patches_df = pd.read_csv(patches_csv_path)
        self.classifier = IntentClassifier()
        self.intent_mapping = get_intent_mapping(self.trees_df, self.patches_df)
    
    def get_answer(self, question):
        # Get question intent from intent classifier
        intent_classifier_result = self.classifier.predict(question)
        question_intent = intent_classifier_result['intent']

        # Get the lookup column and create a list of values
        lookup_column = self.intent_mapping[question_intent]['column_to_extract']
        lookup_column_values = list(set(lookup_column.astype(str).tolist()))    

        # Find matching lookup value using word boundaries to avoid partial matches    
        lookup_value = [value for value in lookup_column_values if re.search(r'\b' + re.escape(value.lower()) + r'\b', question.lower())]

        # Determine which dataframe to search based on the lookup column
        if lookup_column.name in self.trees_df.columns:
            df_to_search = self.trees_df
        else:
            df_to_search = self.patches_df

        # Find the row where the value in the lookup column matches the lookup value
        matching_row = df_to_search[df_to_search[lookup_column.name].astype(str).str.lower() == lookup_value[0].lower()]

        # Get the answer column
        answer_column = self.intent_mapping[question_intent]['column_to_return']

        # Get the value from the answer column
        answer_value = matching_row.iloc[0][answer_column.name]
        
        return answer_value, question_intent, lookup_value


if __name__ == '__main__':
    retriever = AnswerRetriever()
    answer, intent, lookup = retriever.get_answer("What level do I need for magic trees?")
    print(f"Intent: {intent}")
    print(f"Lookup: {lookup}")
    print(f"Answer: {answer}")