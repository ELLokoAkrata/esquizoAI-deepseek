from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import uuid
import json
import traceback

# Importar desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

try:
    from chat_client import DeepSeekClient
    from logger import ConversationLogger
    import config
    IMPORTS_OK = True
except ImportError as e:
    print(f"⚠️ Warning: No se pueden importar módulos de src/: {e}")
    print("💡 Asegúrate de tener instaladas las dependencias del proyecto principal")
    IMPORTS_OK = False

app = FastAPI()

# Permitir CORS para desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sesiones simples en memoria (puedes mejorar esto luego)
sessions = {}

# Almacén de loggers por sesión
session_loggers = {}

def get_or_create_logger(session_id: str, mode: str):
    """Obtiene o crea un logger para la sesión"""
    if session_id not in session_loggers:
        if IMPORTS_OK:
            # Crear logger con ruta específica al directorio logs del proyecto principal
            logger = ConversationLogger(mode_name=f"{mode.upper()}-WEB")
            # Asegurar que use la ruta correcta del directorio logs
            logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/logs'))
            os.makedirs(logs_dir, exist_ok=True)
            logger.logs_dir = os.path.dirname(logs_dir)  # Actualizar la ruta
            session_loggers[session_id] = logger
            print(f"📝 Logger creado para sesión {session_id[:8]}... modo {mode}")
            print(f"📁 Directorio logs: {logs_dir}")
        else:
            session_loggers[session_id] = None
    return session_loggers[session_id]

@app.post("/chat/stream")
async def chat_stream(request: Request):
    if not IMPORTS_OK:
        return JSONResponse(
            content={"error": "Backend no configurado. Instala dependencias del proyecto principal."},
            status_code=500
        )
    
    try:
        data = await request.json()
        message = data.get("message", "")
        mode = data.get("mode", "esquizo")
        model_type = data.get("model_type", "chat")
        session_id = data.get("session_id")

        # Validar parámetros
        if not message.strip():
            return JSONResponse(content={"error": "Mensaje vacío"}, status_code=400)
            
        valid_modes = ["esquizo", "nethacker", "mirror", "oracle"]
        if mode not in valid_modes:
            return JSONResponse(content={"error": f"Modo inválido. Usar: {valid_modes}"}, status_code=400)

        if not session_id or session_id not in sessions:
            session_id = str(uuid.uuid4())
            # Obtener o crear logger para nueva sesión
            logger = get_or_create_logger(session_id, mode)
        
        # Obtener logger para todas las sesiones (nuevo o existente) 
        logger = get_or_create_logger(session_id, mode)
        
        # Registrar mensaje del usuario
        if logger:
            logger.log_message("user", message)
            print(f"🆕 Nueva sesión creada: {session_id}")
            try:
                client = DeepSeekClient(mode=mode, model_type=model_type)
                sessions[session_id] = client
                print(f"📝 Contexto inicial: {len(client.messages)} mensajes")
            except Exception as e:
                return JSONResponse(
                    content={"error": f"Error inicializando cliente: {str(e)}"},
                    status_code=500
                )
        else:
            client = sessions[session_id]
            print(f"♻️  Sesión existente: {session_id} con {len(client.messages)} mensajes en historial")

        def event_stream():
            accumulated_response = ""  # Para acumular la respuesta completa
            try:
                # Enviar session_id como primer mensaje
                session_data = {"session_id": session_id, "content": "", "reasoning": ""}
                yield f"data: {json.dumps(session_data, ensure_ascii=False)}\n\n"
                
                for chunk in client.send_message(message):
                    # Acumular respuesta para logging
                    if chunk.get("content"):
                        accumulated_response += chunk.get("content", "")
                    
                    # Asegurar formato JSON válido
                    chunk_data = {
                        "content": chunk.get("content", ""),
                        "reasoning": chunk.get("reasoning", ""),
                        "session_id": session_id
                    }
                    yield f"data: {json.dumps(chunk_data, ensure_ascii=False)}\n\n"
                
                # Al final del streaming, loggear la respuesta completa
                if logger and accumulated_response.strip():
                    logger.log_message("assistant", accumulated_response.strip())
                    
            except Exception as e:
                error_data = {"error": str(e), "traceback": traceback.format_exc()}
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"

        return StreamingResponse(
            event_stream(), 
            media_type="text/event-stream"
        )
        
    except Exception as e:
        return JSONResponse(
            content={"error": f"Error procesando request: {str(e)}"},
            status_code=500
        )

@app.post("/chat/reset")
async def reset_context(request: Request):
    data = await request.json()
    session_id = data.get("session_id")
    if session_id and session_id in sessions:
        sessions[session_id].clear_context()
        return {"success": True}
    return {"success": False, "error": "Sesión no encontrada"}

@app.get("/")
def root():
    return {
        "status": "ok", 
        "message": "EsquizoAI-DeepSeek backend running",
        "imports_ok": IMPORTS_OK,
        "sessions_active": len(sessions),
        "endpoints": ["/chat/stream", "/chat/reset", "/health"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "imports": IMPORTS_OK,
        "dependencies": {
            "src_modules": IMPORTS_OK,
            "active_sessions": len(sessions)
        }
    }
