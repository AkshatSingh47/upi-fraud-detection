# 📁 Project Structure - UPI Fraud Detection

Complete overview of the project organization and file purposes.

## 🌲 Directory Tree

```
upi-fraud-detection/
│
├── 📂 backend/                          # FastAPI Backend
│   ├── 📂 app/
│   │   ├── 📄 __init__.py              # Package initialization
│   │   ├── 📄 main.py                  # FastAPI app entry point
│   │   │
│   │   ├── 📂 routes/                  # API Endpoints
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 predict.py           # Fraud prediction routes
│   │   │   └── 📄 logs.py              # Transaction logs routes
│   │   │
│   │   ├── 📂 schemas/                 # Pydantic Models
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 transaction_schema.py # Request/Response schemas
│   │   │
│   │   ├── 📂 utils/                   # Utility Functions
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 text_parser.py       # SMS parsing logic
│   │   │   └── 📄 preprocessor.py      # Feature extraction & ML
│   │   │
│   │   ├── 📂 db/                      # Database Layer
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 connection.py        # DB connection & init
│   │   │   └── 📄 models.py            # SQLAlchemy models
│   │   │
│   │   └── 📂 models/                  # ML Models
│   │       ├── 📄 .gitkeep
│   │       └── 📄 fraud_model.pkl      # Trained model (created)
│   │
│   ├── 📄 .env.example                 # Environment template
│   ├── 📄 requirements.txt             # Python dependencies
│   ├── 📄 run.py                       # Server startup script
│   └── 📄 fraud_detection.db           # SQLite database (created)
│
├── 📂 frontend/                         # React Frontend
│   ├── 📂 src/
│   │   ├── 📄 main.jsx                 # React entry point
│   │   ├── 📄 App.jsx                  # Main App component
│   │   │
│   │   ├── 📂 pages/
│   │   │   └── 📄 Home.jsx             # Home page (main UI)
│   │   │
│   │   ├── 📂 components/              # React Components
│   │   │   ├── 📄 ManualInputForm.jsx  # Manual entry form
│   │   │   ├── 📄 SMSInputForm.jsx     # SMS paste form
│   │   │   ├── 📄 ResultCard.jsx       # Result display
│   │   │   └── 📄 HistoryTable.jsx     # Transaction history
│   │   │
│   │   ├── 📂 api/
│   │   │   └── 📄 predict.js           # API client functions
│   │   │
│   │   └── 📂 styles/
│   │       └── 📄 index.css            # Global styles + Tailwind
│   │
│   ├── 📄 index.html                   # HTML entry point
│   ├── 📄 .env.example                 # Environment template
│   ├── 📄 package.json                 # Node dependencies
│   ├── 📄 vite.config.js               # Vite configuration
│   ├── 📄 tailwind.config.js           # Tailwind configuration
│   └── 📄 postcss.config.js            # PostCSS configuration
│
├── 📂 ml/                               # Machine Learning
│   ├── 📂 dataset/
│   │   └── 📄 transactions.csv         # Training data
│   │
│   ├── 📄 data_preparation.py          # Data loading & prep
│   ├── 📄 model_pipeline.py            # Training pipeline
│   ├── 📄 retrain_model.py             # Main training script
│   └── 📄 requirements.txt             # ML dependencies
│
├── 📄 README.md                         # Main documentation
├── 📄 QUICKSTART.md                     # Quick start guide
├── 📄 SETUP.md                          # Detailed setup
├── 📄 API_DOCUMENTATION.md              # API reference
├── 📄 CONTRIBUTING.md                   # Contribution guide
├── 📄 CHANGELOG.md                      # Version history
├── 📄 PROJECT_STRUCTURE.md              # This file
├── 📄 LICENSE                           # MIT License
├── 📄 .gitignore                        # Git ignore patterns
├── 📄 start_server.bat                  # Windows startup
└── 📄 start_server.sh                   # Linux/Mac startup
```

## 📋 File Purposes

