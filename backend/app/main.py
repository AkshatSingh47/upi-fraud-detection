from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import predict, logs, auth

app = FastAPI(
    title="UPI Fraud Detection API",
    description="AI-Driven Transaction Risk Intelligence System",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(logs.router)

@app.get("/")
def root():
    return {
        "message": "UPI Fraud Detection API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "UPI Fraud Detection"}

