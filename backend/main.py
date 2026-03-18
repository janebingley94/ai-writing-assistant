from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import init_db
from routers.generate import router as generate_router
from routers.history import router as history_router

app = FastAPI(title="AI Writing Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


app.include_router(generate_router)
app.include_router(history_router)
