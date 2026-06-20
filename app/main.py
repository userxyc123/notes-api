from fastapi import FastAPI

from app.routers.notes import router as notes_router

app = FastAPI(title="Notes API", version="1.0.0")

app.include_router(notes_router)
