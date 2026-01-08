from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import Response
from fastapi.openapi.utils import get_openapi
from src.presentation.auth_routes import router as auth_router
from src.presentation.session_routes import router as session_router
from src.presentation.api_key_routes import router as api_key_router
from src.presentation.api_gateway.public_routes import router as public_api_router
from src.presentation.analytics_routes import router as analytics_router
from src.presentation.feedback_routes import router as feedback_router
from src.presentation.notification_routes import router as notification_router
from src.presentation.user_settings_routes import router as user_settings_router
from src.infrastructure.database.connection import init_db
from src.infrastructure.identity import PRODUCT_NAME, API_HEADER_POWERED_BY, API_HEADER_VERSION
from src.infrastructure.monitoring.metrics_service import MetricsService

app = FastAPI(
    title=PRODUCT_NAME,
    version=API_HEADER_VERSION,
    description="Developer LLM & Code Assistant",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.middleware("http")
async def add_cerberus_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Powered-By"] = API_HEADER_POWERED_BY
    response.headers["X-Version"] = API_HEADER_VERSION
    return response

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
app.include_router(api_key_router, prefix="/api/keys", tags=["api-keys"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["analytics"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["feedback"])
app.include_router(notification_router, prefix="/api/notifications", tags=["notifications"])
app.include_router(user_settings_router, prefix="/api/user", tags=["user"])
app.include_router(public_api_router, prefix="/v1", tags=["public-api"])

@app.get("/")
async def root():
    return {
        "name": PRODUCT_NAME,
        "version": API_HEADER_VERSION,
        "description": "Developer LLM & Code Assistant"
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=MetricsService.get_metrics(),
        media_type=MetricsService.get_content_type()
    )

@app.get("/health")
async def health():
    return {"status": "ok"}