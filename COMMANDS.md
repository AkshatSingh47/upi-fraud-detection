# ⚡ Quick Command Reference - UPI Fraud Detection

Essential commands for development and deployment.

## 🚀 Quick Start

### Windows
```cmd
start_server.bat
```

### Linux/Mac
```bash
chmod +x start_server.sh
./start_server.sh
```

---

## 🔧 Backend Commands

### Initial Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Run Server
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate
python run.py
```

### Run with Uvicorn Directly
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run in Background (Linux/Mac)
```bash
cd backend
nohup python run.py > backend.log 2>&1 &
```

### Check Logs
```bash
# If running in background
tail -f backend.log

# If running in terminal, logs show in console
```

### Stop Server
```bash
# If running in terminal: Ctrl+C

# If running in background (Linux/Mac):
ps aux | grep "python run.py"
kill <PID>

# Windows:
tasklist | findstr python
taskkill /PID <PID> /F
```

---

## 💻 Frontend Commands

### Initial Setup
```bash
cd frontend
npm install
```

### Development Server
```bash
cd frontend
npm run dev
```

### Build for Production
```bash
cd frontend
npm run build
```

### Preview Production Build
```bash
cd frontend
npm run preview
```

### Clean Install
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🧠 ML Commands

### Train Model
```bash
cd ml
python retrain_model.py
```

### Test Data Preparation
```bash
cd ml
python data_preparation.py
```

### Train Specific Model
```python
# In Python shell
from model_pipeline import train_gradient_boosting
from data_preparation import load_and_prepare_data

X_train, X_test, y_train, y_test, _ = load_and_prepare_data()
model = train_gradient_boosting(X_train, y_train)
```

---

## 🗄️ Database Commands

### SQLite (Default)

**View Database**
```bash
# Install sqlite3 if not available
sqlite3 backend/fraud_detection.db

# Common queries
.tables
SELECT * FROM transaction_logs LIMIT 10;
.quit
```

**Reset Database**
```bash
rm backend/fraud_detection.db
# Restart backend - new DB will be created
```

### PostgreSQL (Production)

**Create Database**
```bash
createdb upi_fraud_db
```

**Connect to Database**
```bash
psql upi_fraud_db
```

**Common Queries**
```sql
-- View all transactions
SELECT * FROM transaction_logs ORDER BY created_at DESC LIMIT 10;

-- Count fraud vs legit
SELECT prediction, COUNT(*) FROM transaction_logs GROUP BY prediction;

-- View high-risk transactions
SELECT * FROM transaction_logs WHERE risk_level IN ('High', 'Critical');

-- Get statistics
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN prediction = 'Fraud' THEN 1 ELSE 0 END) as fraud_count,
    AVG(confidence) as avg_confidence
FROM transaction_logs;
```

**Backup Database**
```bash
pg_dump upi_fraud_db > backup.sql
```

**Restore Database**
```bash
psql upi_fraud_db < backup.sql
```

---

## 🔍 Testing Commands

### Test API with cURL

**Health Check**
```bash
curl http://localhost:8000/health
```

**Manual Prediction**
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

**SMS Prediction**
```bash
curl -X POST "http://localhost:8000/predict/sms" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your UPI transaction of Rs.5000.00 to merchant@upi was successful."
  }'
```

**Get Logs**
```bash
curl "http://localhost:8000/logs?limit=10"
```

**Get Statistics**
```bash
curl "http://localhost:8000/logs/stats"
```

### Test API with HTTPie (if installed)

```bash
# Install HTTPie
pip install httpie

# Health check
http GET http://localhost:8000/health

# Manual prediction
http POST http://localhost:8000/predict/manual \
  account=user@paytm \
  amount:=5000 \
  receiver=merchant@upi \
  date=2025-11-12 \
  time=23:45
```

---

## 📦 Dependency Management

### Backend Dependencies

**Install**
```bash
cd backend
pip install -r requirements.txt
```

**Add New Package**
```bash
pip install package-name
pip freeze > requirements.txt
```

**Update All**
```bash
pip install -U -r requirements.txt
```

### Frontend Dependencies

**Install**
```bash
cd frontend
npm install
```

**Add New Package**
```bash
npm install package-name
```

**Update Package**
```bash
npm update package-name
```

**Check Outdated**
```bash
npm outdated
```

---

## 🐛 Debugging Commands

### Check Ports

**Windows**
```cmd
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

**Linux/Mac**
```bash
lsof -i :8000
lsof -i :3000
```

### Kill Port Process

**Windows**
```cmd
taskkill /PID <PID> /F
```

