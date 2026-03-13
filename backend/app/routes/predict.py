from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.transaction_schema import ManualTransactionInput, SMSInput, PredictionResponse
from app.utils.text_parser import parse_sms
from app.utils.preprocessor import extract_features, predict_fraud
from app.utils.image_ocr import extract_text_from_image, parse_transaction_from_ocr
from app.db.connection import get_db_session
from app.db.models import TransactionLog as DBTransactionLog
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/manual", response_model=PredictionResponse)
async def predict_manual(data: ManualTransactionInput):
    """
    Predict fraud for manually entered transaction data
    """
    try:
        # Extract features and predict
        features = extract_features(
            amount=data.amount,
            time=data.time,
            receiver=data.receiver,
            account=data.account,
            transaction_number=data.transaction_number,
            reference_number=data.reference_number
        )
        
        result = predict_fraud(features)
        
        # Log to database
        try:
            db = next(get_db_session())
            log_entry = DBTransactionLog(
                account=data.account,
                amount=data.amount,
                receiver=data.receiver,
                date=data.date,
                time=data.time,
                raw_text=None,
                prediction=result["prediction"],
                confidence=result["confidence"],
                risk_level=result["risk_level"],
                reference_number=data.reference_number,
                transaction_number=data.transaction_number,
                transaction_type=data.transaction_type,
                bank_name=data.bank_name
            )
            db.add(log_entry)
            db.commit()
        except Exception as db_error:
            logger.warning(f"Database logging failed: {db_error}")
        
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            reason=result["reason"],
            amount=data.amount,
            time=data.time,
            reference_number=data.reference_number,
            transaction_number=data.transaction_number,
            transaction_type=data.transaction_type,
            bank_name=data.bank_name,
            account=data.account,
            receiver=data.receiver,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Manual prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/sms", response_model=PredictionResponse)
async def predict_sms(data: SMSInput):
    """
    Parse SMS text and predict fraud
    """
    try:
        # Parse SMS to extract transaction details
        parsed_data = parse_sms(data.text)
        
        if not parsed_data.get("amount"):
            raise HTTPException(
                status_code=400, 
                detail="Could not extract transaction details from SMS. Please check the format."
            )
        
        # Extract features and predict
        features = extract_features(
            amount=parsed_data["amount"],
            time=parsed_data.get("time", "12:00"),
            receiver=parsed_data.get("receiver", "unknown"),
            account=parsed_data.get("account", "unknown"),
            text=data.text,
            transaction_number=parsed_data.get("transaction_number"),
            reference_number=parsed_data.get("reference_number")
        )
        
        result = predict_fraud(features)
        
        # Log to database
        try:
            db = next(get_db_session())
            log_entry = DBTransactionLog(
                account=parsed_data.get("account"),
                amount=parsed_data["amount"],
                receiver=parsed_data.get("receiver"),
                date=parsed_data.get("date"),
                time=parsed_data.get("time"),
                raw_text=data.text,
                prediction=result["prediction"],
                confidence=result["confidence"],
                risk_level=result["risk_level"],
                reference_number=parsed_data.get("reference_number"),
                transaction_number=parsed_data.get("transaction_number"),
                transaction_type=parsed_data.get("transaction_type"),
                bank_name=parsed_data.get("bank_name")
            )
            db.add(log_entry)
            db.commit()
        except Exception as db_error:
            logger.warning(f"Database logging failed: {db_error}")
        
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            reason=result["reason"],
            amount=parsed_data["amount"],
            time=parsed_data.get("time"),
            reference_number=parsed_data.get("reference_number"),
            transaction_number=parsed_data.get("transaction_number"),
            transaction_type=parsed_data.get("transaction_type"),
            bank_name=parsed_data.get("bank_name"),
            account=parsed_data.get("account"),
            receiver=parsed_data.get("receiver"),
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"SMS prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"SMS parsing failed: {str(e)}")


@router.post("/image", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    """
    Predict fraud from transaction image/screenshot using OCR
    HIGH PRECISION image processing with multiple OCR engines
    """
    try:
        logger.info(f"Received image upload: {file.filename} ({file.content_type})")
        
        # Validate file type
        valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if file.content_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload JPG, PNG, or WebP image."
            )
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Validate file size (max 10MB)
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Image size too large. Maximum 10MB allowed."
            )
        
        logger.info(f"Processing image: {len(image_bytes)} bytes")
        
        # Extract text from image using OCR
        try:
            extracted_text = extract_text_from_image(image_bytes)
            logger.info(f"OCR extracted {len(extracted_text)} characters")
        except Exception as ocr_error:
            logger.error(f"OCR extraction failed: {ocr_error}")
            raise HTTPException(
                status_code=422,
                detail=f"Failed to extract text from image. Please ensure the image is clear and contains transaction details. Error: {str(ocr_error)}"
            )
        
        if not extracted_text.strip():
            raise HTTPException(
                status_code=422,
                detail="No text found in image. Please upload a clear transaction screenshot."
            )
        
        # Parse transaction details from OCR text
        parsed_data = parse_transaction_from_ocr(extracted_text)
        logger.info(f"Parsed transaction data: {parsed_data}")
        
        # Validate essential fields
        if not parsed_data.get("amount"):
            raise HTTPException(
                status_code=400,
                detail="Could not extract transaction amount from image. Please ensure the amount is clearly visible or use manual input."
            )
        
        # Extract features and predict
        features = extract_features(
            amount=parsed_data["amount"],
            time=parsed_data.get("time", datetime.now().strftime("%H:%M")),
            receiver=parsed_data.get("receiver", "unknown"),
            account=parsed_data.get("account", "unknown"),
            text=extracted_text,
            transaction_number=parsed_data.get("transaction_number"),
            reference_number=parsed_data.get("reference_number")
        )
        
        result = predict_fraud(features)
        
        # Log to database
        try:
            db = next(get_db_session())
            log_entry = DBTransactionLog(
                account=parsed_data.get("account"),
                amount=parsed_data["amount"],
                receiver=parsed_data.get("receiver"),
                date=parsed_data.get("date"),
                time=parsed_data.get("time"),
                raw_text=extracted_text[:500],  # Store first 500 chars of OCR text
                prediction=result["prediction"],
                confidence=result["confidence"],
                risk_level=result["risk_level"],
                reference_number=parsed_data.get("reference_number"),
                transaction_number=parsed_data.get("transaction_number"),
                transaction_type=parsed_data.get("transaction_type"),
                bank_name=parsed_data.get("bank_name")
            )
            db.add(log_entry)
            db.commit()
        except Exception as db_error:
            logger.warning(f"Database logging failed: {db_error}")
        
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            reason=result["reason"],
            amount=parsed_data["amount"],
            time=parsed_data.get("time"),
            reference_number=parsed_data.get("reference_number"),
            transaction_number=parsed_data.get("transaction_number"),
            transaction_type=parsed_data.get("transaction_type"),
            bank_name=parsed_data.get("bank_name"),
            account=parsed_data.get("account"),
            receiver=parsed_data.get("receiver"),
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

