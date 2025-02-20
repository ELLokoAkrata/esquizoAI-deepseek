import json
from openai import OpenAI
from typing import Generator, Dict, List
import config

class DeepSeekClient:
    def __init__(self, mode: str = "esquizo", model_type: str = "reasoner"):
        self.mode = mode
        self.model_type = model_type
        self.base_url = "https://api.deepseek.com" if model_type == "reasoner" else "https://api.deepseek.com/v1"
        
        self.client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=self.base_url
        )
        
        # Cargar configuración según el modo seleccionado
        config_path = config.MODES[mode]["config_path"]
        with open(config_path, 'r', encoding='utf-8') as f:
            self.system_config = json.load(f)
        
        self.messages = [{
            "role": "system",
            "content": json.dumps(self.system_config, ensure_ascii=False)
        }]
        
        welcome_messages = {
            "esquizo": "¡Psi-activación completa! ¿En qué dimensión necesitas ayuda?",
            "nethacker": "NetHacker-X inicializado. ¿Qué análisis de red necesitas realizar?"
        }
        
        if model_type == "chat":
            self.messages.append({
                "role": "assistant", 
                "content": welcome_messages[mode]
            })

    def _validate_message_sequence(self):
        """Valida la secuencia de mensajes para cada modelo"""
        if self.model_type == "reasoner" and len(self.messages) > 1:
            if self.messages[1]["role"] != "user":
                raise RuntimeError("Primer mensaje después del system debe ser user")
            
        for i in range(1, len(self.messages)):
            if self.messages[i]["role"] == self.messages[i-1]["role"]:
                raise RuntimeError(f"Secuencia inválida: {self.messages[i-1]} → {self.messages[i]}")

    def send_message(self, message: str) -> Generator[Dict[str, str], None, None]:
        try:
            # Limpiar mensajes huérfanos
            if self.messages[-1]["role"] == "user":
                self.messages.pop()
                
            self.messages.append({"role": "user", "content": message})
            self._validate_message_sequence()
            
            response = self.client.chat.completions.create(
                model="deepseek-reasoner" if self.model_type == "reasoner" else "deepseek-chat",
                messages=self.messages,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS,
                stream=config.STREAM
            )
            
            full_response = {"reasoning": "", "content": ""}
            
            for chunk in response:
                delta = chunk.choices[0].delta
                chunk_data = {
                    "content": delta.content if delta.content else "",
                    "reasoning": delta.reasoning_content if self.model_type == "reasoner" and delta.reasoning_content else ""
                }
                
                if any(chunk_data.values()):
                    yield chunk_data
                    full_response["reasoning"] += chunk_data["reasoning"]
                    full_response["content"] += chunk_data["content"]
            
            self.messages.append({
                "role": "assistant",
                "content": f"{full_response['reasoning']}\n{full_response['content']}".strip()
            })
            
        except Exception as e:
            raise RuntimeError(f"[ERROR] {str(e)}")

    def clear_context(self):
        """Reinicia contexto manteniendo compatibilidad con el modo actual"""
        self.messages = [{
            "role": "system",
            "content": json.dumps(self.system_config, ensure_ascii=False)
        }]
        
        welcome_messages = {
            "esquizo": "¡Conversación reiniciada! Pregunta lo que desees.",
            "nethacker": "Sesión reiniciada. Listo para nuevo análisis de red."
        }
        
        if self.model_type == "chat":
            self.messages.append({
                "role": "assistant",
                "content": welcome_messages[self.mode]
            })