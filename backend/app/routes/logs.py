from fastapi import APIRouter, HTTPException, Query
from app.db.connection import get_db_session
from app.db.models import TransactionLog as DBTransactionLog
from app.schemas.transaction_schema import TransactionLog
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/", response_model=List[TransactionLog])
async def get_transaction_logs(
    limit: int = Query(default=50, le=500, description="Maximum number of logs to return"),
    skip: int = Query(default=0, ge=0, description="Number of logs to skip"),
    prediction: str = Query(default=None, description="Filter by prediction (Fraud/Legit)")
):
    """
    Retrieve transaction logs with optional filtering
    """
    try:
        db = next(get_db_session())
        query = db.query(DBTransactionLog)
        
        if prediction:
            query = query.filter(DBTransactionLog.prediction == prediction)
        
        logs = query.order_by(DBTransactionLog.created_at.desc()).offset(skip).limit(limit).all()
        
        return logs
    
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs: {str(e)}")

@router.get("/stats")
async def get_statistics():
    """
    Get overall fraud detection statistics
    """
    try:
        db = next(get_db_session())
        
        total_transactions = db.query(DBTransactionLog).count()
        fraud_count = db.query(DBTransactionLog).filter(DBTransactionLog.prediction == "Fraud").count()
        legit_count = db.query(DBTransactionLog).filter(DBTransactionLog.prediction == "Legit").count()
        
        return {
            "total_transactions": total_transactions,
            "fraud_detected": fraud_count,
            "legitimate": legit_count,
            "fraud_percentage": round((fraud_count / total_transactions * 100), 2) if total_transactions > 0 else 0
        }
    
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {str(e)}")

