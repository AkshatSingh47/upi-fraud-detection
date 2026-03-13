import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def load_and_prepare_data(csv_path='dataset/transactions.csv'):
    """
    Load and prepare training data
    """
    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Fraud cases: {df['label'].sum()}")
    print(f"Legit cases: {(df['label'] == 0).sum()}")
    
    # Separate features and target
    X = df.drop('label', axis=1)
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test, X.columns.tolist()

def scale_features(X_train, X_test):
    """
    Scale features using StandardScaler
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, scaler

if __name__ == "__main__":
    # Test data preparation
    X_train, X_test, y_train, y_test, feature_names = load_and_prepare_data()
    print("\nFeatures:", feature_names)
    print("\nData preparation successful!")

