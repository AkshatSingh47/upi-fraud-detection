# 🏗️ System Architecture - UPI Fraud Detection

Comprehensive architecture overview of the AI-powered fraud detection system.

## 🎯 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│                    (React + TailwindCSS)                     │
│  ┌─────────────────┐           ┌─────────────────┐         │
│  │  Manual Input   │           │   SMS Input     │         │
│  │  Form           │           │   Form          │         │
│  └────────┬────────┘           └────────┬────────┘         │
│           │                              │                   │
│           └──────────────┬───────────────┘                   │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       API LAYER                              │
│                      (FastAPI)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  /predict    │  │    /logs     │  │   /health    │     │
│  │  /manual     │  │    /stats    │  │              │     │
│  │  /sms        │  │              │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘     │
└─────────┼──────────────────┼────────────────────────────────┘
          │                  │
          ▼                  ▼
┌──────────────────┐  ┌──────────────────┐
│  BUSINESS LOGIC  │  │   DATA ACCESS    │
│                  │  │                  │
│ ┌──────────────┐ │  │ ┌──────────────┐ │
│ │ SMS Parser   │ │  │ │  SQLAlchemy  │ │
│ └──────────────┘ │  │ └──────────────┘ │
│ ┌──────────────┐ │  │ ┌──────────────┐ │
│ │Feature       │ │  │ │  PostgreSQL  │ │
│ │Extractor     │ │  │ │  / SQLite    │ │
│ └──────┬───────┘ │  │ └──────────────┘ │
└────────┼─────────┘  └──────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│         ML INFERENCE ENGINE           │
│                                       │
│  ┌─────────────────────────────┐    │
│  │   Gradient Boosting Model   │    │
│  │   (fraud_model.pkl)         │    │
│  └─────────────────────────────┘    │
│                                       │
│  Features:                            │
│  • Time-based patterns               │
│  • Amount analysis                   │
│  • Receiver patterns                 │
│  • SMS urgency detection             │
└──────────────────────────────────────┘
```

## 🔄 Request Flow

### Manual Transaction Flow

```
1. User fills Manual Input Form
   ├─ Account: user@paytm
   ├─ Amount: 5000
   ├─ Receiver: merchant@upi
   ├─ Date: 2025-11-12
   └─ Time: 23:45
         │
         ▼
2. Frontend validates input
   └─ Pydantic schema validation
         │
         ▼
3. POST /predict/manual
   └─ Request body: JSON
         │
         ▼
4. Feature Extraction
   ├─ Time features (hour, is_odd_hour)
   ├─ Amount features (log, is_large, is_round)
   └─ Receiver features (pattern analysis)
         │
         ▼
5. ML Model Prediction
   ├─ Input: Feature vector [5000, 1, 1, 0, 23]
   └─ Output: Prediction + Confidence
         │
         ▼
6. Risk Analysis
   ├─ Determine risk level (Low/Medium/High/Critical)
   └─ Generate reasoning
         │
         ▼
7. Database Logging
   └─ Save to transaction_logs table
         │
         ▼
8. Response
   ├─ Prediction: "Fraud"
   ├─ Confidence: 0.923
   ├─ Risk Level: "High"
   └─ Reason: "unusual late-night transaction"
         │
         ▼
9. Frontend Display
   ├─ ResultCard animation
   ├─ Toast notification
   └─ History table update
```

### SMS Transaction Flow

```
1. User pastes SMS text
   "Your UPI transaction of Rs.5000.00 to merchant@upi
    on 12-Nov-25 at 23:45 was successful."
         │
         ▼
2. POST /predict/sms
   └─ Request: { "text": "..." }
         │
         ▼
3. SMS Parsing
   ├─ Extract amount: 5000.00
   ├─ Extract receiver: merchant@upi
   ├─ Extract date: 12-Nov-25
   ├─ Extract time: 23:45
   └─ Detect urgency keywords
         │
         ▼
4. Feature Extraction
   (Same as manual flow)
         │
         ▼
5. ML Prediction
   (Same as manual flow)
         │
         ▼
6. Response + Display
   (Same as manual flow)
```

## 🧩 Component Architecture

### Frontend Components

```
App.jsx
  │
  ├─ Home.jsx
       │
       ├─ ManualInputForm.jsx
       │    ├─ Form inputs
       │    ├─ Validation
       │    └─ API call (predictManual)
       │
       ├─ SMSInputForm.jsx
       │    ├─ Text area
       │    ├─ Example button
       │    └─ API call (predictSMS)
       │
       ├─ ResultCard.jsx
       │    ├─ Prediction display
       │    ├─ Risk visualization
       │    └─ Recommendations
       │
       └─ HistoryTable.jsx
            ├─ Transaction list
            ├─ Filtering
            └─ API call (getLogs)
