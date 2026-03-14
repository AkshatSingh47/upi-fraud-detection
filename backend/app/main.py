import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "UPI Fraud Detection"}

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
assets_dir = os.path.join(static_dir, "assets")

# Mount /assets specifically if it exists for performance
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Catch-all route to serve index.html for all non-API routes (React router)
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react_app(full_path: str):
    # Try to serve a static file first (like favicon.ico or explicit assets)
    file_path = os.path.join(static_dir, full_path)
    if full_path and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Fallback to index.html for React SPA handling
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
        
    return {
        "message": "UPI Fraud Detection API",
        "status": "active",
        "version": "1.0.0"
    }
