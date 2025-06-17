import os
from typing import List
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import requests

# === 環境變數 ===
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", 11434))
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "rag-collection"
VECTOR_DIM = 768

# === 初始化 Qdrant 客戶端 ===
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# 確保 Collection 存在
collections = qdrant.get_collections().collections
if COLLECTION_NAME not in [c.name for c in collections]:
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE)
    )

# === FastAPI 應用 ===
app = FastAPI()


# === 輸入模型 ===
class QueryRequest(BaseModel):
    query: str

class InsertRequest(BaseModel):
    text: str


# === 向 Ollama 請求文字嵌入向量 ===
def get_embedding(text: str) -> List[float]:
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Ollama embedding 失敗：{response.text}")
    return response.json()["embedding"]


# === 查詢向量資料庫並產生回應 ===
@app.post("/query")
def query(request: QueryRequest):
    embedding = get_embedding(request.query)

    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=1
    )

    if not hits:
        return {"response": "找不到相關內容", "context": ""}

    context = hits[0].payload.get("text", "")

    # 呼叫 LLM 回答問題（使用 llama3）
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": f"根據以下內容回答問題：\n{context}\n\n問題：{request.query}",
            "stream": False
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="呼叫 LLM 失敗")

    answer = response.json()["response"]
    return {"response": answer, "context": context}


# === 插入資料到向量資料庫 ===
@app.post("/insert")
def insert(request: InsertRequest):
    embedding = get_embedding(request.text)
    point = PointStruct(id=0, vector=embedding, payload={"text": request.text})
    qdrant.upsert(collection_name=COLLECTION_NAME, points=[point])
    return {"status": "ok"}
