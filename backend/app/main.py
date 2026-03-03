from fastapi import FastAPI

from app.api.v1.router import router

app = FastAPI(title="Sheenly API")

app.include_router(router)
