"""
High-Precision OCR for Transaction Image Processing
Supports multiple OCR engines for maximum accuracy
"""

import io
import re
from typing import Dict, Optional
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Try importing OCR libraries
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.warning("Tesseract OCR not available")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    logger.warning("EasyOCR not available")

# Initialize EasyOCR reader (supports English and Hindi)
_easyocr_reader = None

def get_easyocr_reader():
    """Lazy load EasyOCR reader"""
    global _easyocr_reader
    if EASYOCR_AVAILABLE and _easyocr_reader is None:
        try:
            _easyocr_reader = easyocr.Reader(['en', 'hi'], gpu=False)
            logger.info("EasyOCR reader initialized")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {e}")
    return _easyocr_reader


def preprocess_image_for_ocr(image: Image.Image) -> tuple:
    """
    Advanced image preprocessing for better OCR accuracy
    Returns both PIL and OpenCV versions
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize if too large (for faster processing)
    max_dimension = 2000
    if max(image.size) > max_dimension:
        ratio = max_dimension / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Enhance image for better OCR
    # 1. Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    # 2. Increase sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.3)
    
    # Convert to OpenCV format for advanced processing
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 3. Convert to grayscale
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # 4. Apply adaptive thresholding for better text extraction
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # 5. Denoise
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    
    # Convert back to PIL
    processed_pil = Image.fromarray(denoised)
    
    return image, processed_pil, img_cv


def extract_text_tesseract(image: Image.Image) -> str:
    """Extract text using Tesseract OCR"""
    if not TESSERACT_AVAILABLE:
        raise RuntimeError("Tesseract OCR is not available")
    
    try:
        # Configure Tesseract for better accuracy
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    except Exception as e:
        logger.error(f"Tesseract OCR error: {e}")
        return ""


def extract_text_easyocr(image: Image.Image) -> str:
    """Extract text using EasyOCR (more accurate for varied fonts)"""
    if not EASYOCR_AVAILABLE:
        raise RuntimeError("EasyOCR is not available")
    
    try:
        reader = get_easyocr_reader()
        if reader is None:
            return ""
        
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # Extract text
        results = reader.readtext(img_array, detail=0, paragraph=True)
        text = '\n'.join(results)
        return text
    except Exception as e:
        logger.error(f"EasyOCR error: {e}")
        return ""


def extract_text_multi_engine(original_image: Image.Image, processed_image: Image.Image) -> str:
    """
    Use multiple OCR engines and combine results for maximum accuracy
    """
    texts = []
    
    # Try EasyOCR first (generally more accurate)
    if EASYOCR_AVAILABLE:
        try:
            logger.info("Trying EasyOCR...")
            text = extract_text_easyocr(processed_image)
            if text.strip():
                texts.append(text)
                logger.info(f"EasyOCR extracted {len(text)} characters")
        except Exception as e:
            logger.error(f"EasyOCR failed: {e}")
    
    # Try Tesseract as fallback/supplement
    if TESSERACT_AVAILABLE:
        try:
            logger.info("Trying Tesseract OCR...")
            text = extract_text_tesseract(processed_image)
            if text.strip():
                texts.append(text)
                logger.info(f"Tesseract extracted {len(text)} characters")
        except Exception as e:
            logger.error(f"Tesseract failed: {e}")
    
    if not texts:
        raise RuntimeError("No OCR engine available or all engines failed")
    
    # Combine texts (prefer the longer one as it likely has more data)
    combined_text = max(texts, key=len)
    
    logger.info(f"Final extracted text length: {len(combined_text)} characters")
    return combined_text


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Main function to extract text from image with high precision
    """
    try:
        # Load image
        image = Image.open(io.BytesIO(image_bytes))
        logger.info(f"Image loaded: {image.size} {image.mode}")
        
        # Preprocess image
        original, processed, cv_image = preprocess_image_for_ocr(image)
        logger.info("Image preprocessing complete")
        
        # Extract text using multiple engines
        text = extract_text_multi_engine(original, processed)
        
        # Clean up text
        text = text.strip()
        
        logger.info(f"Successfully extracted text: {len(text)} characters")
        logger.debug(f"Extracted text preview: {text[:200]}...")
        
        return text
        
    except Exception as e:
        logger.error(f"Image OCR failed: {e}")
        raise RuntimeError(f"Failed to extract text from image: {str(e)}")


def parse_transaction_from_ocr(text: str) -> Dict[str, Optional[str]]:
    """
    Parse transaction details from OCR text with high precision
    Enhanced patterns for better extraction
    """
    from app.utils.text_parser import parse_sms
    
    # First, try standard SMS parsing
    parsed = parse_sms(text)
    
    # If basic parsing didn't work well, try advanced patterns for image text
    if not parsed.get("amount"):
        # Try to find amount patterns in OCR text
        amount_patterns = [
            r'[₹Rs\.]\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'Amount[:\s]+[₹Rs\.]*\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'Total[:\s]+[₹Rs\.]*\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'(\d+(?:,\d+)*(?:\.\d{2})?)\s*(?:rupees|rs|inr)',
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    parsed["amount"] = float(amount_str)
                    break
                except ValueError:
                    continue
    
    # Try to extract UPI ID / receiver
    if not parsed.get("receiver"):
        upi_patterns = [
            r'To[:\s]+([a-zA-Z0-9._-]+@[a-zA-Z]+)',
            r'Paid to[:\s]+([a-zA-Z0-9._-]+@[a-zA-Z]+)',
            r'([a-zA-Z0-9._-]+@(?:paytm|phonepe|gpay|okaxis|okhdfcbank|okicici|oksbi))',
        ]
        
        for pattern in upi_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parsed["receiver"] = match.group(1)
                break
    
    # Try to extract from account
    if not parsed.get("account"):
        account_patterns = [
            r'From[:\s]+([a-zA-Z0-9._-]+@[a-zA-Z]+)',
            r'Paid by[:\s]+([a-zA-Z0-9._-]+@[a-zA-Z]+)',
            r'([a-zA-Z0-9._-]+@[a-zA-Z]+)\s+to\s+',
        ]
        
        for pattern in account_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parsed["account"] = match.group(1)
                break
    
    # Extract transaction ID with higher precision
    if not parsed.get("transaction_number"):
        txn_patterns = [
            r'UPI\s*(?:transaction\s*)?(?:ID|No)?[:\s]*([A-Z0-9]{10,20})',
            r'Transaction\s*ID[:\s]*([A-Z0-9]{10,20})',
            r'Google\s*transaction\s*ID[:\s]*([A-Za-z0-9]{10,20})',
            r'Txn[:\s]*([A-Z0-9]{10,20})',
        ]
        
        for pattern in txn_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parsed["transaction_number"] = match.group(1)
                break
    
    # Extract date and time
    if not parsed.get("date") or not parsed.get("time"):
        datetime_patterns = [
            r'(\d{1,2})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})[,\s]+(\d{1,2}):(\d{2})\s*(am|pm)?',
            r'(\d{1,2})-(\d{1,2})-(\d{4})\s+(\d{1,2}):(\d{2})',
        ]
        
        for pattern in datetime_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Parse date/time based on pattern
                if not parsed.get("time"):
                    parsed["time"] = f"{match.group(3)}:{match.group(4)}"
                break
    
    logger.info(f"Parsed from OCR: {parsed}")
    return parsed

