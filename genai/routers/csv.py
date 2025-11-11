import pandas as pd
import asyncio
import json
from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from ..store import PromptFactory, BaseNLP
from ..core import TaskModelConfig

router = APIRouter()


def get_description_sync(nlp_instance: BaseNLP, prompt: str, car_features: str):
    contents = prompt.format(car_features=car_features)
    return nlp_instance.chat(
        TaskModelConfig.BESTFIT_DESCRIPE.value,
        "Arabic Descriptive Expirt",
        contents,
    )


async def description_generator(dataframe: pd.DataFrame, nlp: BaseNLP, prompt: str):
    yield '{"descriptions": ['
    first = True
    for row in dataframe.itertuples(index=True):
        car_features = ", ".join(f"{k}={v}" for k, v in row._asdict().items())
        response = await asyncio.to_thread(
            get_description_sync, nlp, prompt, car_features
        )
        result_data = {"row_index": row.Index, "description": response}
        if not first:
            yield ","
        yield json.dumps(result_data, ensure_ascii=False)
        first = False
    yield "]}"


@router.post("/csv-stream")
async def describe_csv_stream(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    nlp: BaseNLP = request.app.state.nlp
    prompt = PromptFactory().get_prompt("descripe")
    csv_bytes = await file.read()
    try:
        dataframe = await asyncio.to_thread(
            pd.read_csv, pd.io.common.BytesIO(csv_bytes)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")
    return StreamingResponse(
        description_generator(dataframe, nlp, prompt), media_type="application/json"
    )
