"""Carga inicial y sincronización batch de las tablas de Laravel hacia Chroma."""
import argparse
import json
import os
from typing import Callable

import chromadb
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "core", ".env"))

COLLECTION_NAME = "nexus_knowledge"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

# Wrapper simple para adaptar LangChain Embeddings a ChromaDB sin requerir paquetes externos antiguos
class LangChainEmbeddingAdapter:
    def __init__(self, key: str):
        self.lc_embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=key
        )
    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.lc_embeddings.embed_documents(input)
    def name(self) -> str:
        return "langchain_gemini_embedding"

embedding_fn = LangChainEmbeddingAdapter(key=GEMINI_API_KEY)
client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn,
)


def value(row: dict, key: str, default=""):
    return row.get(key, default) if row.get(key) is not None else default


def json_text(data) -> str:
    return json.dumps(data, ensure_ascii=False) if data is not None else ""


def property_to_doc(row: dict):
    text = (
        f"Propiedad #{row['id']}. Título: {value(row, 'title')}. "
        f"Descripción: {value(row, 'description')}. Zona: {value(row, 'zone')}. "
        f"Precio: {value(row, 'price')} COP. Administración: {value(row, 'administration_fee')} COP. "
        f"Área: {value(row, 'area_m2')} m2. Habitaciones: {value(row, 'bedrooms')}. "
        f"Baños: {value(row, 'bathrooms')}. Amenidades: {json_text(row.get('amenities'))}. "
        f"Estado: {value(row, 'status')}. Agente ID: {value(row, 'agent_id', 'sin asignar')}."
    )
    metadata = {
        "source": "properties", "category": "property", "record_id": int(row["id"]),
        "zone": str(value(row, "zone")), "status": str(value(row, "status")),
    }
    return f"property_{row['id']}", text, metadata


def agent_to_doc(row: dict):
    text = (
        f"Agente #{row['id']}: {value(row, 'name')}. Email: {value(row, 'email')}. "
        f"Teléfono: {value(row, 'phone')}. Zona: {value(row, 'zone')}. "
        f"Idiomas: {json_text(row.get('languages'))}. Horario: {value(row, 'working_hours')}. "
        f"Ventas del mes: {value(row, 'monthly_sales_count')}."
    )
    metadata = {
        "source": "agents", "category": "agent", "record_id": int(row["id"]),
        "zone": str(value(row, "zone")),
    }
    return f"agent_{row['id']}", text, metadata


def lead_to_doc(row: dict):
    text = (
        f"Lead #{row['id']}: {value(row, 'name')}. Email: {value(row, 'email')}. "
        f"Teléfono: {value(row, 'phone')}. Estado: {value(row, 'status')}. "
        f"Notas: {value(row, 'notes')}. Propiedad ID: {value(row, 'property_id')}. "
        f"Agente ID: {value(row, 'agent_id')}. Creado: {value(row, 'created_at')}."
    )
    metadata = {
        "source": "leads", "category": "lead", "record_id": int(row["id"]),
        "status": str(value(row, "status")),
    }
    return f"lead_{row['id']}", text, metadata


def transaction_to_doc(row: dict):
    text = (
        f"Transacción #{row['id']}: tipo {value(row, 'type')}. "
        f"Propiedad ID: {value(row, 'property_id')}. Agente ID: {value(row, 'agent_id')}. "
        f"Lead ID: {value(row, 'lead_id')}. Monto: {value(row, 'amount')} COP. "
        f"Fecha: {value(row, 'transaction_date')}."
    )
    metadata = {
        "source": "transactions", "category": "transaction", "record_id": int(row["id"]),
        "type": str(value(row, "type")),
    }
    return f"transaction_{row['id']}", text, metadata


TABLE_MAP: dict[str, Callable] = {
    "properties": property_to_doc,
    "agents": agent_to_doc,
    "leads": lead_to_doc,
    "transactions": transaction_to_doc,
}


def get_rows(table: str):
    if table not in TABLE_MAP:
        raise ValueError(f"Tabla no soportada: {table}")
    
    pg_config = {
        "host": os.getenv("DATABASE_HOST", os.getenv("DB_HOST", "db-postgres")),
        "port": int(os.getenv("DATABASE_PORT", os.getenv("DB_PORT", "5432"))),
        "dbname": os.getenv("DATABASE_NAME", os.getenv("DB_DATABASE", "nexus_db")),
        "user": os.getenv("DATABASE_USER", os.getenv("DB_USERNAME", "postgres")),
        "password": os.getenv("DATABASE_PASSWORD", os.getenv("DB_PASSWORD", "secret")),
    }
    
    with psycopg2.connect(**pg_config) as connection:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            return cursor.fetchall()


def sync_table(table: str):
    rows = get_rows(table)
    if not rows:
        print(f"[{table}] sin filas")
        return
    ids, documents, metadatas = zip(*(TABLE_MAP[table](dict(row)) for row in rows))
    collection.upsert(ids=list(ids), documents=list(documents), metadatas=list(metadatas))
    print(f"[{table}] {len(ids)} documentos sincronizados")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", choices=list(TABLE_MAP), help="Sincronizar una tabla")
    args = parser.parse_args()
    for table in ([args.table] if args.table else list(TABLE_MAP)):
        sync_table(table)
