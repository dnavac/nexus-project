from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
import os

router = APIRouter()

class ChatRequest(BaseModel):
    message: str


@router.post("/test")
async def test_gemini(request: ChatRequest):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GOOGLE_API_KEY no configurada")
        
        # Instanciamos el modelo de IA
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            verbose=True,
            temperature=0,
            google_api_key=api_key
        )

        # Generamos la respuesta
        response = model.invoke(request.message)
        
        return {"message": response.content}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))