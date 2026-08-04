"""Sincronización incremental de Laravel hacia ChromaDB."""
import os
from enum import Enum

import chromadb
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ingest_db_to_chroma import TABLE_MAP, LangChainEmbeddingAdapter

router = APIRouter()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

embedding_fn = LangChainEmbeddingAdapter(key=api_key)
client = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "chroma"),
    port=int(os.getenv("CHROMA_PORT", "8000")),
)
collection = client.get_or_create_collection(
    name="nexus_knowledge", embedding_function=embedding_fn
)


class TableName(str, Enum):
    properties = "properties"
    agents = "agents"
    leads = "leads"
    transactions = "transactions"


class SyncPayload(BaseModel):
    table: TableName
    event: str
    row: dict


@router.post("/sync")
def sync_document(payload: SyncPayload):
    row_id = payload.row.get("id")
    if row_id is None:
        raise HTTPException(status_code=400, detail="La fila debe incluir id")

    prefix = {
        "properties": "property", "agents": "agent",
        "leads": "lead", "transactions": "transaction",
    }[payload.table.value]
    document_id = f"{prefix}_{row_id}"

    if payload.event == "deleted":
        collection.delete(ids=[document_id])
        return {"status": "deleted", "id": document_id}
    if payload.event not in {"created", "updated"}:
        raise HTTPException(status_code=400, detail="Evento inválido")

    _, text, metadata = TABLE_MAP[payload.table.value](payload.row)
    collection.upsert(ids=[document_id], documents=[text], metadatas=[metadata])
    return {"status": "synced", "id": document_id}
