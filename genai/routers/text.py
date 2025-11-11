from fastapi import APIRouter, Request
from pydantic import BaseModel
from ..agents import BestFitAgent

router = APIRouter()


class BestFitPayload(BaseModel):
    user_message: str


@router.post("/bestfit")
async def bestfit(request: Request, payload: BestFitPayload):
    nlp = request.app.state.nlp
    vectordb = request.app.state.vectordb
    agent = BestFitAgent(nlp, vectordb)
    response = agent.run(payload.user_message)
    return {"response": response}
