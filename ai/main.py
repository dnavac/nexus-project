from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

#cargar .env ANTES de importar los routers, 
load_dotenv()

from routers.chat import router as chat_router
from routers.predict import router as predict_router
from routers.analyze import router as analyze_router
from routers.whatsapp import router as whatsapp_router
from routers.rag_sync import router as rag_sync_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])

@app.get("")
def read_root():
    return{"message": "Motor de IA NEXUS en línea y listo."}

app.include_router(predict_router, prefix="/api/predict", tags=["Predictions"])
app.include_router(analyze_router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(whatsapp_router, prefix="/api/whatsapp", tags=["WhatsApp"])
app.include_router(rag_sync_router, prefix="/api/rag", tags=["RAG Sync"])
