"""
Main orchestrator for the complete question-answering pipeline

"""

from source.intent_classifier import IntentClassifier
from source.answer_retriever import AnswerRetriever
from source.response_generator import ResponseGenerator
import random

class Bolongo:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.retriever = AnswerRetriever()
        self.generator = ResponseGenerator()
        self.confidence_threshold = 0.35 # Some training questions had confidence below 0.45
    
    def ask(self, question):

        # Classify intent
        intent, confidence = self.classifier.predict(question)
        
        # Check confidence threshold
        if confidence < self.confidence_threshold:
            return random.choice([
                "That one's gone right over my hat.",
                "You've lost me there, friend.\nUnless it's got roots or leaves, I'm afraid I can't help you.",
                "I haven't the foggiest what you're on about.",
                "Why is it that every time I take a break from pruning, someone asks me riddles?",
                "I think you might have had one too many Blurberry specials."
            ])
        
        # Retrieve answer data
        result = self.retriever.get_answer(question, intent)
        
        # Check if retriever returned an error message
        if isinstance(result, str):
            return result
        
        # Generate response
        response = self.generator.generate_response(intent, result)
        
        return response


if __name__ == '__main__':
    bolongo = Bolongo()
    test_questions = [
        "What level do I need for magic trees?",
        "How many fruit tree patches are there?",
        "What's the weather in Lumbridge?", # Low confidence
        "What level do I need for trees?", # Missing lookup value
        "How do I get to the Falador patch?"
        ]
    for question in test_questions:
        print(f"Q: {question}")
        print(f"A: {bolongo.ask(question)}")
        print()