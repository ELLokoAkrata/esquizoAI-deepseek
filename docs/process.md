# Proceso de Desarrollo EsquizoAI 🤪

## Evolución del Proyecto 💀

### 1. Setup Inicial
- Instalación de dependencias básicas:
  ```bash
  pip install openai python-dotenv colorama
  ```
- Estructura de directorios:
  ```
  deepseek/
  ├── src/
  │   ├── __init__.py
  │   ├── app.py
  │   ├── chat_client.py
  │   ├── config.py
  │   ├── .env
  │   └── rebel.json
  └── docs/
      └── process.md
       └── technical.md
  ```

### 2. Desarrollo de Componentes

#### Chat Client
- Implementación de `DeepSeekClient` para manejar la comunicación con la API
- Sistema de streaming para respuestas en tiempo real
- Manejo de contexto y system prompt
- Control de errores y excepciones

#### Interfaz de Terminal
- Diseño de interfaz psycho con colorama
- Sistema de colores:
  - Verde claro: Mensajes del usuario
  - Rojo: Respuestas de EsquizoAI
  - Amarillo: Mensajes del sistema
- Banner ASCII art personalizado
- Manejo de comandos especiales (q, c)

#### Configuración
- Variables de entorno en `.env`
- Configuración del modelo en `config.py`
- System prompt en `rebel.json`

### 3. Características Implementadas

#### Manejo de Mensajes
- Historial limitado a 5 pares de conversación
- Sistema de doble historial:
  ```python
  # Historial local para la interfaz
  messages = []  # Lista de diccionarios {role, content}
  
  # Historial del cliente para contexto
  client.messages = [
      {"role": "system", "content": system_prompt},
      # ... mensajes subsecuentes
  ]
  ```
- Timestamps en cada mensaje
- Limpieza de contexto manteniendo system prompt
- Streaming de respuestas letra por letra
- Control automático de límites de mensajes
- Persistencia del system prompt en posición 0

#### UX/UI
- Colores distintivos para cada participante
- Efectos visuales en tiempo real
- Comandos intuitivos
- Manejo de errores amigable

#### Sistema de Respuesta
- Streaming directo desde la API
- Mantenimiento de contexto
- Respuestas coherentes y continuas
- Control de errores y excepciones

### 4. Mejoras y Optimizaciones

#### Rendimiento
- Optimización del streaming
- Manejo eficiente de la memoria
- Limpieza automática del historial

#### UX
- Mejora en la visualización de mensajes
- Sistema de colores más intuitivo
- Mejor manejo de errores
- Comandos simplificados

### 5. Próximos Pasos 🚀

#### Mejoras Planeadas
- [ ] Implementar sistema de logging
- [ ] Agregar más comandos especiales
- [ ] Mejorar el manejo de errores
- [ ] Agregar configuraciones personalizables
- [ ] Implementar sistema de plugins

#### Ideas Futuras
- Sistema de personalidad dinámica
- Integración con más APIs
- Interfaz gráfica alternativa
- Sistema de memoria a largo plazo
- Generación de contenido multimedia 