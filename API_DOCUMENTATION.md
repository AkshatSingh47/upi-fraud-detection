# 📡 API Documentation - UPI Fraud Detection

Complete API reference for the UPI Fraud Detection backend service.

## 🌐 Base URL

```
http://localhost:8000
```

For production, replace with your domain.

## 📋 Table of Contents

- [Authentication](#authentication)
- [Prediction Endpoints](#prediction-endpoints)
- [Logs Endpoints](#logs-endpoints)
- [Utility Endpoints](#utility-endpoints)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)

## 🔐 Authentication

Current version does not require authentication. For production, implement JWT or API key authentication.

## 🎯 Prediction Endpoints

### 1. Manual Transaction Prediction

Analyze a manually entered transaction for fraud.

**Endpoint:** `POST /predict/manual`

**Request Body:**
```json
{
  "account": "user@paytm",
  "amount": 5000.0,
  "receiver": "merchant@upi",
  "date": "2025-11-12",
  "time": "23:45"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| account | string | Yes | UPI ID or account identifier |
| amount | float | Yes | Transaction amount (> 0) |
| receiver | string | Yes | Receiver name or UPI ID |
| date | string | Yes | Transaction date (YYYY-MM-DD) |
| time | string | Yes | Transaction time (HH:MM) |

**Response:**
```json
{
  "prediction": "Fraud",
  "confidence": 0.923,
  "risk_level": "High",
  "reason": "Potential fraud detected: unusual late-night transaction, large transaction amount",
  "amount": 5000.0,
  "time": "23:45",
  "timestamp": "2025-11-12T15:30:45.123456"
}
```

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/predict/manual" \
  -H "Content-Type: application/json" \
  -d '{
    "account": "user@paytm",
    "amount": 5000.0,
    "receiver": "merchant@upi",
    "date": "2025-11-12",
    "time": "23:45"
  }'
```

**Example using Python:**
```python
import requests

data = {
    "account": "user@paytm",
    "amount": 5000.0,
    "receiver": "merchant@upi",
    "date": "2025-11-12",
    "time": "23:45"
}

response = requests.post(
    "http://localhost:8000/predict/manual",
    json=data
)

print(response.json())
```

---

### 2. SMS Transaction Prediction

Parse and analyze a UPI transaction SMS for fraud.

**Endpoint:** `POST /predict/sms`

**Request Body:**
```json
{
  "text": "Your UPI transaction of Rs.5000.00 to merchant@upi on 12-Nov-25 at 23:45 was successful. UPI Ref: 987654321"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | Yes | Complete SMS text |

**Response:**
```json
{
  "prediction": "Legit",
  "confidence": 0.876,
  "risk_level": "Low",
  "reason": "Transaction appears legitimate",
  "amount": 5000.0,
  "time": "23:45",
  "timestamp": "2025-11-12T15:30:45.123456"
}
```

**Supported SMS Formats:**
- Standard bank UPI messages
- Paytm, PhonePe, Google Pay formats
- Various date/time formats
- Multiple currency notations (Rs, INR, ₹)

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/predict/sms" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your UPI transaction of Rs.5000.00 to merchant@upi on 12-Nov-25 at 23:45 was successful."
  }'
```

---

## 📊 Logs Endpoints

### 3. Get Transaction Logs

Retrieve historical transaction predictions.

**Endpoint:** `GET /logs`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | int | 50 | Max number of logs (max: 500) |
| skip | int | 0 | Number of logs to skip |
| prediction | string | null | Filter by "Fraud" or "Legit" |

**Response:**
```json
[
  {
    "id": 1,
    "account": "user@paytm",
    "amount": 5000.0,
    "receiver": "merchant@upi",
    "date": "2025-11-12",
    "time": "23:45",
    "raw_text": null,
    "prediction": "Fraud",
    "confidence": 0.923,
    "risk_level": "High",
    "created_at": "2025-11-12T15:30:45.123456"
  }
]
```

**Examples:**

Get all logs:
```bash
curl "http://localhost:8000/logs"
```

Get only fraud transactions:
```bash
curl "http://localhost:8000/logs?prediction=Fraud"
```

Get last 10 legitimate transactions:
```bash
curl "http://localhost:8000/logs?limit=10&prediction=Legit"
```

Pagination:
```bash
curl "http://localhost:8000/logs?limit=20&skip=40"
```

---

### 4. Get Statistics

Get overall fraud detection statistics.

**Endpoint:** `GET /logs/stats`

**Response:**
```json
{
  "total_transactions": 150,
  "fraud_detected": 45,
  "legitimate": 105,
  "fraud_percentage": 30.0
}
```

**Example:**
```bash
curl "http://localhost:8000/logs/stats"
```

---

## 🛠️ Utility Endpoints

### 5. Root

API information.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "UPI Fraud Detection API",
  "status": "active",
  "version": "1.0.0"
}
```

---

### 6. Health Check

Check API health status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "UPI Fraud Detection"
}
```

---

## 📝 Response Formats

### Prediction Response

```typescript
{
  prediction: "Fraud" | "Legit",
  confidence: number,        // 0.0 to 1.0
  risk_level: "Low" | "Medium" | "High" | "Critical",
  reason: string,
  amount?: number,
  time?: string,
  timestamp: string          // ISO 8601 format
}
```

### Transaction Log

```typescript
{
  id: number,
  account: string | null,
  amount: number,
  receiver: string | null,
  date: string | null,
  time: string | null,
  raw_text: string | null,
  prediction: "Fraud" | "Legit",
  confidence: number,
  risk_level: string,
  created_at: string         // ISO 8601 format
}
```

---

## ⚠️ Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (validation error) |
| 404 | Not Found |
| 422 | Unprocessable Entity (invalid data) |
| 500 | Internal Server Error |

### Error Examples

**400 - Validation Error:**
```json
{
  "detail": "Could not extract transaction details from SMS. Please check the format."
}
```

**422 - Invalid Data:**
```json
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

**500 - Server Error:**
```json
{
  "detail": "Prediction failed: Model not loaded"
}
```

---

## 🔍 Interactive API Documentation

FastAPI provides automatic interactive API documentation:

### Swagger UI
Visit: `http://localhost:8000/docs`

Features:
- Try API calls directly from browser
- See request/response schemas
- Test with different parameters

### ReDoc
Visit: `http://localhost:8000/redoc`

Features:
- Clean, readable documentation
- Detailed schema information
- Example requests and responses

---

## 💡 Usage Tips

### 1. Time Format is Critical

The `time` field significantly impacts fraud detection:
```json
{
  "time": "23:45"  // Late night = Higher risk
}
```

vs

```json
{
  "time": "14:30"  // Business hours = Lower risk
}
```

### 2. Amount Patterns

Large, round amounts are considered suspicious:
```json
{
  "amount": 50000  // Large, round = Suspicious
}
```

vs

```json
{
  "amount": 1234.56  // Specific amount = Less suspicious
}
```

### 3. SMS Parsing

For best SMS parsing results:
- Include complete SMS text
- Keep original formatting
- Include amount, date, and time
- Don't manually edit SMS content

### 4. Rate Limiting (Production)

Implement rate limiting in production:
- Use Redis for distributed rate limiting
- Limit: 100 requests per minute per IP
- Return 429 status when exceeded

---

## 🔗 Integration Examples

### JavaScript/TypeScript (Frontend)

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Manual prediction
async function predictManual(data) {
  const response = await api.post('/predict/manual', data);
  return response.data;
}

// SMS prediction
async function predictSMS(text) {
  const response = await api.post('/predict/sms', { text });
  return response.data;
}

// Get logs
async function getLogs(limit = 50, prediction = null) {
  const params = { limit };
  if (prediction) params.prediction = prediction;
  
  const response = await api.get('/logs', { params });
  return response.data;
}
```

### Python (Backend Integration)

```python
import requests

class FraudDetectionClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def predict_manual(self, account, amount, receiver, date, time):
        data = {
            "account": account,
            "amount": amount,
            "receiver": receiver,
            "date": date,
            "time": time
        }
        response = requests.post(f"{self.base_url}/predict/manual", json=data)
        return response.json()
    
    def predict_sms(self, text):
        response = requests.post(
            f"{self.base_url}/predict/sms",
            json={"text": text}
        )
        return response.json()
    
    def get_logs(self, limit=50, prediction=None):
        params = {"limit": limit}
        if prediction:
            params["prediction"] = prediction
        
        response = requests.get(f"{self.base_url}/logs", params=params)
        return response.json()

# Usage
client = FraudDetectionClient()
result = client.predict_manual(
    account="user@paytm",
    amount=5000.0,
    receiver="merchant@upi",
    date="2025-11-12",
    time="23:45"
)
print(result)
```

---

## 🚀 Production Deployment

### CORS Configuration

Update `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables

Set in production:
```env
DATABASE_URL=postgresql://user:pass@localhost/fraud_db
ALLOWED_ORIGINS=https://yourdomain.com
SECRET_KEY=your-secret-key
```

### HTTPS

Use HTTPS in production:
- Deploy behind Nginx/Apache
- Use Let's Encrypt for SSL
- Update frontend `VITE_API_URL` to HTTPS

---

**For more information, visit the interactive docs at `/docs` when running the server.**

