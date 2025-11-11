import json
import uvicorn
import aio_pika
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .store import NLPFactory, VectorDBFactory
from .core import get_settings
from .routers import text, stt, tts

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
QUEUE_NAME = "db_export_queue"


@asynccontextmanager
async def lifespan(app: FastAPI):
    SETTINGS = get_settings()

    nlp_factory = NLPFactory(SETTINGS)
    nlp = nlp_factory.create("gemini")
    nlp.connect()
    app.state.nlp = nlp

    vectordb_factory = VectorDBFactory(SETTINGS)
    vectordb = vectordb_factory.create("qdrant")
    vectordb.connect()
    app.state.vectordb = vectordb

    app.state.rabbit_conn = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await app.state.rabbit_conn.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    async def process_message(message: aio_pika.IncomingMessage):
        async with message.process():
            data = json.loads(message.body.decode())
            print(data)

    await queue.consume(process_message, no_ack=False)

    yield

    await channel.close()
    await app.state.rabbit_conn.close()
    nlp.disconnect()
    vectordb.disconnect()


app = FastAPI(
    lifespan=lifespan,
    title="Syara",
    version="0.1.0",
    openapi_url="/openapi.json",
    root_path="/api/genai",
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


@app.get("/", tags=["Health"])
async def read_root():
    return {"status": "ok", "title": app.title, "version": app.version}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
