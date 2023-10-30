# syntax = docker/dockerfile:1
FROM python:3.7-slim

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir tensorflow torch

WORKDIR /app
COPY requirements.txt ./
# RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN python3 -m pip install --no-cache-dir starlette transformers asyncio uvicorn

ENV PYTORCH_TRANSFORMERS_CACHE=/transformers_cache

# execute the command to download the model
# RUN python3 -c "from transformers import pipeline; print(pipeline('question-answering', model='deepset/roberta-base-squad2')(question='What is the name of the repository ?', context='Pipeline have been included in the huggingface/transformers repository'))"

COPY . .
CMD ["python3", "-m", "uvicorn", "--host", "0.0.0.0", "server:app"]
