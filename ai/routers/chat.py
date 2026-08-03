from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb import MongoDBChatMessageHistory
import chromadb
import os
import time

router = APIRouter()

# 1. Configuración Global 
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
chroma_host = os.getenv("CHROMA_HOST", "localhost")
chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
if not api_key:
    raise RuntimeError("Falta GEMINI_API_KEY o GOOGLE_API_KEY en las variables de entorno")


# Embeddings y Base Vectorial
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key)
chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
vector_store = Chroma(client=chroma_client, collection_name="nexus_knowledge", embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Modelo de Lenguaje (El cerebro)
# gemini-2.5-flash: confirmado disponible con esta API key (ver check_models.py)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, google_api_key=api_key)

# A) Prompt para reformular la pregunta. CRÍTICO: debe ser MUY BREVE para no superar
# el límite de tokens del modelo de embeddings (gemini-embedding-001 acepta ~100 tokens).
def get_session_history(session_id: str):
    return MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=mongo_uri,
        database_name="nexus_ai_db",
        collection_name="chat_histories",
    )

# 5. El Endpoint de la API
class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/conversational")
def chat_with_memory(request: ChatRequest):
    last_error = None
    for attempt in range(3):
        try:
            # 1. Obtener el historial de la base de datos
            history = get_session_history(request.session_id)
            messages = history.messages
            
            # 2. Determinar la pregunta a buscar en la base de datos
            search_query = request.message
            if len(messages) > 0:
                # Si hay historial, reformulamos la pregunta con el LLM
                hist_str = "\n".join([f"{'User' if m.type == 'human' else 'AI'}: {m.content}" for m in messages[-4:]])
                prompt = (
                    "Reformula la siguiente pregunta del usuario usando el historial de chat "
                    "en máximo 10 palabras para que sea independiente.\n\n"
                    f"Historial:\n{hist_str}\n\nPregunta: {request.message}\nReformula:"
                )
                res = llm.invoke(prompt)
                search_query = res.content.strip()
                print(f"Pregunta reformulada: '{search_query}'")
            
            # 3. Buscar en la base de datos vectorial (Chroma -> Embeddings)
            docs = retriever.invoke(search_query)
            context = "\n".join([d.page_content for d in docs])
            
            # 4. Generar la respuesta final con el LLM
            hist_str_full = "\n".join([f"{'User' if m.type == 'human' else 'AI'}: {m.content}" for m in messages[-6:]])
            final_prompt = (
                "Eres un agente inmobiliario de NEXUS. Responde a la pregunta del usuario basándote "
                "únicamente en el contexto proporcionado y en el historial de chat.\n\n"
                f"Contexto:\n{context}\n\nHistorial:\n{hist_str_full}\n\n"
                f"Usuario: {request.message}\nRespuesta:"
            )
            final_res = llm.invoke(final_prompt)
            
            # 5. Guardar en el historial
            history.add_user_message(request.message)
            history.add_ai_message(final_res.content)
            
            return {"response": final_res.content}
            
        except Exception as e:
            last_error = e
            error_str = str(e)
            if "500 INTERNAL" in error_str or "503" in error_str or "INTERNAL" in error_str:
                wait = 2 ** attempt
                print(f"Error transitorio Google (intento {attempt+1}/3). Esperando {wait}s...")
                import time
                time.sleep(wait)
                continue
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=error_str)
            
    raise HTTPException(status_code=503, detail=f"API de Google temporalmente no disponible. Error: {str(last_error)}")