```

### Backend Modules

```
main.py (FastAPI App)
  │
  ├─ routes/
  │    ├─ predict.py
  │    │    ├─ POST /predict/manual
  │    │    └─ POST /predict/sms
  │    │
  │    └─ logs.py
  │         ├─ GET /logs
  │         └─ GET /logs/stats
  │
  ├─ utils/
  │    ├─ text_parser.py
  │    │    ├─ parse_sms()
  │    │    ├─ contains_urgency_keywords()
  │    │    └─ extract_sms_features()
  │    │
  │    └─ preprocessor.py
  │         ├─ extract_features()
  │         ├─ predict_fraud()
  │         ├─ rule_based_prediction()
  │         └─ analyze_risk()
  │
  ├─ db/
  │    ├─ models.py (TransactionLog)
  │    └─ connection.py (SQLAlchemy setup)
  │
  └─ schemas/
       └─ transaction_schema.py
            ├─ ManualTransactionInput
            ├─ SMSInput
            ├─ PredictionResponse
            └─ TransactionLog
```

## 🧠 ML Pipeline Architecture

### Training Pipeline

```
1. Data Preparation
   ├─ Load dataset (transactions.csv)
   ├─ Split train/test (80/20)
   └─ Stratified sampling
         │
         ▼
2. Feature Engineering
   ├─ Amount features
   ├─ Time features
   ├─ Receiver features
   └─ SMS features
         │
         ▼
3. Model Training
   ├─ Gradient Boosting ──┐
   ├─ Random Forest     ──┤
   └─ Logistic Regression ┤
         │                │
         ▼                │
4. Model Evaluation       │
   ├─ Accuracy      ◄─────┤
   ├─ Precision     ◄─────┤
   ├─ Recall        ◄─────┤
   └─ F1 Score      ◄─────┘
         │
         ▼
5. Model Selection
   └─ Best F1 Score
         │
         ▼
6. Model Serialization
   └─ Save as fraud_model.pkl
```

### Inference Pipeline

```
Input Features
    │
    ├─ amount: 5000
    ├─ is_odd_hour: 1
    ├─ is_large_amount: 1
    ├─ has_suspicious: 0
    └─ hour: 23
         │
         ▼
Feature Vector: [5000, 1, 1, 0, 23]
         │
         ▼
ML Model (Gradient Boosting)
         │
         ▼
Raw Prediction: 1 (Fraud)
Probability: [0.077, 0.923]
         │
         ▼
Post-Processing
    ├─ Confidence: 0.923
    ├─ Risk Level: "High"
    └─ Reasoning: "unusual late-night transaction"
         │
         ▼
Final Output
```

## 💾 Database Schema

```sql
┌─────────────────────────────────────────────┐
│         transaction_logs                     │
├─────────────────────────────────────────────┤
│ id              INTEGER PRIMARY KEY          │
│ account         VARCHAR(255)                 │
│ amount          FLOAT NOT NULL               │
│ receiver        VARCHAR(255)                 │
│ date            VARCHAR(50)                  │
│ time            VARCHAR(50)                  │
│ raw_text        TEXT                         │
│ prediction      VARCHAR(50) NOT NULL         │
│ confidence      FLOAT NOT NULL               │
│ risk_level      VARCHAR(50) NOT NULL         │
│ created_at      DATETIME NOT NULL            │
└─────────────────────────────────────────────┘

Indexes:
  - PRIMARY KEY on id
  - INDEX on prediction (for filtering)
  - INDEX on created_at (for sorting)
```

## 🔐 Security Architecture

### Input Validation

```
User Input
    │
    ▼
Frontend Validation
    ├─ Type checking
    ├─ Required fields
    └─ Format validation
    │
    ▼
Backend Validation (Pydantic)
    ├─ Schema validation
    ├─ Type coercion
    └─ Range validation
    │
    ▼
Sanitization
    ├─ SQL injection prevention (SQLAlchemy)
    └─ XSS prevention (React)
```

### CORS Policy

```
Frontend (localhost:3000)
    │
    │ CORS Headers
    ▼
Backend (localhost:8000)
    ├─ Allow-Origin: *
    ├─ Allow-Methods: *
    └─ Allow-Headers: *

Production:
    ├─ Allow-Origin: https://yourdomain.com
    └─ Credentials: true
