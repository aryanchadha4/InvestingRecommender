"""Asset endpoints - minimal CRUD."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_database
from app.db.models.asset import Asset

router = APIRouter()


@router.get("/")
async def list_assets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
) -> List[dict]:
    """List all assets."""
    stmt = select(Asset).offset(skip).limit(limit)
    result = db.execute(stmt)
    assets = result.scalars().all()
    return [
        {
            "id": a.id,
            "symbol": a.symbol,
            "name": a.name,
            "asset_class": a.asset_class,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in assets
    ]


@router.post("/")
async def create_asset(
    symbol: str,
    name: str,
    asset_class: str,
    db: Session = Depends(get_database),
) -> dict:
    """Create a new asset."""
    # Check if symbol already exists
    stmt = select(Asset).where(Asset.symbol == symbol)
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Asset with this symbol already exists")

    asset = Asset(symbol=symbol, name=name, asset_class=asset_class)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return {
        "id": asset.id,
        "symbol": asset.symbol,
        "name": asset.name,
        "asset_class": asset.asset_class,
        "created_at": asset.created_at.isoformat() if asset.created_at else None,
    }
