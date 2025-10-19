"""
Intent classifier for user question categorization

"""

import joblib


class IntentClassifier:
    def __init__(self, model_dir='models'):
        self.vectorizer = joblib.load(f'{model_dir}/vectoriser.pkl')
        self.classifier = joblib.load(f'{model_dir}/classifier.pkl')
    
    def predict(self, question):
        text_tfidf = self.vectorizer.transform([question])
        intent = self.classifier.predict(text_tfidf)[0]
        confidence = max(self.classifier.predict_proba(text_tfidf)[0])
        return intent, confidence


if __name__ == '__main__':
    classifier = IntentClassifier()
    question = "What level do I need for magic trees?"
    intent, confidence = classifier.predict(question)
    print(f'Question: {question}')
    print(f'Intent: {intent}')
    print(f'Confidence: {confidence}')