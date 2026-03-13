import re
from datetime import datetime
from typing import Dict, Optional

def parse_sms(text: str) -> Dict:
    """
    Parse UPI transaction SMS to extract key details
    
    Supports multiple SMS formats from different banks/UPI apps
    """
    result = {
        "amount": None,
        "receiver": None,
        "account": None,
        "date": None,
        "time": None,
        "reference_number": None,
        "transaction_number": None,
        "transaction_type": None,
        "bank_name": None
    }
    
    # Extract amount - supports multiple formats
    amount_patterns = [
        r'Rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
        r'INR\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
        r'₹\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
        r'amount\s+(?:of\s+)?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(',', '')
            result["amount"] = float(amount_str)
            break
    
    # Extract receiver/merchant
    receiver_patterns = [
        r'to\s+([a-zA-Z0-9@._-]+)',
        r'merchant\s+([a-zA-Z0-9\s]+?)(?:\s+on|\s+at|\.|$)',
        r'paid\s+to\s+([a-zA-Z0-9\s@._-]+?)(?:\s+on|\s+via|\s+through)',
    ]
    
    for pattern in receiver_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["receiver"] = match.group(1).strip()
            break
    
    # Extract account/UPI ID
    account_patterns = [
        r'from\s+([a-zA-Z0-9@._-]+)',
        r'A/c\s+([A-Z0-9]+)',
        r'account\s+([0-9X]+)',
    ]
    
    for pattern in account_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["account"] = match.group(1).strip()
            break
    
    # Extract date
    date_patterns = [
        r'(\d{2})-([A-Za-z]{3})-(\d{2,4})',  # 12-Nov-25
        r'(\d{2})/(\d{2})/(\d{2,4})',        # 12/11/25
        r'(\d{4})-(\d{2})-(\d{2})',          # 2025-11-12
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            result["date"] = match.group(0)
            break
    
    # If no date found, use current date
    if not result["date"]:
        result["date"] = datetime.now().strftime("%Y-%m-%d")
    
    # Extract time
    time_patterns = [
        r'at\s+(\d{1,2}:\d{2}(?::\d{2})?)',
        r'(\d{1,2}:\d{2})\s*(?:AM|PM|am|pm)?',
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, text)
        if match:
            time_str = match.group(1)
            # Standardize to HH:MM format
            time_parts = time_str.split(':')
            result["time"] = f"{time_parts[0].zfill(2)}:{time_parts[1]}"
            break
    
    # If no time found, use current time
    if not result["time"]:
        result["time"] = datetime.now().strftime("%H:%M")
    
    # Extract reference number
    ref_patterns = [
        r'Ref:?\s*([A-Z0-9]+)',
        r'Reference:?\s*([A-Z0-9]+)',
        r'UPI Ref:?\s*([A-Z0-9]+)',
    ]
    
    for pattern in ref_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["reference_number"] = match.group(1)
            break
    
    # Extract transaction number/ID
    txn_patterns = [
        r'Txn:?\s*([A-Z0-9]+)',
        r'Transaction:?\s*(?:ID|No|Number):?\s*([A-Z0-9]+)',
        r'TXN:?\s*([A-Z0-9]+)',
        r'UPI ID:?\s*([A-Z0-9]+)',
    ]
    
    for pattern in txn_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["transaction_number"] = match.group(1)
            break
    
    # Extract transaction type
    text_lower = text.lower()
    if 'sent' in text_lower or 'debited' in text_lower or 'paid' in text_lower:
        result["transaction_type"] = "Sent"
    elif 'received' in text_lower or 'credited' in text_lower:
        result["transaction_type"] = "Received"
    else:
        result["transaction_type"] = "Transaction"
    
    # Extract bank name
    bank_patterns = [
        r'(HDFC Bank|ICICI Bank|SBI|Axis Bank|Kotak Bank|PNB|Bank of Baroda)',
        r'From\s+([A-Z\s]+Bank)',
    ]
    
    for pattern in bank_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["bank_name"] = match.group(1).strip()
            break
    
    return result

def contains_urgency_keywords(text: str) -> bool:
    """
    Check if SMS contains urgency/scam keywords
    """
    urgency_keywords = [
        'urgent', 'immediately', 'verify now', 'call now', 'block',
        'suspended', 'expired', 'action required', 'confirm now',
        'limited time', 'act fast', 'fraud', 'unauthorized',
        'click here', 'link', 'update kyc', 'refund', 'won prize'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in urgency_keywords)

def extract_sms_features(text: str) -> Dict:
    """
    Extract additional features from SMS for fraud detection
    """
    return {
        "has_urgency": contains_urgency_keywords(text),
        "length": len(text),
        "has_link": bool(re.search(r'http[s]?://|www\.', text)),
        "has_phone": bool(re.search(r'\d{10}', text)),
        "all_caps_ratio": sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0
    }

