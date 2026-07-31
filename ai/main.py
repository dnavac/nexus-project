from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers.chat import router as chat_router
from routers.predict import router as predict_router

load_dotenv()

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