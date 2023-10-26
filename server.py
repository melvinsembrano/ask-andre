from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from transformers import pipeline
import asyncio
import json


async def homepage(request):
    payload = await request.body()
    jsonString = payload.decode("utf-8")
    jsonData = json.loads(jsonString)

    if "question" not in jsonData:
        return JSONResponse({"error": "question parameter not found"})

    if "context" not in jsonData:
        return JSONResponse({"error": "context parameter not found"})

    response_q = asyncio.Queue()
    await request.app.model_queue.put((jsonData, response_q))
    output = await response_q.get()
    return JSONResponse(output)


async def server_loop(q):
    pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")
    while True:
        (jsonData, response_q) = await q.get()
        out = pipe(question=jsonData["question"], context=jsonData["context"])
        await response_q.put(out)


app = Starlette(
    routes=[
        Route("/", homepage, methods=["POST"]),
    ],
)


@app.on_event("startup")
async def startup_event():
    q = asyncio.Queue()
    app.model_queue = q
    asyncio.create_task(server_loop(q))