```

## 📊 Data Flow Diagram

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     ▼
┌─────────────────┐
│   Frontend      │ ◄──── React State Management
│   (React)       │ ◄──── Form Validation
└────┬────────────┘
     │
     │ HTTP Request
     ▼
┌─────────────────┐
│   API Gateway   │ ◄──── CORS
│   (FastAPI)     │ ◄──── Rate Limiting (future)
└────┬────────────┘
     │
     ├──────┬──────┬──────┐
     │      │      │      │
     ▼      ▼      ▼      ▼
┌────────┐ ┌────┐ ┌────┐ ┌────┐
│ Parser │ │ ML │ │ DB │ │Logs│
└────────┘ └────┘ └────┘ └────┘
     │       │      │      │
     └───────┴──────┴──────┘
             │
             ▼
      ┌──────────────┐
      │   Response   │
      └──────────────┘
             │
             ▼
      ┌──────────────┐
      │  Frontend    │
      │  Display     │
      └──────────────┘
```

## 🔄 State Management

### Frontend State

```
Home Component State
    │
    ├─ result: PredictionResult | null
    │    └─ Updated on successful prediction
    │
    └─ refreshHistory: number
         └─ Incremented to trigger history refresh
              │
              ▼
         HistoryTable watches this
         Re-fetches when it changes
```

### Backend State

```
Application Startup
    │
    ├─ Load ML Model
    │    └─ Global _model variable
    │
    └─ Initialize Database
         └─ Create tables if not exist

Request Handling (Stateless)
    │
    ├─ Parse request
    ├─ Extract features
    ├─ Predict
    └─ Log + Respond
```

## ⚡ Performance Considerations

### Backend Optimization

```
1. Model Loading
   └─ Singleton pattern (load once)

2. Database Connections
   └─ Connection pooling (SQLAlchemy)

3. Feature Extraction
   └─ Vectorized operations (NumPy)

4. API Response
   └─ Async endpoints (FastAPI)
```

### Frontend Optimization

```
1. Code Splitting
   └─ Dynamic imports (Vite)

2. Component Memoization
   └─ React.memo for expensive components

3. Lazy Loading
   └─ Images and large components

4. API Caching
   └─ React Query (future enhancement)
```

## 🚀 Deployment Architecture

### Development

```
Local Machine
    │
    ├─ Backend: localhost:8000
    │    └─ SQLite database
    │
    └─ Frontend: localhost:3000
         └─ Vite dev server
```

### Production (Recommended)

```
┌─────────────────────────────────────┐
│         Load Balancer               │
│         (Nginx/HAProxy)             │
└─────────┬───────────────────────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌────────┐  ┌────────┐
│Backend │  │Backend │  ◄─── Horizontal Scaling
│Server 1│  │Server 2│
└───┬────┘  └───┬────┘
    │           │
    └─────┬─────┘
          │
          ▼
    ┌──────────┐
    │PostgreSQL│
    │  Master  │
    └─────┬────┘
          │
          ▼
    ┌──────────┐
    │PostgreSQL│
    │  Replica │
    └──────────┘

Frontend: CDN (Vercel/Netlify)
```

## 📈 Scalability Strategy

### Horizontal Scaling

```
Single Server → Multiple Servers
    │
    ├─ Stateless API design
    ├─ Centralized database
    ├─ Session-less authentication
    └─ Load balancer distribution
```

### Database Scaling

```
SQLite → PostgreSQL → PostgreSQL + Replicas
    │
    ├─ Read replicas for logs
    ├─ Write master for predictions
    └─ Connection pooling
```

### Caching Layer (Future)

```
Request → Cache Check → Database
    │           │
    │ Hit       │ Miss
    ▼           ▼
Response    Fetch + Cache
```

## 🎯 Design Patterns Used

### Backend

- **Singleton**: ML model loading
- **Factory**: Model selection and creation
- **Repository**: Database abstraction
- **Strategy**: Multiple prediction algorithms
- **Dependency Injection**: FastAPI dependencies

### Frontend

- **Component Composition**: Building complex UIs
- **Container/Presentation**: Smart vs. dumb components
- **Hooks**: State and lifecycle management
- **Observer**: React state updates

### ML

- **Pipeline**: Sequential data transformations
- **Strategy**: Multiple model algorithms
- **Template Method**: Training pipeline steps

## 📝 Configuration Management

```
Environment Variables
    │
    ├─ .env (Backend)
    │    ├─ DATABASE_URL
    │    ├─ API_HOST
    │    └─ API_PORT
    │
    └─ .env (Frontend)
         └─ VITE_API_URL

Loaded at Runtime
    │
    ├─ Backend: python-dotenv
    └─ Frontend: Vite env handling
```

---

**This architecture supports production-grade scalability and maintainability! 🏗️**

