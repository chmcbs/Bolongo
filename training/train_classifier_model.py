"""
Train Intent Classifier Model

Generates training data, trains a logistic regression classifier,
evaluates performance, and saves the model artifacts.
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from training_data_generator import TrainingDataGenerator


def main():
    # Generate Training Data
    generator = TrainingDataGenerator(
        question_bank_path='training/question_bank.md', 
        trees_csv_path='data/trees_df.csv', 
        patches_csv_path='data/patches_df.csv'
    )
    df = generator.generate_dataset()
    
    # Split Data
    X = df['text']  # Questions
    y = df['intent']  # Intent
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Vectorisation (TF-IDF)
    vectoriser = TfidfVectorizer(
        max_features=500,  # Keep top 500 words
        ngram_range=(1, 2),  # Use single words and word pairs
        lowercase=True
    )
    X_train_tfidf = vectoriser.fit_transform(X_train)
    X_test_tfidf = vectoriser.transform(X_test)
    
    # Train Model
    classifier = LogisticRegression(
        max_iter=1000,
        random_state=42
    )
    classifier.fit(X_train_tfidf, y_train)
    
    # Evaluate Model Performance
    y_pred = classifier.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2%}")
    print(classification_report(y_test, y_pred))

    # Save Model
    joblib.dump(vectoriser, 'models/vectoriser.pkl')
    joblib.dump(classifier, 'models/classifier.pkl')


if __name__ == "__main__":
    main()