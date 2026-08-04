import os
import base64
import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File
from langchain_google_genai import ChatGoogleGenerativeAI

router = APIRouter()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Falta GEMINI_API_KEY o GOOGLE_API_KEY en las variables de entorno")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, google_api_key=api_key)

N8N_WEBHOOK_URL = "https://matrilaterally-varicelloid-cordie.ngrok-free.dev/webhook-test/upload-documents"

@router.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    try:
        content   = await file.read()
        mime_type = file.content_type

        if "pdf" in mime_type:
            doc_type = "pdf"
        elif "image" in mime_type:
            doc_type = "image"
        else:
            raise HTTPException(status_code=400, detail="Formato no soportado. Solo PDF o Imágenes.")

        base64_content = base64.b64encode(content).decode("utf-8")

        payload = {
            "filename":    file.filename,
            "mime_type":   mime_type,
            "doc_type":    doc_type,
            "file_base64": base64_content,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(N8N_WEBHOOK_URL, json=payload)
            response.raise_for_status()
            n8n_data       = response.json()
            extracted_text = n8n_data.get("extracted_text", "")

        if not extracted_text:
            raise HTTPException(status_code=500, detail="n8n no devolvió 'extracted_text'.")

        prompt = (
            "Eres un analista de la inmobiliaria NEXUS. Analiza el siguiente documento "
            "e identifica la información clave (nombres, cédula, valores, direcciones, etc.). "
            "Devuelve un resumen estructurado indicando si es válido para un trámite de arriendo o compra.\n\n"
            f"Contenido del documento:\n{extracted_text}\n\nAnálisis estructurado:"
        )
        ai_response = llm.invoke(prompt)

        return {"status": "success", "doc_type": doc_type, "analysis": ai_response.content}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Error comunicándose con n8n: {str(e)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
