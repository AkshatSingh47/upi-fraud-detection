from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score
import numpy as np
import pickle
import os

def train_gradient_boosting(X_train, y_train):
    """
    Train Gradient Boosting Classifier
    """
    print("\n🎯 Training Gradient Boosting Classifier...")
    
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42,
        min_samples_split=5,
        min_samples_leaf=2
    )
    
    model.fit(X_train, y_train)
    
    return model

def train_random_forest(X_train, y_train):
    """
    Train Random Forest Classifier
    """
    print("\n🌲 Training Random Forest Classifier...")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    return model

def train_logistic_regression(X_train, y_train):
    """
    Train Logistic Regression (baseline)
    """
    print("\n📊 Training Logistic Regression...")
    
    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    return model

def evaluate_model(model, X_test, y_test, model_name="Model"):
    """
    Evaluate model performance
    """
    print(f"\n{'='*60}")
    print(f"📈 Evaluating {model_name}")
    print('='*60)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"\n✅ Accuracy:  {accuracy:.4f}")
    print(f"🎯 Precision: {precision:.4f}")
    print(f"🔍 Recall:    {recall:.4f}")
    print(f"⚖️  F1 Score:  {f1:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n📊 Confusion Matrix:")
    print(cm)
    
    # Classification Report
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legit', 'Fraud']))
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'model': model
    }

def cross_validate_model(model, X, y, cv=5):
    """
    Perform cross-validation
    """
    print(f"\n🔄 Performing {cv}-Fold Cross Validation...")
    
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    
    print(f"Cross-validation scores: {scores}")
    print(f"Mean CV Accuracy: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
    
    return scores

def save_model(model, filepath='../backend/app/models/fraud_model.pkl'):
    """
    Save trained model to file
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\n💾 Model saved to: {filepath}")

def load_model(filepath='../backend/app/models/fraud_model.pkl'):
    """
    Load model from file
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model not found at {filepath}")
    
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    
    print(f"✅ Model loaded from: {filepath}")
    return model

