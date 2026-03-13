from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ManualTransactionInput(BaseModel):
    account: str = Field(..., description="Account identifier or UPI ID")
    amount: float = Field(..., gt=0, description="Transaction amount in INR")
    receiver: str = Field(..., description="Receiver name or UPI ID")
    date: str = Field(..., description="Transaction date (YYYY-MM-DD)")
    time: str = Field(..., description="Transaction time (HH:MM)")
    reference_number: Optional[str] = Field(None, description="Transaction reference number")
    transaction_number: Optional[str] = Field(None, description="Transaction/UPI ID number")
    transaction_type: Optional[str] = Field(None, description="Type: Sent/Received/Paid")
    bank_name: Optional[str] = Field(None, description="Bank name")

    class Config:
        json_schema_extra = {
            "example": {
                "account": "user@paytm",
                "amount": 5000.0,
                "receiver": "merchant@upi",
                "date": "2025-11-12",
                "time": "23:45",
                "reference_number": "113988090014",
                "transaction_number": "TXN987654321",
                "transaction_type": "Sent",
                "bank_name": "HDFC Bank"
            }
        }

class SMSInput(BaseModel):
    text: str = Field(..., description="Full SMS text to parse")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Your UPI transaction of Rs.5000.00 to merchant@upi on 12-Nov-25 at 23:45 was successful. UPI Ref: 987654321"
            }
        }

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    risk_level: str
    reason: str
    amount: Optional[float] = None
    time: Optional[str] = None
    reference_number: Optional[str] = None
    transaction_number: Optional[str] = None
    transaction_type: Optional[str] = None
    bank_name: Optional[str] = None
    account: Optional[str] = None
    receiver: Optional[str] = None
    timestamp: str

class TransactionLog(BaseModel):
    id: int
    account: Optional[str]
    amount: float
    receiver: Optional[str]
    date: Optional[str]
    time: Optional[str]
    raw_text: Optional[str]
    prediction: str
    confidence: float
    risk_level: str
    reference_number: Optional[str]
    transaction_number: Optional[str]
    transaction_type: Optional[str]
    bank_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

