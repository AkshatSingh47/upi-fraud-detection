from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TransactionLog(Base):
    """
    Transaction log model for storing all predictions
    """
    __tablename__ = "transaction_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    receiver = Column(String(255), nullable=True)
    date = Column(String(50), nullable=True)
    time = Column(String(50), nullable=True)
    raw_text = Column(Text, nullable=True)
    prediction = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    risk_level = Column(String(50), nullable=False)
    reference_number = Column(String(100), nullable=True)
    transaction_number = Column(String(100), nullable=True)
    transaction_type = Column(String(50), nullable=True)
    bank_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<TransactionLog(id={self.id}, amount={self.amount}, prediction={self.prediction})>"