### Backend Files

#### Core Files

**`backend/app/main.py`**
- FastAPI application initialization
- CORS middleware setup
- Router registration
- Health check endpoints

**`backend/run.py`**
- Uvicorn server configuration
- Development server startup
- Logging configuration

#### Routes

**`backend/app/routes/predict.py`**
- `POST /predict/manual` - Manual transaction prediction
- `POST /predict/sms` - SMS-based prediction
- Feature extraction and ML inference
- Database logging

**`backend/app/routes/logs.py`**
- `GET /logs` - Retrieve transaction history
- `GET /logs/stats` - Get statistics
- Filtering and pagination

#### Schemas

**`backend/app/schemas/transaction_schema.py`**
- `ManualTransactionInput` - Manual input validation
- `SMSInput` - SMS input validation
- `PredictionResponse` - API response format
- `TransactionLog` - Log entry format

#### Utils

**`backend/app/utils/text_parser.py`**
- SMS text parsing
- Pattern matching for amounts, dates, times
- Multiple bank format support
- Urgency keyword detection

**`backend/app/utils/preprocessor.py`**
- Feature engineering
- Time-based feature extraction
- Amount pattern analysis
- ML model loading and inference
- Rule-based fallback logic

#### Database

**`backend/app/db/models.py`**
- `TransactionLog` model definition
- Database schema

**`backend/app/db/connection.py`**
- Database connection setup
- Session management
- Automatic table creation

### Frontend Files

#### Core Files

**`frontend/src/main.jsx`**
- React app mounting
- Root component rendering

**`frontend/src/App.jsx`**
- Main application component
- Toast notification setup
- Router configuration

#### Pages

**`frontend/src/pages/Home.jsx`**
- Main dashboard layout
- Component orchestration
- State management for results

#### Components

**`frontend/src/components/ManualInputForm.jsx`**
- Manual input form UI
- Form validation
- API call for manual prediction
- Loading states

**`frontend/src/components/SMSInputForm.jsx`**
- SMS textarea UI
- Example SMS button
- API call for SMS prediction
- Loading states

**`frontend/src/components/ResultCard.jsx`**
- Prediction result display
- Risk level visualization
- Color-coded feedback
- Animated entrance

**`frontend/src/components/HistoryTable.jsx`**
- Transaction history table
- Filtering capabilities
- Refresh functionality
- Pagination

#### API

**`frontend/src/api/predict.js`**
- Axios client setup
- API endpoint functions
- Error handling
- Request/response formatting

#### Styles

**`frontend/src/styles/index.css`**
- Tailwind directives
- Custom CSS classes
- Glassmorphic styles
- Animations

### ML Files

**`ml/dataset/transactions.csv`**
- Training dataset
- Fraud and legitimate samples
- Feature columns

**`ml/data_preparation.py`**
- Data loading
- Train/test split
- Feature scaling
- Data validation

**`ml/model_pipeline.py`**
- Model training functions
- Multiple algorithms (GB, RF, LR)
- Model evaluation
- Cross-validation
- Model persistence

**`ml/retrain_model.py`**
- Complete training pipeline
- Model comparison
- Best model selection
- Feature importance analysis
- Model deployment

### Configuration Files

**`backend/.env.example` / `frontend/.env.example`**
- Environment variable templates
- Configuration examples

**`frontend/vite.config.js`**
- Vite build configuration
- Development server setup
- Proxy configuration

**`frontend/tailwind.config.js`**
- Tailwind CSS customization
- Custom colors
- Custom animations
- Theme extensions

**`frontend/postcss.config.js`**
- PostCSS configuration
- Tailwind and Autoprefixer setup

### Documentation Files

**`README.md`**
- Project overview
- Feature list
- Setup instructions
- Usage guide
- Architecture explanation

**`QUICKSTART.md`**
- Fastest way to get started
- Minimal instructions
- Quick test cases

