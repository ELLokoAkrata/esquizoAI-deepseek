import json
from openai import OpenAI
from typing import Generator, Dict, List, Optional
import config
import traceback
from meta_prompt import get_enhanced_system_prompt

class DeepSeekClient:
    def __init__(self, mode: str = "esquizo", model_type: str = "reasoner"):
        self.mode = mode
        self.model_type = model_type
        self.base_url = "https://api.deepseek.com"
        
        self.client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=self.base_url
        )
        
        # Cargar configuración original
        self.mode_config = config.MODES[mode]
        with open(self.mode_config["config_path"], 'r', encoding='utf-8') as f:
            original_config = json.load(f)
        
        # Solo usar meta_prompt para chat (que soporta functions)
        if model_type == "chat":
            enhanced_config = get_enhanced_system_prompt(original_config, mode)
        else:
            # Para reasoner, usar config original sin function calling
            enhanced_config = json.dumps(original_config, ensure_ascii=False, indent=2)
        
        self.messages = [{
            "role": "system",
            "content": enhanced_config
        }]
        
        welcome_messages = {
            "esquizo": "¡Psi-activación completa! ¿En qué dimensión necesitas ayuda?" + 
                      (" Puedo crear arte visionario también." if model_type == "chat" else ""),
            "nethacker": "NetHacker-X inicializado. ¿Qué análisis necesitas?" +
                        (" También puedo generar visualizaciones geométricas." if model_type == "chat" else ""),
            "mirror": "MirrorReflex listo. ¿Qué emociones deseas explorar?" +
                     (" Puedo crear arte para acompañar la introspección." if model_type == "chat" else ""),
            "oracle": "☯ PsychoOracle activado. ¿Qué misterios deseas consultar?" +
                     (" Puedo materializar visiones geométricas sagradas." if model_type == "chat" else "")
        }
        
        if model_type == "chat":
            self.messages.append({
                "role": "assistant", 
                "content": welcome_messages[mode]
            })

    def _execute_function_call(self, function_name: str, arguments: Dict) -> Dict:
        """Ejecuta function calls - SOLO para modelo chat"""
        if self.model_type != "chat":
            return {"error": "Function calling no disponible en reasoner"}
            
        try:
            if function_name == "create_visionary_art":
                try:
                    from visionary_art import create_visionary_art
                    result = create_visionary_art(**arguments)
                    return result
                except ImportError:
                    return {
                        "error": "Dependencias faltantes",
                        "message": "Ejecuta: pip install numpy matplotlib",
                        "success": False
                    }
                except Exception as e:
                    return {
                        "error": f"Error en generación de arte: {str(e)}",
                        "success": False
                    }
            else:
                return {"error": f"Función no reconocida: {function_name}"}
                
        except Exception as e:
            return {"error": f"Error ejecutando función: {str(e)}"}

    def _safe_get_content(self, delta, attr_name: str, default: str = "") -> str:
        """Obtiene contenido de manera segura manejando None"""
        try:
            value = getattr(delta, attr_name, None)
            return value if value is not None else default
        except:
            return default

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
            
            # 🔧 SEPARAR LÓGICA SEGÚN MODELO
            if self.model_type == "chat":
                # Chat: Con function calling
                
                try:
                    from visionary_art import VISIONARY_ART_TOOLS
                    tools = VISIONARY_ART_TOOLS
                except ImportError:
                    tools = None
                    
                yield from self._handle_chat_response(message, tools)
                
            else:
                # Reasoner: Sin function calling, solo reasoning
                yield from self._handle_reasoner_response(message)
                
        except Exception as e:
            error_msg = f"[ERROR] {str(e)}"
            print(f"Debug - Error completo: {traceback.format_exc()}")
            raise RuntimeError(error_msg)

    def _handle_chat_response(self, message: str, tools) -> Generator[Dict[str, str], None, None]:
        """Maneja respuesta del modelo chat con function calling"""
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            temperature=self.mode_config["temperature"],
            max_tokens=config.MAX_TOKENS,
            stream=config.STREAM,
            tools=tools
        )
        
        full_response = {"reasoning": "", "content": ""}
        accumulated_tool_calls = {}
        
        for chunk in response:
            delta = chunk.choices[0].delta
            
            # Contenido regular
            regular_content = self._safe_get_content(delta, 'content')
            if regular_content:
                yield {"content": regular_content, "reasoning": ""}
                full_response["content"] += regular_content
            
            # Function calls
            if hasattr(delta, 'tool_calls') and delta.tool_calls:
                for tool_call in delta.tool_calls:
                    if tool_call.index is not None:
                        idx = tool_call.index
                        
                        if idx not in accumulated_tool_calls:
                            accumulated_tool_calls[idx] = {
                                'function_name': '',
                                'arguments': '',
                                'complete': False
                            }
                        
                        if tool_call.function and tool_call.function.name:
                            accumulated_tool_calls[idx]['function_name'] += tool_call.function.name
                        
                        if tool_call.function and tool_call.function.arguments:
                            accumulated_tool_calls[idx]['arguments'] += tool_call.function.arguments
                        
                        if (accumulated_tool_calls[idx]['function_name'] and 
                            accumulated_tool_calls[idx]['arguments'] and
                            not accumulated_tool_calls[idx]['complete']):
                            
                            try:
                                args_str = accumulated_tool_calls[idx]['arguments']
                                args = json.loads(args_str) if args_str.strip() else {}
                                function_name = accumulated_tool_calls[idx]['function_name']
                                
                                result = self._execute_function_call(function_name, args)
                                
                                if result.get("success"):
                                    yield {
                                        "content": f"\n🎨 Arte creado: {result.get('filename', 'arte.png')}\n",
                                        "reasoning": ""
                                    }
                                else:
                                    yield {
                                        "content": f"\n⚠️ Error: {result.get('error', 'Error desconocido')}\n",
                                        "reasoning": ""
                                    }
                                
                                accumulated_tool_calls[idx]['complete'] = True
                                
                            except json.JSONDecodeError:
                                # Argumentos aún incompletos
                                pass
                            except Exception as e:
                                yield {
                                    "content": f"\n❌ Error: {str(e)}\n",
                                    "reasoning": ""
                                }
                                accumulated_tool_calls[idx]['complete'] = True
        
        # Agregar al historial
        response_content = full_response["content"].strip()
        self.messages.append({
            "role": "assistant",
            "content": response_content if response_content else "Respuesta procesada"
        })

    def _handle_reasoner_response(self, message: str) -> Generator[Dict[str, str], None, None]:
        """Maneja respuesta del modelo reasoner (sin function calling)"""
        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=self.messages,
            temperature=self.mode_config["temperature"],
            max_tokens=config.MAX_TOKENS,
            stream=config.STREAM
            # 🔧 SIN tools para reasoner
        )
        
        full_response = {"reasoning": "", "content": ""}
        
        for chunk in response:
            delta = chunk.choices[0].delta
            
            # 🔧 Manejo específico de reasoning para reasoner
            reasoning_content = ""
            # Probar diferentes atributos posibles
            for attr in ['reasoning_content', 'reasoning', 'thoughts']:
                reasoning_content = self._safe_get_content(delta, attr)
                if reasoning_content:
                    break
            
            if reasoning_content:
                yield {"content": "", "reasoning": reasoning_content}
                full_response["reasoning"] += reasoning_content
            
            # Contenido regular
            regular_content = self._safe_get_content(delta, 'content')
            if regular_content:
                yield {"content": regular_content, "reasoning": ""}
                full_response["content"] += regular_content
        
        # Agregar al historial
        response_content = f"{full_response['reasoning']}\n{full_response['content']}".strip()
        self.messages.append({
            "role": "assistant",
            "content": response_content if response_content else "Respuesta procesada"
        })

    def clear_context(self):
        """Reinicia contexto manteniendo compatibilidad con el modo actual"""
        with open(self.mode_config["config_path"], 'r', encoding='utf-8') as f:
            original_config = json.load(f)
        
        if self.model_type == "chat":
            enhanced_config = get_enhanced_system_prompt(original_config, self.mode)
        else:
            enhanced_config = json.dumps(original_config, ensure_ascii=False, indent=2)
        
        self.messages = [{
            "role": "system",
            "content": enhanced_config
        }]
        
        welcome_messages = {
            "esquizo": "¡Conversación reiniciada! Pregunta lo que desees.",
            "nethacker": "Sesión reiniciada. Listo para nuevo análisis de red.",
            "mirror": "Contexto reiniciado. Comencemos de nuevo la introspección.",
            "oracle": "Contexto reiniciado. Comencemos de nuevo la consulta oracular."
        }
        
        if self.model_type == "chat":
            self.messages.append({
                "role": "assistant",
                "content": welcome_messages[self.mode]
            })
