# 🚀 Setup Guide - UPI Fraud Detection

Complete step-by-step setup instructions for the UPI Fraud Detection system.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.9 or higher**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version` or `python3 --version`

2. **Node.js 16 or higher**
   - Download: https://nodejs.org/
   - Verify: `node --version`

3. **pip** (Python package installer)
   - Usually comes with Python
   - Verify: `pip --version`

4. **npm** (Node package manager)
   - Comes with Node.js
   - Verify: `npm --version`

### Optional (for Production)

- PostgreSQL 13+ (for production database)
- Git (for version control)

## 🎯 Quick Setup (Automated)

### Windows Users

1. **Open Command Prompt or PowerShell**
2. **Navigate to project directory**
   ```cmd
   cd path\to\upi-fraud-detection
   ```

3. **Run the startup script**
   ```cmd
   start_server.bat
   ```

This will automatically:
- Create Python virtual environment
- Install all backend dependencies
- Train the ML model
- Install all frontend dependencies
- Start both servers

### Linux/Mac Users

1. **Open Terminal**
2. **Navigate to project directory**
   ```bash
   cd path/to/upi-fraud-detection
   ```

3. **Make script executable and run**
   ```bash
   chmod +x start_server.sh
   ./start_server.sh
   ```

## 🔧 Manual Setup (Step-by-Step)

If you prefer manual control or the automated script doesn't work:

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# You should see (venv) in your terminal prompt
```

### Step 2: Configure Environment

```bash
# Copy example env file
# On Windows:
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env

# On Linux/Mac:
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit .env files if needed (optional for local development)
```

### Step 3: Train ML Model

```bash
# Navigate to ml directory
cd ml

# Activate backend virtual environment if not already active
# Windows: ..\backend\venv\Scripts\activate
# Linux/Mac: source ../backend/venv/bin/activate

# Run training script
python retrain_model.py

# You should see training progress and model evaluation results
# Model will be saved to: backend/app/models/fraud_model.pkl
```

Expected output:
```
====================================
🚀 UPI FRAUD DETECTION - ML TRAINING PIPELINE
====================================

📁 Step 1: Loading and preparing data...
Dataset shape: (50, 5)
...
✅ TRAINING COMPLETE!
🎯 Model ready for deployment
```

### Step 4: Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment if not already active
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Run the server
python run.py

# Server will start on http://localhost:8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Keep this terminal open!**

### Step 5: Frontend Setup

Open a **NEW** terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# This may take a few minutes...
```

### Step 6: Start Frontend Server

```bash
# Still in frontend directory
npm run dev

# Server will start on http://localhost:3000
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Keep this terminal open too!**

## ✅ Verification

### Check Backend

1. Open browser: http://localhost:8000
2. You should see:
   ```json
   {
     "message": "UPI Fraud Detection API",
     "status": "active",
     "version": "1.0.0"
   }
   ```

3. Check API docs: http://localhost:8000/docs
4. You should see interactive API documentation

### Check Frontend

1. Open browser: http://localhost:3000
2. You should see the beautiful UI with:
   - Header with "UPI Fraud Detection"
   - Two input forms (Manual Input and SMS Paste)
   - Stats cards
   - Animated elements

### Test the System

1. **Try Manual Input:**
   - Account: `user@paytm`
   - Amount: `5000`
   - Receiver: `merchant@upi`
   - Date: Today's date
   - Time: `23:45` (late night - should trigger high risk)
   - Click "Detect Fraud"

2. **Try SMS Input:**
   - Click "Use Example SMS"
   - Click "Detect Fraud"

3. **Check Results:**
   - Result card should appear with prediction
   - Transaction should appear in History Table

## 🐛 Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError"**
```bash
# Make sure virtual environment is activated
# You should see (venv) in terminal

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Error: "Address already in use"**
```bash
# Port 8000 is in use. Kill the process:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

**Error: "Model not found"**
```bash
# Train the model
cd ml
python retrain_model.py
```

### Frontend Issues

**Error: "Cannot find module"**
```bash
# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 3000 already in use"**
```bash
# Port is in use. Kill the process:
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:3000 | xargs kill -9
```

**Blank page or errors in browser console**
```bash
# Check backend is running
# Open http://localhost:8000

# Check frontend .env file
# Make sure VITE_API_URL=http://localhost:8000

# Restart frontend
npm run dev
```

### Database Issues

**Error: "Database locked"**
```bash
# Close all terminals accessing the database
# Delete database file
rm backend/fraud_detection.db
# Restart backend - new DB will be created
```

### ML Model Issues

**Error: "Model training failed"**
```bash
# Check Python version (need 3.9+)
python --version

# Install ML dependencies
pip install numpy pandas scikit-learn joblib

# Try training again
cd ml
python retrain_model.py
```

## 🔒 Security Setup (Production)

### Environment Variables

Create `.env` files with secure values:

**backend/.env**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/fraud_db
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://yourdomain.com
```

**frontend/.env**
```env
VITE_API_URL=https://api.yourdomain.com
```

### PostgreSQL Setup

```bash
# Install PostgreSQL
# Create database
createdb upi_fraud_db

# Update backend/.env
DATABASE_URL=postgresql://username:password@localhost:5432/upi_fraud_db
```

## 📊 Directory Structure After Setup

```
upi-fraud-detection/
├── backend/
│   ├── venv/                    ✓ Virtual environment
│   ├── app/
│   │   └── models/
│   │       └── fraud_model.pkl  ✓ Trained model
│   ├── .env                     ✓ Environment config
│   └── fraud_detection.db       ✓ SQLite database
│
├── frontend/
│   ├── node_modules/            ✓ Dependencies
│   └── .env                     ✓ Environment config
│
└── ml/
    └── dataset/
        └── transactions.csv     ✓ Training data
```

## 🎉 Success!

If everything is working:
- ✅ Backend runs on http://localhost:8000
- ✅ Frontend runs on http://localhost:3000
- ✅ Model is trained and loaded
- ✅ Database is connected
- ✅ You can make predictions

## 📚 Next Steps

1. **Read the main README.md** for detailed documentation
2. **Explore the API** at http://localhost:8000/docs
3. **Try different transactions** to test fraud detection
4. **Check the code** to understand the architecture
5. **Customize** for your specific needs

## 💡 Tips

- Keep both terminal windows open while using the app
- Check browser console (F12) for frontend errors
- Check terminal for backend errors
- Use the example SMS to test quickly
- Try different times (late night = higher risk)

## 🆘 Still Having Issues?

1. Make sure all prerequisites are installed
2. Check all terminals for error messages
3. Verify ports 3000 and 8000 are available
4. Try restarting from Step 1
5. Check the troubleshooting section above

---

**Happy Fraud Detecting! 🛡️**