**`SETUP.md`**
- Detailed setup guide
- Step-by-step instructions
- Troubleshooting
- Platform-specific guides

**`API_DOCUMENTATION.md`**
- Complete API reference
- Endpoint documentation
- Request/response examples
- Integration guides

**`CONTRIBUTING.md`**
- Contribution guidelines
- Development workflow
- Coding standards
- PR process

**`CHANGELOG.md`**
- Version history
- Release notes
- Breaking changes

**`PROJECT_STRUCTURE.md`**
- This file
- Directory organization
- File purposes

### Utility Files

**`start_server.bat` (Windows)**
- Automated setup and startup
- Virtual environment creation
- Dependency installation
- Model training
- Server startup

**`start_server.sh` (Linux/Mac)**
- Same as above for Unix systems

**`.gitignore`**
- Git ignore patterns
- Excludes generated files
- Protects sensitive data

**`LICENSE`**
- MIT License
- Usage terms

## 🎯 Key Directories

### `/backend/app/`
Core backend application code. All business logic, API endpoints, and database interactions.

### `/frontend/src/`
React application source code. All UI components, styling, and client-side logic.

### `/ml/`
Machine learning pipeline. Training scripts, datasets, and model artifacts.

## 🔄 Data Flow

```
User Input (Frontend)
    ↓
API Request (frontend/src/api/predict.js)
    ↓
FastAPI Route (backend/app/routes/predict.py)
    ↓
Feature Extraction (backend/app/utils/preprocessor.py)
    ↓
ML Model Inference (backend/app/models/fraud_model.pkl)
    ↓
Database Logging (backend/app/db/)
    ↓
API Response
    ↓
Result Display (frontend/src/components/ResultCard.jsx)
```

## 🗄️ Database Schema

```sql
CREATE TABLE transaction_logs (
    id INTEGER PRIMARY KEY,
    account VARCHAR(255),
    amount FLOAT NOT NULL,
    receiver VARCHAR(255),
    date VARCHAR(50),
    time VARCHAR(50),
    raw_text TEXT,
    prediction VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL
);
```

## 📦 Dependencies Overview

### Backend (Python)
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **SQLAlchemy**: Database ORM
- **scikit-learn**: ML algorithms
- **NumPy**: Numerical operations

### Frontend (JavaScript)
- **React**: UI framework
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **Framer Motion**: Animations
- **Axios**: HTTP client
- **Lucide React**: Icons

### ML (Python)
- **pandas**: Data manipulation
- **scikit-learn**: ML algorithms
- **NumPy**: Numerical operations
- **joblib**: Model serialization

## 🚀 Build Artifacts

Generated during setup/runtime:

```
backend/venv/           # Python virtual environment
backend/fraud_detection.db  # SQLite database
backend/app/models/fraud_model.pkl  # Trained ML model
frontend/node_modules/  # Node dependencies
frontend/dist/          # Production build
```

## 🎨 Architecture Patterns

### Backend
- **MVC Pattern**: Models, Views (routes), Controllers (utils)
- **Repository Pattern**: Database abstraction
- **Dependency Injection**: FastAPI's dependency system
- **Factory Pattern**: Model loading

### Frontend
- **Component-Based**: Reusable React components
- **Container/Presentational**: Smart vs. dumb components
- **Hooks Pattern**: State management with React hooks
- **API Layer**: Separated API calls

### ML
- **Pipeline Pattern**: Sequential data processing
- **Strategy Pattern**: Multiple model algorithms
- **Factory Pattern**: Model selection

## 📈 Scalability Considerations

**Current Structure Supports:**
- ✅ Microservices separation (backend/frontend)
- ✅ Database migrations
- ✅ Model versioning
- ✅ Environment-based configuration
- ✅ Horizontal scaling ready

**Easy to Add:**
- Authentication layer
- Caching layer (Redis)
- Message queue (Celery)
- Monitoring (Prometheus)
- Logging aggregation

---

**This structure follows best practices for full-stack ML applications! 🏗️**

