#!/usr/bin/env python3
"""
Complete ML Pipeline: Train and deploy fraud detection model
"""

import os
import sys
import pandas as pd
import numpy as np
from data_preparation import load_and_prepare_data, scale_features
from model_pipeline import (
    train_gradient_boosting,
    train_random_forest,
    train_logistic_regression,
    evaluate_model,
    cross_validate_model,
    save_model
)

def main():
    print("="*70)
    print("🚀 UPI FRAUD DETECTION - ML TRAINING PIPELINE")
    print("="*70)
    
    # 1. Load and prepare data
    print("\n📁 Step 1: Loading and preparing data...")
    X_train, X_test, y_train, y_test, feature_names = load_and_prepare_data()
    
    # 2. Feature scaling (optional - tree-based models don't require it)
    # X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    
    # 3. Train multiple models
    models = {}
    
    # Gradient Boosting
    gb_model = train_gradient_boosting(X_train, y_train)
    models['Gradient Boosting'] = evaluate_model(gb_model, X_test, y_test, "Gradient Boosting")
    
    # Random Forest
    rf_model = train_random_forest(X_train, y_train)
    models['Random Forest'] = evaluate_model(rf_model, X_test, y_test, "Random Forest")
    
    # Logistic Regression (Baseline)
    lr_model = train_logistic_regression(X_train, y_train)
    models['Logistic Regression'] = evaluate_model(lr_model, X_test, y_test, "Logistic Regression")
    
    # 4. Select best model
    print("\n" + "="*70)
    print("🏆 MODEL COMPARISON")
    print("="*70)
    
    for name, results in models.items():
        print(f"\n{name}:")
        print(f"  Accuracy: {results['accuracy']:.4f} | F1: {results['f1']:.4f} | Recall: {results['recall']:.4f}")
    
    # Choose model with best F1 score (balance of precision and recall)
    best_model_name = max(models.keys(), key=lambda k: models[k]['f1'])
    best_model = models[best_model_name]['model']
    
    print(f"\n✨ Best Model: {best_model_name}")
    print(f"   F1 Score: {models[best_model_name]['f1']:.4f}")
    
    # 5. Cross-validation on best model
    cross_validate_model(best_model, pd.concat([X_train, X_test]), pd.concat([y_train, y_test]))
    
    # 6. Feature importance (if available)
    if hasattr(best_model, 'feature_importances_'):
        print("\n📊 Feature Importance:")
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': best_model.feature_importances_
        }).sort_values('Importance', ascending=False)
        print(importance_df.to_string(index=False))
    
    # 7. Save best model
    model_path = os.path.join('..', 'backend', 'app', 'models', 'fraud_model.pkl')
    save_model(best_model, model_path)
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    print(f"🎯 Model ready for deployment")
    print(f"📍 Location: {model_path}")
    print(f"🔮 Best Model: {best_model_name}")
    print(f"📈 Test Accuracy: {models[best_model_name]['accuracy']:.2%}")
    print(f"⚖️  F1 Score: {models[best_model_name]['f1']:.4f}")
    
    return best_model

if __name__ == "__main__":
    try:
        model = main()
        print("\n🎉 Success! Model is ready to use.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

