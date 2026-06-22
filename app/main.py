from fastapi import FastAPI

from app.routers.notes import router as notes_router

app = FastAPI(title="Notes API", version="1.0.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(notes_router)
