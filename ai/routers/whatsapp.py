import os
import time
from fastapi import APIRouter, BackgroundTasks, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_mongodb import MongoDBChatMessageHistory
import chromadb

router = APIRouter()

# ── Configuración ───────────────────────────────────────────────────────────
api_key     = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
mongo_uri   = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
chroma_host = os.getenv("CHROMA_HOST", "localhost")
chroma_port = int(os.getenv("CHROMA_PORT", "8000"))

if not api_key:
    raise RuntimeError("Falta GEMINI_API_KEY o GOOGLE_API_KEY en las variables de entorno")

# ── Embeddings y Base Vectorial RAG ─────────────────────────────────────────
embeddings    = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key)
chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
vector_store  = Chroma(client=chroma_client, collection_name="nexus_knowledge", embedding_function=embeddings)
retriever     = vector_store.as_retriever(search_kwargs={"k": 3})

# ── Modelo de Lenguaje (max_retries=0 para evitar timeouts de Twilio) ───────
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, google_api_key=api_key, max_retries=0)

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_whatsapp_from = os.getenv("TWILIO_WHATSAPP_FROM")


def get_session_history(session_id: str) -> MongoDBChatMessageHistory:
    """Recupera o crea el historial de conversación en MongoDB."""
    return MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=mongo_uri,
        database_name="nexus_ai_db",
        collection_name="whatsapp_histories",
    )


def process_message(session_id: str, user_message: str) -> str:
    """Procesa el mensaje del usuario con RAG + Gemini o respuesta rápida."""
    try:
        context = ""
        # Buscar conocimiento general en ChromaDB.
        try:
            docs = retriever.invoke(user_message)
            context = "\n".join([d.page_content for d in docs])
        except Exception as e_chroma:
            print(f"[WhatsApp] Aviso ChromaDB: {e_chroma}", flush=True)

        if not context:
            context = "Inmobiliaria NEXUS: catálogo de apartamentos en Cartagena (Bocagrande, Manga, Castillogrande)."

        # 2. Llamar a Gemini.
        final_prompt = (
            "Eres el agente inmobiliario virtual de NEXUS en WhatsApp. "
            "Responde de forma muy amable, breve (máximo 2 párrafos) y profesional.\n\n"
            f"Contexto disponible:\n{context}\n\n"
            f"Usuario: {user_message}\nRespuesta:"
        )
        
        final_res = llm.invoke(final_prompt)
        reply_text = final_res.content

        # 3. Guardar en historial de MongoDB
        try:
            history = get_session_history(session_id)
            history.add_user_message(user_message)
            history.add_ai_message(reply_text)
        except Exception as e_mongo:
            print(f"[WhatsApp] Aviso MongoDB: {e_mongo}", flush=True)

        return reply_text

    except Exception as e:
        error_str = str(e)
        print(f"[WhatsApp Error]: {error_str}", flush=True)
        
        # Si la API de Google agotó cuota (429) o falló
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return (
                "¡Hola! 👋 Gracias por escribir a *Inmobiliaria NEXUS* 🏢.\n\n"
                "En este momento estamos experimentando un alto volumen de consultas. "
                "Un agente humano revisará tu mensaje muy pronto, o puedes reintentar en unos minutos. ¡Gracias por tu paciencia!"
            )
        
        return "¡Hola! Gracias por comunicarte con *Inmobiliaria NEXUS*. ¿En qué tipo de propiedad en Cartagena estás interesado?"


def send_whatsapp_reply(to_number: str, user_message: str, session_id: str) -> None:
    """Genera y envía la respuesta fuera de la petición del webhook."""
    if not all((twilio_account_sid, twilio_auth_token, twilio_whatsapp_from)):
        print(
            "[WhatsApp] Faltan TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN o "
            "TWILIO_WHATSAPP_FROM; no se puede enviar la respuesta.",
            flush=True,
        )
        return

    try:
        bot_reply = process_message(session_id, user_message)
        client = Client(twilio_account_sid, twilio_auth_token)
        message = client.messages.create(
            body=str(bot_reply),
            from_=twilio_whatsapp_from,
            to=to_number,
        )
        print(f"[WhatsApp] Respuesta enviada por Twilio: {message.sid}", flush=True)
    except Exception as e:
        print(f"[WhatsApp] Error enviando respuesta por Twilio: {e}", flush=True)


@router.post("/webhook")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint de Webhook que llama Twilio cuando llega un mensaje de WhatsApp.
    Responde INSTANTÁNEAMENTE en formato TwiML (XML).
    """
    try:
        form_data = await request.form()

        incoming_msg = form_data.get("Body", "").strip()
        from_number  = form_data.get("From", "")

        print(f"\n==================================================", flush=True)
        print(f"[WhatsApp Webhook] Mensaje recibido de: {from_number}", flush=True)
        print(f"[WhatsApp Webhook] Mensaje: '{incoming_msg}'", flush=True)
        print(f"==================================================\n", flush=True)

        if not incoming_msg:
            incoming_msg = "Hola"

        session_id = from_number.replace("whatsapp:", "").replace("+", "").replace(" ", "")
        if not session_id:
            session_id = "default_user"

        # Generar respuesta de forma rápida
        background_tasks.add_task(
            send_whatsapp_reply, from_number, incoming_msg, session_id
        )

        print("[WhatsApp Webhook] Respuesta delegada a tarea en segundo plano", flush=True)

        # Formatear respuesta XML TwiML para Twilio
        twiml_response = MessagingResponse()
        # No bloqueamos el webhook esperando a Gemini/Chroma.

        return Response(
            content="<Response></Response>",
            media_type="application/xml; charset=utf-8"
        )

    except Exception as e:
        print(f"[WhatsApp Webhook Critical Error]: {e}", flush=True)
        twiml_fallback = MessagingResponse()
        twiml_fallback.message("¡Hola! Gracias por escribir a Inmobiliaria NEXUS. ¿En qué podemos ayudarte?")
        return Response(
            content=str(twiml_fallback),
            media_type="application/xml; charset=utf-8"
        )


@router.get("/health")
def whatsapp_health():
    return {"status": "WhatsApp webhook listo."}
