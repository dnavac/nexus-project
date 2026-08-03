import os
import time
from dotenv import load_dotenv
import chromadb
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# 1. Cargar la API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY o GOOGLE_API_KEY no configurada en .env")

print("🔍 Buscando documentos...")
# 2. Cargar los .txt desde la carpeta que creaste afuera
# Como estamos en /ai, usamos ../rag_documents para subir un nivel
loader = DirectoryLoader("../rag_documents", glob="**/*.txt", loader_cls=TextLoader,loader_kwargs={"encoding":"utf-8"})
documents = loader.load()
print(f"✅ Se encontraron {len(documents)} documentos.")

# 3. Dividir los textos en "chunks" (pedazos más pequeños para que la IA los procese mejor)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)
print(f"Se dividieron en {len(chunks)} chunks de texto.")

# 4. Inicializar Embeddings de Google (Convierte el texto a coordenadas matemáticas)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", 
    google_api_key=api_key
)

# 5. Conectarse a ChromaDB y guardar
print("Guardando vectores en ChromaDB (puerto 8000)...")
chroma_host = os.getenv("CHROMA_HOST", "localhost")
chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)

vector_store = Chroma(
    client=chroma_client,
    collection_name="nexus_knowledge",
    embedding_function=embeddings,
)

batch_size = 80 # Enviamos 80 a la vez para mantenernos debajo del límite de 100
for i in range(0, len(chunks), batch_size):
    batch = chunks[i : i + batch_size]
    print(f"Procesando lote {i} a {i + len(batch)} de {len(chunks)}...")
    vector_store.add_documents(documents=batch)
    
    # Pausamos 60 segundos si aún quedan documentos por procesar
    if i + batch_size < len(chunks):
        print("Esperando 60 segundos para respetar el límite de la API...")
        time.sleep(60)

print("Ingesta completada. El RAG tiene la base de conocimiento lista.")
