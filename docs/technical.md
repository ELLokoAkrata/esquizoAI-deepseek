# Documentación Técnica EsquizoAI 🤖

## Arquitectura del Sistema 🏗️

### Componentes Principales

#### 1. DeepSeekClient (`chat_client.py`)
```python
class DeepSeekClient:
    def __init__(self):
        # Inicialización con API key y configuración
        # Carga del system prompt desde rebel.json
    
    def send_message(self, message: str) -> str:
        # Envío de mensajes a la API
        # Manejo de streaming y respuestas
    
    def clear_context(self):
        # Limpieza de contexto manteniendo system prompt
```

#### 2. Configuración (`config.py`)
```python
# Variables de entorno y configuración
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-chat"
TEMPERATURE = 0.7
MAX_TOKENS = 1000
STREAM = True
```

#### 3. Interfaz Terminal (`app.py`)
```python
def main():
    # Loop principal de la aplicación
    # Manejo de input/output
    # Control de flujo y comandos
```

### Flujo de Datos

1. **Input del Usuario**
   - Captura de texto via terminal
   - Procesamiento de comandos especiales
   - Validación de input

2. **Procesamiento**
   - Envío a la API via DeepSeekClient
   - Streaming de respuestas
   - Manejo de errores

3. **Output**
   - Formateo de respuestas
   - Colores y estilos
   - Timestamps y formato

## Configuración y Setup 🛠️

### Requisitos
- Python 3.8+
- Dependencias:
  ```
  openai
  python-dotenv
  colorama
  ```

### Variables de Entorno
```env
DEEPSEEK_API_KEY=tu-api-key
BASE_URL=https://api.deepseek.com/v1
```

### System Prompt
```json
{
    "system_prompt": {
        "role": "system",
        "content": "..."
    }
}
```

## Características Técnicas 🔧

### Manejo de Memoria
- Historial limitado a 5 pares
- Limpieza automática
- Persistencia del system prompt

### Streaming
- Respuestas en tiempo real
- Buffer optimizado
- Control de flujo

### Manejo de Errores
- Try/catch en operaciones críticas
- Mensajes de error amigables
- Recuperación de fallos

## Comandos y Control 🎮

### Comandos Disponibles
- `q`: Salir del programa
- `c`: Limpiar chat y contexto

### Señales
- `KeyboardInterrupt`: Salida segura
- `Exception`: Manejo general de errores

## Personalización 🎨

### Colores
```python
Fore.LIGHTGREEN_EX  # Usuario
Fore.RED           # EsquizoAI
Fore.YELLOW        # Sistema
```

### Formatos
- Timestamps: `HH:MM`
- Emojis: 👤 🤖 💀
- ASCII Art Banner

## Optimizaciones 🚀

### Rendimiento
- Manejo eficiente de memoria
- Limpieza automática
- Streaming optimizado

### UX
- Respuestas instantáneas
- Feedback visual
- Comandos intuitivos 

### Manejo del Historial 📚

#### Estructura de Datos
El historial se maneja en dos niveles usando listas de diccionarios:

1. **Historial Local (`app.py`)**
```python
messages = []  # Lista de mensajes local

# Estructura de cada mensaje
{
    "role": str,      # "user" o "assistant"
    "content": str    # Contenido del mensaje
}

# Ejemplo de uso
messages.append({
    "role": "user",
    "content": user_input
})
```

2. **Historial del Cliente (`chat_client.py`)**
```python
class DeepSeekClient:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]
```

#### Características del Historial
- **Límite**: Mantiene los últimos 5 pares de conversación (10 mensajes)
- **Persistencia**: El system prompt siempre se mantiene en posición 0
- **Limpieza**: 
  - Comando `c` limpia ambos historiales
  - Se mantiene el system prompt en el cliente
  - Se reinicia la interfaz visual

#### Flujo de Datos del Historial
1. Usuario envía mensaje → Se añade a `messages` local
2. API responde → Se añade a `messages` local
3. Si se excede el límite → Se mantienen últimos 10
4. Al limpiar → Se reinician ambos historiales 