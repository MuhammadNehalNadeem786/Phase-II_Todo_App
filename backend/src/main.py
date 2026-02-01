from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import tasks, auth, signup
from src.config import settings
from src.utils.logging import setup_logging
import uvicorn

# Set up logging
setup_logging()

app = FastAPI(
    title="Todo Backend API",
    description="RESTful API for managing user tasks with user-based data isolation",
    version="1.0.0"
)

# ✅ ADD CORS HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,  # Next.js frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(signup.router, prefix="/signup", tags=["signup"])

@app.get("/")
def read_root():
    return {"message": "Todo Backend API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
    
    
    