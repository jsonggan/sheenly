from fastapi import APIRouter

from app.api.v1.inventory.router import router as inventory_router

router = APIRouter(prefix="/api/v1")
router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
