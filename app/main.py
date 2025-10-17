from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from app.api import ingest, query
from app.core.embeddings import get_model

app = FastAPI(title="Knowledge-base Search Engine")

# CORS configuration (allow all for demo; tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Preload embedding model on startup to reduce first-request latency
@app.on_event("startup")
def preload_models():
    get_model()

app.include_router(ingest.router)
app.include_router(query.router)

# Mount static UI at /ui
app.mount("/ui", StaticFiles(directory="app/static", html=True), name="static")

@app.get("/")
def home():
    return {"message": "Welcome to the Knowledge-base Search Engine API"}
