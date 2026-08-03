import os
from dotenv import load_dotenv
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 1. Usamos el mismo modelo de embeddings que en la ingesta
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", 
    google_api_key=api_key
)

# 2. Conectarnos a tu ChromaDB local
print("🔌 Conectando a ChromaDB...")
chroma_client = chromadb.HttpClient(host="localhost", port=8000)

vector_store = Chroma(
    client=chroma_client,
    collection_name="nexus_knowledge",
    embedding_function=embeddings,
)

# 3. La pregunta de prueba (puedes cambiarla por lo que quieras)
pregunta = "¿Qué apartamentos tienes en Bocagrande?"
print(f"🔎 Buscando: '{pregunta}'\n")

# Hacemos la búsqueda por similitud. k=3 trae los 3 fragmentos más relevantes.
resultados = vector_store.similarity_search(pregunta, k=3)

for i, doc in enumerate(resultados):
    print(f"--- Resultado {i+1} ---")
    print(doc.page_content)
    print("----------------------\n")
