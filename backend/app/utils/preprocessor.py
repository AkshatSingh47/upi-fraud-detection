import os
import pickle
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'fraud_model.pkl')

def load_model():
    """
    Load the trained fraud detection model
    """
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                return pickle.load(f)
        else:
            logger.warning(f"Model not found at {MODEL_PATH}. Using rule-based fallback.")
            return None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None

# Global model instance
_model = None

def get_model():
    """
    Get or load the model (singleton pattern)
    """
    global _model
    if _model is None:
        _model = load_model()
    return _model

def extract_time_features(time_str: str) -> Dict[str, Any]:
    """
    Extract time-based features
    """
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        hour = time_obj.hour
        minute = time_obj.minute
        
        # Risk indicators
        is_odd_hour = hour < 6 or hour > 22  # Late night/early morning
        is_business_hours = 9 <= hour <= 18
        
        return {
            "hour": hour,
            "minute": minute,
            "is_odd_hour": int(is_odd_hour),
            "is_business_hours": int(is_business_hours),
            "hour_sin": np.sin(2 * np.pi * hour / 24),
            "hour_cos": np.cos(2 * np.pi * hour / 24)
        }
    except Exception as e:
        logger.warning(f"Time parsing error: {e}")
        return {
            "hour": 12,
            "minute": 0,
            "is_odd_hour": 0,
            "is_business_hours": 1,
            "hour_sin": 0,
            "hour_cos": 1
        }

def extract_amount_features(amount: float) -> Dict[str, Any]:
    """
    Extract amount-based features
    """
    return {
        "amount": amount,
        "amount_log": np.log1p(amount),
        "is_round_amount": int(amount % 100 == 0),
        "is_large_amount": int(amount > 10000),
        "is_very_large": int(amount > 50000)
    }

def extract_receiver_features(receiver: str) -> Dict[str, Any]:
    """
    Extract receiver/merchant features
    """
    receiver_lower = receiver.lower()
    
    # Suspicious patterns
    suspicious_keywords = ['unknown', 'test', 'verify', 'confirm', 'urgent']
    has_suspicious = any(keyword in receiver_lower for keyword in suspicious_keywords)
    
    return {
        "receiver_length": len(receiver),
        "has_numbers": int(any(c.isdigit() for c in receiver)),
        "has_suspicious": int(has_suspicious),
        "is_upi_id": int('@' in receiver)
    }

def extract_transaction_number_features(txn_number: str, ref_number: str = None) -> Dict[str, Any]:
    """
    Extract transaction number features for fraud detection
    HIGH PRECISION FRAUD INDICATORS based on transaction patterns
    """
    features = {
        "has_txn_number": 0,
        "txn_length": 0,
        "txn_has_pattern": 0,
        "txn_suspicious_pattern": 0,
        "txn_ref_mismatch": 0,
        "txn_sequential_digits": 0,
        "txn_repeating_digits": 0,
        "txn_all_same": 0
    }
    
    if not txn_number:
        return features
    
    features["has_txn_number"] = 1
    features["txn_length"] = len(txn_number)
    
    # Check for legitimate transaction number patterns
    # Real UPI transaction IDs are typically 12-16 alphanumeric characters
    if 10 <= len(txn_number) <= 20 and any(c.isalpha() for c in txn_number) and any(c.isdigit() for c in txn_number):
        features["txn_has_pattern"] = 1
    
    # FRAUD INDICATORS:
    
    # 1. Suspicious patterns (TEST, FAKE, DEMO, etc.)
    suspicious_keywords = ['TEST', 'FAKE', 'DEMO', 'SAMPLE', 'DUMMY', 'TEMP', 'TMP', 'XXX']
    if any(keyword in txn_number.upper() for keyword in suspicious_keywords):
        features["txn_suspicious_pattern"] = 1
    
    # 2. Too short or too long (legitimate UPI IDs are usually 10-20 chars)
    if len(txn_number) < 8 or len(txn_number) > 25:
        features["txn_suspicious_pattern"] = 1
    
    # 3. Sequential digits (123456, 654321) - common in fake transactions
    digits_only = ''.join(c for c in txn_number if c.isdigit())
    if len(digits_only) >= 6:
        for i in range(len(digits_only) - 5):
            seq = digits_only[i:i+6]
            if seq == ''.join(str((int(seq[0]) + j) % 10) for j in range(6)):
                features["txn_sequential_digits"] = 1
                break
            # Reverse sequential
            if seq == ''.join(str((int(seq[0]) - j) % 10) for j in range(6)):
                features["txn_sequential_digits"] = 1
                break
    
    # 4. Repeating digits (111111, 999999) - suspicious
    if len(digits_only) >= 6:
        for i in range(len(digits_only) - 5):
            if len(set(digits_only[i:i+6])) == 1:
                features["txn_repeating_digits"] = 1
                break
    
    # 5. All same character (AAAAAAA, 0000000)
    if len(txn_number) >= 6 and len(set(txn_number)) == 1:
        features["txn_all_same"] = 1
    
    # 6. Transaction number vs Reference number mismatch check
    # Legitimate transactions usually have consistent ref and txn patterns
    if ref_number and txn_number:
        # If both exist but have very different patterns, it's suspicious
        ref_alpha_ratio = sum(c.isalpha() for c in ref_number) / max(len(ref_number), 1)
        txn_alpha_ratio = sum(c.isalpha() for c in txn_number) / max(len(txn_number), 1)
        
        if abs(ref_alpha_ratio - txn_alpha_ratio) > 0.5:
            features["txn_ref_mismatch"] = 1
    
    return features