**Linux/Mac**
```bash
kill -9 <PID>
# or
lsof -ti:8000 | xargs kill -9
```

### Check Python Version
```bash
python --version
python3 --version
```

### Check Node Version
```bash
node --version
npm --version
```

### View Python Packages
```bash
pip list
pip show package-name
```

### View Node Packages
```bash
npm list
npm list package-name
```

---

## 🔐 Environment Setup

### Create Environment Files

**Backend**
```bash
cd backend
cp .env.example .env
# Edit .env with your settings
```

**Frontend**
```bash
cd frontend
cp .env.example .env
# Edit .env with your settings
```

### Load Environment Variables

**Backend (Python)**
```python
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL')
```

**Frontend (Vite)**
```javascript
const apiUrl = import.meta.env.VITE_API_URL
```

---

## 🚢 Production Deployment

### Backend Production

**With Gunicorn**
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**With systemd (Linux)**
```bash
# Create service file: /etc/systemd/system/upi-fraud-api.service
sudo systemctl start upi-fraud-api
sudo systemctl enable upi-fraud-api
sudo systemctl status upi-fraud-api
```

### Frontend Production

**Build**
```bash
cd frontend
npm run build
```

**Serve with Nginx**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

---

## 📊 Monitoring Commands

### Check System Resources

**CPU & Memory**
```bash
# Linux/Mac
top
htop

# Windows
taskmgr
```

### Check Disk Space
```bash
# Linux/Mac
df -h

# Windows
wmic logicaldisk get size,freespace,caption
```

### Check Network
```bash
# Test backend connection
curl http://localhost:8000/health

# Test with timing
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

---

## 🔄 Git Commands (Version Control)

### Initialize Repository
```bash
git init
git add .
git commit -m "Initial commit: UPI Fraud Detection System"
```

### Common Workflow
```bash
# Check status
git status

# Create feature branch
git checkout -b feature/new-feature

# Stage changes
git add .

# Commit
git commit -m "feat: Add new feature"

# Push
git push origin feature/new-feature
```

### Update from Remote
```bash
git pull origin main
```

---

## 📝 Logging Commands

### View Backend Logs
```bash
# If using run.py, logs show in terminal

# Redirect to file
python run.py > app.log 2>&1

# View log file
tail -f app.log
```

### View Frontend Logs
```bash
# Browser console (F12)
# Or in terminal where npm run dev is running
```

---

## 🧹 Cleanup Commands

### Clean Python Cache
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Clean Node Modules
```bash
cd frontend
rm -rf node_modules
```

### Clean Build Artifacts
```bash
# Frontend build
rm -rf frontend/dist

# Python builds
rm -rf backend/build backend/dist backend/*.egg-info
```

### Clean Database
```bash
rm backend/fraud_detection.db
```

### Full Clean (Start Fresh)
```bash
# Backend
rm -rf backend/venv backend/__pycache__ backend/**/__pycache__
rm backend/fraud_detection.db

# Frontend
rm -rf frontend/node_modules frontend/dist

# ML
rm backend/app/models/fraud_model.pkl
```

---

## 💡 Quick Tips

### Open API Docs
```bash
# Start backend, then visit:
http://localhost:8000/docs
```

### Run Both Servers Simultaneously

**Linux/Mac**
```bash
# Terminal 1
cd backend && source venv/bin/activate && python run.py

# Terminal 2
cd frontend && npm run dev
```

**Windows (PowerShell)**
```powershell
# Terminal 1
cd backend; .\venv\Scripts\activate; python run.py

# Terminal 2
cd frontend; npm run dev
```

### Quick API Test
```bash
# One-liner to test all endpoints
curl http://localhost:8000/health && \
curl http://localhost:8000/ && \
curl "http://localhost:8000/logs?limit=1"
```

---

## 📚 Documentation Commands

### View Documentation
```bash
# Open in browser
# README.md, SETUP.md, API_DOCUMENTATION.md, etc.
```

### Generate API Docs (Already automatic)
```bash
# FastAPI automatically generates docs at:
# /docs (Swagger UI)
# /redoc (ReDoc)
```

---

## 🎓 Learning Commands

### Interactive Python
```bash
cd backend
source venv/bin/activate
python

>>> from app.utils.preprocessor import extract_features
>>> features = extract_features(5000, "23:45", "merchant", "user@upi")
>>> print(features)
```

### Test SMS Parser
```bash
cd backend
python

>>> from app.utils.text_parser import parse_sms
>>> result = parse_sms("Your UPI transaction of Rs.5000...")
>>> print(result)
```

---

**Save this file for quick reference! 📋**

