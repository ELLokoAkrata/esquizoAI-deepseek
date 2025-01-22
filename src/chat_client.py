import json
from openai import OpenAI
from typing import List, Dict, Optional
import config

class DeepSeekClient:
    def __init__(self):
        if not config.DEEPSEEK_API_KEY:
            raise ValueError("¡PSYCHO! Necesitas setear la variable de entorno DEEPSEEK_API_KEY")
        
        self.client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.BASE_URL
        )
        
        # Cargar el system prompt desde rebel.json
        with open(config.REBEL_JSON_PATH, 'r', encoding='utf-8') as f:
            rebel_config = json.load(f)
            self.system_prompt = rebel_config["system_prompt"]
        
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": json.dumps(self.system_prompt)}
        ]
    
    def send_message(self, message: str) -> Optional[str]:
        """Envía un mensaje al bot esquizo y retorna su respuesta."""
        try:
            self.messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=self.messages,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS,
                stream=config.STREAM
            )
            
            if config.STREAM:
                collected_messages = []
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        collected_messages.append(chunk.choices[0].delta.content)
                        yield chunk.choices[0].delta.content
                full_response = "".join(collected_messages)
            else:
                full_response = response.choices[0].message.content
                yield full_response
            
            self.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"¡ERROR PSYCHO! 💀 Algo salió mal: {str(e)}")
            return None
    
    def clear_context(self):
        """Limpia el contexto pero mantiene el system prompt."""
        self.messages = [self.messages[0]]  # Mantiene solo el system prompt 