"""
Enhanced ML Training Pipeline with Transaction Number Features
HIGH PRECISION UPI Fraud Detection
"""

import sys
import os
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Train enhanced fraud detection model with transaction number validation
    """
    
    logger.info("=" * 80)
    logger.info("🚀 ENHANCED UPI FRAUD DETECTION MODEL TRAINING")
    logger.info("=" * 80)
    
    # Load enhanced dataset
    data_path = Path(__file__).parent / "dataset" / "transactions_enhanced.csv"
    
    if not data_path.exists():
        logger.error(f"Dataset not found: {data_path}")
        return
    
    df = pd.read_csv(data_path)
    logger.info(f"✅ Loaded {len(df)} transactions")
    logger.info(f"📊 Fraud cases: {df['label'].sum()} ({df['label'].sum()/len(df)*100:.1f}%)")
    logger.info(f"📊 Legit cases: {(~df['label'].astype(bool)).sum()} ({(~df['label'].astype(bool)).sum()/len(df)*100:.1f}%)")
    
    # Feature extraction with HIGH PRECISION transaction number analysis
    logger.info("\n🔍 Extracting features with transaction number validation...")
    
    from app.utils.preprocessor import extract_features
    
    def extract_all_features(row):
        features = extract_features(
            amount=row['amount'],
            time=row['time'],
            receiver=row['receiver'],
            account=row['account'],
            transaction_number=row.get('transaction_number'),
            reference_number=row.get('reference_number')
        )
        return pd.Series(features)
    
    feature_df = df.apply(extract_all_features, axis=1)
    
    logger.info(f"✅ Extracted {len(feature_df.columns)} features")
    logger.info(f"📋 Feature list: {list(feature_df.columns)}")
    
    # Prepare training data
    X = feature_df.values
    y = df['label'].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"\n📦 Training samples: {len(X_train)}")
    logger.info(f"📦 Test samples: {len(X_test)}")
    
    # Train Gradient Boosting Model
    logger.info("\n🎯 Training Gradient Boosting Classifier...")
    
    gb_model = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        min_samples_split=5,
        min_samples_leaf=2,
        subsample=0.8
    )
    
    gb_model.fit(X_train, y_train)
    
    # Evaluate
    logger.info("\n" + "=" * 80)
    logger.info("📈 MODEL EVALUATION")
    logger.info("=" * 80)
    
    y_pred_train = gb_model.predict(X_train)
    y_pred_test = gb_model.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    
    logger.info(f"\n✅ Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    logger.info(f"✅ Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    logger.info("\n📊 Test Set Classification Report:")
    print(classification_report(y_test, y_pred_test, target_names=['Legit', 'Fraud']))
    
    logger.info("\n📊 Test Set Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred_test)
    print(cm)
    print(f"\nTrue Negatives: {cm[0][0]}, False Positives: {cm[0][1]}")
    print(f"False Negatives: {cm[1][0]}, True Positives: {cm[1][1]}")
    
    # Feature importance
    logger.info("\n🔍 TOP 10 MOST IMPORTANT FEATURES:")
    feature_importance = pd.DataFrame({
        'feature': feature_df.columns,
        'importance': gb_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(10).iterrows():
        logger.info(f"  {row['feature']}: {row['importance']:.4f}")
    
    # Save model
    model_path = Path(__file__).parent.parent / "backend" / "app" / "models" / "fraud_model.pkl"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save model with feature names
    model_data = {
        'model': gb_model,
        'feature_names': list(feature_df.columns),
        'version': '2.0-enhanced-txn-validation'
    }
    
    joblib.dump(model_data, model_path)
    logger.info(f"\n💾 Model saved to: {model_path}")
    
    logger.info("\n" + "=" * 80)
    logger.info("🎉 MODEL TRAINING COMPLETED SUCCESSFULLY!")
    logger.info("=" * 80)
    
    # Test with some examples
    logger.info("\n🧪 TESTING WITH EXAMPLES:")
    logger.info("=" * 80)
    
    # Test case 1: Legit transaction
    test_legit = extract_features(
        amount=1500,
        time="14:30",
        receiver="shop@upi",
        account="user@paytm",
        transaction_number="UPI439287AF1234",
        reference_number="REF987654321"
    )
    pred_legit = gb_model.predict([list(test_legit.values())])[0]
    prob_legit = gb_model.predict_proba([list(test_legit.values())])[0]
    logger.info(f"✅ Legit transaction: Predicted={pred_legit} (Fraud prob: {prob_legit[1]:.3f})")
    
    # Test case 2: Fake transaction number
    test_fraud = extract_features(
        amount=25000,
        time="02:15",
        receiver="unknown@upi",
        account="user@paytm",
        transaction_number="TEST123456",
        reference_number="TEST999"
    )
    pred_fraud = gb_model.predict([list(test_fraud.values())])[0]
    prob_fraud = gb_model.predict_proba([list(test_fraud.values())])[0]
    logger.info(f"🚨 Fraud transaction (TEST pattern): Predicted={pred_fraud} (Fraud prob: {prob_fraud[1]:.3f})")
    
    # Test case 3: Sequential pattern
    test_fraud2 = extract_features(
        amount=15000,
        time="23:45",
        receiver="urgent@upi",
        account="user@paytm",
        transaction_number="123456789",
        reference_number="REF999888777"
    )
    pred_fraud2 = gb_model.predict([list(test_fraud2.values())])[0]
    prob_fraud2 = gb_model.predict_proba([list(test_fraud2.values())])[0]
    logger.info(f"🚨 Fraud transaction (Sequential): Predicted={pred_fraud2} (Fraud prob: {prob_fraud2[1]:.3f})")
    
    # Test case 4: All same digits
    test_fraud3 = extract_features(
        amount=50000,
        time="03:20",
        receiver="verify@upi",
        account="user@paytm",
        transaction_number="111111111",
        reference_number="REF222222222"
    )
    pred_fraud3 = gb_model.predict([list(test_fraud3.values())])[0]
    prob_fraud3 = gb_model.predict_proba([list(test_fraud3.values())])[0]
    logger.info(f"🚨 Fraud transaction (All same): Predicted={pred_fraud3} (Fraud prob: {prob_fraud3[1]:.3f})")
    
    logger.info("\n" + "=" * 80)

if __name__ == "__main__":
    main()

