"""
Script para probar cuál modelo de Gemini realmente funciona para generación de texto.
Ejecutar con: .\.venv\Scripts\python test_models.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
print(f"Usando API key: {api_key[:20]}...")

# Modelos candidatos a probar (en orden de preferencia)
CANDIDATES = [
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite-001",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-pro-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
]

print("\n=== Probando modelos para generación de texto ===\n")

working = []
for model_name in CANDIDATES:
    try:
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=api_key)
        response = llm.invoke("Di solo 'OK'")
        print(f"✅ {model_name} → FUNCIONA → '{response.content.strip()[:50]}'")
        working.append(model_name)
    except Exception as e:
        err = str(e)
        if "RESOURCE_EXHAUSTED" in err:
            print(f"⚠️  {model_name} → CUOTA AGOTADA (429)")
        elif "NOT_FOUND" in err:
            print(f"❌ {model_name} → NO DISPONIBLE PARA NUEVOS USUARIOS (404)")
        elif "INVALID_ARGUMENT" in err:
            print(f"🔸 {model_name} → ARGUMENTO INVÁLIDO")
        else:
            print(f"💥 {model_name} → ERROR: {err[:100]}")

print("\n=== RESUMEN ===")
if working:
    print(f"✅ Modelos funcionando: {working}")
    print(f"\n👉 Usa este en chat.py: model=\"{working[0]}\"")
else:
    print("❌ Ningún modelo funcionó. La cuota diaria de esta API key está agotada.")
    print("   Solución: genera una nueva API key en https://aistudio.google.com/apikey")
