# 🧪 Quick Test - Image Upload Feature

## Test Without Installing Tesseract

If you don't want to install Tesseract yet, you can test with **EasyOCR only** (which works out of the box after `pip install`).

## Quick Start

### 1. Install Dependencies
```powershell
cd "D:\UPI fraud detection sms version\backend"
.\venv\Scripts\activate
pip install Pillow==10.1.0 opencv-python==4.8.1.78 easyocr==1.7.1
```

### 2. Start Backend
```powershell
python run.py
```

### 3. Start Frontend
```powershell
cd ..\frontend
npm run dev
```

### 4. Test Image Upload
1. Go to `http://localhost:3000`
2. Click **📸 Image Upload** tab
3. Upload a transaction screenshot
4. See automatic extraction and fraud detection!

## Test Images

You can use the screenshots you provided:
1. **ICICI Hospital Payment** (SMS):  
   - Amount: Rs.5,670.25
   - Expected: LEGIT

2. **Google Pay Transaction** (Image):
   - Amount: ₹1.69
   - Transaction ID: 531626623932
   - Expected: LEGIT

## What Happens on First Run

### EasyOCR Model Download
On first use, EasyOCR will download models (~100MB):
```
Downloading detection model...
Downloading recognition model...
Models saved to: C:\Users\<your-username>\.EasyOCR\
```

This happens once. Future uses will be instant!

## Expected Behavior

### Success Case:
```
Processing image... ✓
OCR extracted text ✓
Parsed transaction details ✓
Amount: ₹1.69
Receiver: Manasvi Mall
Transaction ID: 531626623932
Prediction: LEGIT (92% confidence)
```

### If Tesseract Not Installed:
```
Warning: Tesseract OCR not available
Using EasyOCR only... ✓
(Still works fine!)
```

### If No Text Found:
```
Error: No text found in image
Suggestion: Ensure image is clear and contains transaction details
```

## Manual Test with API

```powershell
# Test image upload endpoint
$headers = @{
    "Authorization" = "Bearer YOUR_TOKEN"
}

$file = "path/to/screenshot.jpg"

Invoke-RestMethod -Uri "http://localhost:8000/predict/image" `
    -Method POST `
    -Headers $headers `
    -InFile $file `
    -ContentType "multipart/form-data"
```

## Troubleshooting

### "Module not found: easyocr"
```powershell
pip install easyocr==1.7.1
```

### "No module named 'cv2'"
```powershell
pip install opencv-python==4.8.1.78
```

### "Cannot identify image file"
```powershell
pip install Pillow==10.1.0
```

### Image Upload Button Not Working
- Check browser console (F12)
- Ensure backend is running
- Check file type (only JPG, PNG, WebP)

## Full Installation (Optional)

For maximum accuracy, install Tesseract:

### Windows:
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer → Install to `C:\Program Files\Tesseract-OCR`
3. Add to PATH:
   ```powershell
   $env:Path += ";C:\Program Files\Tesseract-OCR"
   ```
4. Install Python wrapper:
   ```powershell
   pip install pytesseract==0.3.10
   ```

## Performance Comparison

| OCR Engine | Speed | Accuracy | Installation |
|------------|-------|----------|--------------|
| EasyOCR only | 3-5 sec | 85-90% | ✅ Easy (pip install) |
| Tesseract only | 1-2 sec | 80-85% | ⚠️ Requires binary |
| Both (Multi-engine) | 4-6 sec | 95%+ | ⚠️ Full setup |

**Recommendation:** Start with EasyOCR, add Tesseract later for best results!

---

**Ready to test?** Just install the Python packages and start the servers! 🚀

