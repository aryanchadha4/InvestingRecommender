"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import setup_logging
from app.api.v1 import health, assets, signals, recommend, portfolio

setup_logging()

app = FastAPI(title="AI Investment Recommender", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["assets"])
app.include_router(signals.router, prefix="/api/v1/signals", tags=["signals"])
app.include_router(recommend.router, prefix="/api/v1/recommend", tags=["recommend"])
app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["portfolio"])


@app.on_event("startup")
async def startup_event() -> None:
    """Application startup event."""
    from loguru import logger
    from app.core.config import settings

    logger.info("Starting AI Investment Recommender API")
    logger.info(f"Environment: {settings.env}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Application shutdown event."""
    from loguru import logger

    logger.info("Shutting down AI Investment Recommender API")

