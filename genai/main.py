import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .store import NLPFactory, VectorDBFactory
from .core import get_settings
from .routers import text, stt, tts, csv


@asynccontextmanager
async def lifespan(app: FastAPI):
    SETTINGS = get_settings()

    nlp_factory = NLPFactory(SETTINGS)
    nlp = nlp_factory.create("gemini")
    nlp.connect()
    app.state.nlp = nlp

    vectordb_factory = VectorDBFactory(SETTINGS)
    vectordb = vectordb_factory.create("chroma")
    vectordb.connect()
    app.state.vectordb = vectordb

    yield

    nlp.disconnect()
    vectordb.disconnect()


app = FastAPI(
    lifespan=lifespan,
    title="Syara",
    version="0.1.0",
    openapi_url="/openapi.json",
    root_path="/api/ai",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text.router, prefix="/api/v1", tags=["Best Fit"])
app.include_router(stt.router, prefix="/api/v1", tags=["Speech-to-Text"])
app.include_router(tts.router, prefix="/api/v1", tags=["Text-to-Speech"])
app.include_router(csv.router, prefix="/api/v1", tags=["CSV"])


@app.get("/", tags=["Health"])
async def read_root():
    return {"status": "ok", "title": app.title, "version": app.version}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