def extract_features(
    amount: float,
    time: str,
    receiver: str,
    account: str,
    text: Optional[str] = None,
    transaction_number: Optional[str] = None,
    reference_number: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract all features for fraud detection with HIGH PRECISION
    """
    features = {}
    
    # Time features
    time_features = extract_time_features(time)
    features.update(time_features)
    
    # Amount features
    amount_features = extract_amount_features(amount)
    features.update(amount_features)
    
    # Receiver features
    receiver_features = extract_receiver_features(receiver)
    features.update(receiver_features)
    
    # Transaction number features (HIGH PRECISION INDICATORS)
    txn_features = extract_transaction_number_features(transaction_number, reference_number)
    features.update(txn_features)
    
    # SMS text features (if available)
    if text:
        from app.utils.text_parser import extract_sms_features
        sms_features = extract_sms_features(text)
        features.update(sms_features)
    
    return features

def predict_fraud(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict if transaction is fraudulent
    
    Uses ML model if available, otherwise uses rule-based approach
    """
    model = get_model()
    
    if model is not None:
        try:
            # Prepare feature vector (adjust based on trained model)
            feature_vector = [
                features.get("amount", 0),
                features.get("is_odd_hour", 0),
                features.get("is_large_amount", 0),
                features.get("has_suspicious", 0),
                features.get("hour", 12),
            ]
            
            prediction = model.predict([feature_vector])[0]
            
            # Get probability if available
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba([feature_vector])[0]
                confidence = float(max(proba))
            else:
                confidence = 0.85
            
            is_fraud = prediction == 1
        except Exception as e:
            logger.error(f"Model prediction error: {e}. Falling back to rules.")
            is_fraud, confidence = rule_based_prediction(features)
    else:
        # Rule-based fallback
        is_fraud, confidence = rule_based_prediction(features)
    
    # Determine risk level and reason
    risk_level, reason = analyze_risk(features, is_fraud)
    
    return {
        "prediction": "Fraud" if is_fraud else "Legit",
        "confidence": round(confidence, 3),
        "risk_level": risk_level,
        "reason": reason
    }

def rule_based_prediction(features: Dict[str, Any]) -> tuple:
    """
    Rule-based fraud detection fallback with HIGH PRECISION
    """
    risk_score = 0
    
    # Time-based risk
    if features.get("is_odd_hour", 0):
        risk_score += 30
    
    # Amount-based risk
    if features.get("is_very_large", 0):
        risk_score += 25
    elif features.get("is_large_amount", 0):
        risk_score += 15
    
    # Round amounts can be suspicious
    if features.get("is_round_amount", 0) and features.get("amount", 0) > 5000:
        risk_score += 10
    
    # Receiver-based risk
    if features.get("has_suspicious", 0):
        risk_score += 20
    
    # SMS features (if available)
    if features.get("has_urgency", False):
        risk_score += 25
    if features.get("has_link", False):
        risk_score += 20
    
    # ===== HIGH PRECISION: Transaction Number Features =====
    # These are strong fraud indicators
    
    if features.get("txn_suspicious_pattern", 0):
        risk_score += 35  # Very high weight - TEST, FAKE patterns
    
    if features.get("txn_sequential_digits", 0):
        risk_score += 30  # Sequential numbers like 123456 are red flags
    
    if features.get("txn_repeating_digits", 0):
        risk_score += 25  # Repeating digits like 111111
    
    if features.get("txn_all_same", 0):
        risk_score += 40  # All same character = fake transaction
    
    if features.get("txn_ref_mismatch", 0):
        risk_score += 15  # Inconsistent transaction patterns
    
    # Legitimate transaction indicator (reduces risk)
    if features.get("has_txn_number", 0) and features.get("txn_has_pattern", 0):
        risk_score -= 10  # Proper transaction ID format reduces risk
    
    # Determine fraud
    is_fraud = risk_score >= 40
    confidence = min(0.98, 0.65 + (risk_score / 100))  # Higher confidence with txn features
    
    return is_fraud, confidence

def analyze_risk(features: Dict[str, Any], is_fraud: bool) -> tuple:
    """
    Analyze risk level and provide detailed reason with examples
    """
    reasons = []
    detailed_remarks = []
    
    # === HIGH PRECISION: Transaction Number Analysis ===
    if features.get("txn_suspicious_pattern"):
        reasons.append("suspicious transaction ID pattern")
        detailed_remarks.append(
            "🆔 **FAKE TRANSACTION ID DETECTED**: The transaction number contains suspicious patterns (TEST, FAKE, DEMO, etc.). "
            "Legitimate bank transactions use randomly generated alphanumeric IDs. "
            "**This is a STRONG FRAUD INDICATOR**. Examples of fake IDs: TEST123, FAKE999, DEMO001."
        )
    
    if features.get("txn_sequential_digits"):
        reasons.append("sequential transaction number")
        detailed_remarks.append(
            "🔢 **Sequential Pattern Alert**: Transaction ID contains sequential digits (e.g., 123456, 654321). "
            "Real UPI transaction IDs use random generation and rarely have long sequential patterns. "
            "Fraudsters often use simple sequences for fake transactions."
        )
    
    if features.get("txn_repeating_digits"):
        reasons.append("repeating digits in transaction ID")
        detailed_remarks.append(
            "🔁 **Repeating Pattern Detected**: Transaction number has repeating digits (e.g., 111111, 999999). "
            "Legitimate transaction IDs are randomly generated with good entropy. "
            "This pattern indicates a manually created or fake transaction."
        )
    
    if features.get("txn_all_same"):
        reasons.append("invalid transaction ID format")
        detailed_remarks.append(
            "❌ **CRITICAL: Invalid Transaction ID**: All characters in the transaction number are identical (e.g., AAAAAAA, 0000000). "
            "**This is DEFINITELY a fake transaction**. No legitimate bank system would generate such an ID. "
            "STOP THIS TRANSACTION IMMEDIATELY!"
        )
    
    if features.get("txn_ref_mismatch"):
        reasons.append("inconsistent transaction identifiers")
        detailed_remarks.append(
            "⚠️ **Transaction ID Mismatch**: The transaction number and reference number have very different patterns. "
            "In legitimate transactions, these identifiers follow consistent formatting from the same bank system. "
            "This inconsistency suggests tampering or fabrication."
        )
    
    if features.get("is_odd_hour"):
        reasons.append("unusual late-night transaction")
        hour = features.get("hour", 0)
        detailed_remarks.append(
            f"⏰ **Unusual Time Alert**: Transaction occurred at {hour:02d}:00 hrs, which is outside normal business hours (6 AM - 10 PM). "
            "Fraudsters often operate during odd hours to avoid immediate detection."
        )
    
    if features.get("is_very_large"):
        reasons.append("exceptionally high amount")
        amount = features.get("amount", 0)
        detailed_remarks.append(
            f"💰 **High-Value Transaction**: Amount of ₹{amount:,.2f} is significantly higher than typical transactions. "
            "Large amounts are often used in sophisticated fraud schemes. Examples: Fake investment scams (₹50,000+), unauthorized bulk transfers."
        )
    elif features.get("is_large_amount"):
        reasons.append("large transaction amount")
        amount = features.get("amount", 0)
        detailed_remarks.append(
            f"💵 **Elevated Amount**: Transaction of ₹{amount:,.2f} is above average. "
            "Verify this is an authorized transaction. Common scenarios: Business payments, rent, EMI payments."
        )
    
    if features.get("is_round_amount") and features.get("amount", 0) > 5000:
        detailed_remarks.append(
            "🔢 **Round Amount Pattern**: Exact round numbers like ₹5,000, ₹10,000 are commonly used in scams. "
            "Legitimate transactions often have specific amounts (e.g., ₹4,847.50 for a bill)."
        )
    
    if features.get("has_suspicious"):
        reasons.append("suspicious receiver pattern")
        detailed_remarks.append(
            "⚠️ **Suspicious Receiver**: The receiver name contains red-flag keywords (unknown, test, verify, urgent). "
            "Examples of fraud: 'Verify-UPI', 'Urgent-Payment', 'Test-Merchant'. Always verify receiver identity before sending money."
        )
    
    if features.get("has_urgency"):
        reasons.append("urgency keywords detected")
        detailed_remarks.append(
            "🚨 **Urgency Scam Detected**: Message contains pressure tactics like 'Call Now', 'Immediate Action Required', 'Account will be blocked'. "
            "Real banks never create urgency. Examples: Fake KYC updates, phishing SMS claiming account suspension."
        )
    
    if features.get("has_link"):
        reasons.append("contains external link")
        detailed_remarks.append(
            "🔗 **Phishing Link Alert**: Message contains external URL. NEVER click links in transaction SMS. "
            "Fraudsters use fake banking sites to steal credentials. Example: 'Click here to verify your UPI' - This is ALWAYS a scam."
        )
    
    if not features.get("is_upi_id"):
        detailed_remarks.append(
            "📱 **Non-UPI Receiver**: Transaction not to a standard UPI ID. "
            "Verify receiver details carefully. Legitimate UPI IDs format: name@bank (e.g., user@paytm)."
        )
    
    # Additional fraud patterns
    if is_fraud and len(reasons) >= 3:
        detailed_remarks.append(
            "🎯 **Multiple Red Flags**: This transaction shows several fraud indicators simultaneously. "
            "**Common Fraud Scenarios**: "
            "\n• Lottery/Prize scams requiring upfront payment"
            "\n• Fake customer support asking for 'verification' payments"
            "\n• Romance scams requesting money transfers"
            "\n• Job scams asking for 'registration fees'"
            "\n• Cryptocurrency investment fraud"
            "\n\n**Action Required**: DO NOT proceed. Contact your bank immediately if money was already sent."
        )
    
    # Determine risk level
    if is_fraud:
        if len(reasons) >= 3:
            risk_level = "Critical"
            reason = "🚨 CRITICAL FRAUD ALERT: " + ", ".join(reasons)
        else:
            risk_level = "High"
            reason = "⚠️ HIGH RISK: " + ", ".join(reasons)
    else:
        if not reasons:
            risk_level = "Low"
            reason = "✅ Transaction appears legitimate with standard patterns"
            detailed_remarks.append(
                "✓ **Safe Transaction Indicators**: "
                "\n• Transaction during business hours"
                "\n• Normal amount range"
                "\n• Recognized receiver pattern"
                "\n• No urgency or phishing attempts"
                "\n\n**Best Practices**: "
                "\n• Always verify receiver details"
                "\n• Keep transaction receipts"
                "\n• Enable SMS/email alerts"
                "\n• Never share UPI PIN/OTP"
            )
        else:
            risk_level = "Medium"
            reason = "⚡ MEDIUM RISK: " + ", ".join(reasons)
            detailed_remarks.append(
                "⚠️ **Proceed with Caution**: While not clearly fraudulent, this transaction has some unusual characteristics. "
                "Verify all details before proceeding."
            )
    
    # Combine all remarks
    full_reason = reason
    if detailed_remarks:
        full_reason += "\n\n" + "\n\n".join(detailed_remarks)
    
    return risk_level, full_reason

