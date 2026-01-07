from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.presentation.auth_routes import router as auth_router
from src.presentation.session_routes import router as session_router
from src.infrastructure.database.connection import init_db

app = FastAPI(title="Focus AI", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(session_router, prefix="/api/sessions", tags=["sessions"])

@app.get("/")
async def root():
    return {"message": "Focus AI API"}

@app.get("/health")
async def health():
    return {"status": "ok"}