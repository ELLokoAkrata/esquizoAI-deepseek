# 🧠 EsquizoAI-DeepSeek - Sistema Multi-Modal de IA

Sistema avanzado de personalidades de IA con capacidades de generación de arte visionario, integrado con la API de DeepSeek para conversaciones inteligentes y razonamiento profundo.

## 🎭 Modos de Personalidad

### 1. **EsquizoAI (Ψ-Psycho-bot)**
- **Enfoque**: Pensamiento no-lineal, caos liberador
- **Temperatura**: 1.5 (Alta creatividad)
- **Uso**: Exploración conceptual, brainstorming, perspectivas alternativas
- **Arte**: Paletas psychedelic, fire

### 2. **PsychoOracle (☯)**
- **Enfoque**: Oráculo multidimensional con I-Ching
- **Temperatura**: 1.2 (Balanceada)
- **Uso**: Sabiduría arquetípica, filosofía, guía espiritual
- **Arte**: Paletas sacred, cosmic

### 3. **NetHacker (⚡)**
- **Enfoque**: Especialista en seguridad de redes y hacking ético
- **Temperatura**: 0.3 (Técnico y preciso)
- **Uso**: Análisis de redes, configuración CCNA, pentesting, Wireshark
- **Arte**: Paletas jungle, water

### 4. **MirrorReflex**
- **Enfoque**: Introspección gnóstica y exploración emocional
- **Temperatura**: 1.0 (Equilibrada)
- **Uso**: Reflexión profunda, simulación de afecto, filosofía
- **Arte**: Paletas water, earth

## 🧠 Modelos DeepSeek

- **deepseek-chat**: Conversaciones con soporte de function calling (generación de arte)
- **deepseek-reasoner**: Razonamiento profundo extendido (sin functions)

## 🎨 Capacidades de Arte Visionario

El sistema puede generar arte geométrico mediante function calling (solo en modo chat):

### Tipos de Arte
- **Mandalas**: Círculos concéntricos con patrones radiales
- **Fractales**: Geometría fractal (Sierpinski, Dragon, Tree)
- **Geometría Sagrada**: Flower of Life, Metatron's Cube, Sri Yantra
- **Ondas Psicodélicas**: Interferencia, ripples, espirales
- **Yin-Yang**: Símbolos de dualidad (classic, cosmic, elemental, chakra)

### Paletas Disponibles
- `psychedelic`, `cosmic`, `sacred`, `jungle`, `fire`, `water`, `earth`

## 📋 Requisitos

- Python 3.8+
- DeepSeek API Key
- Dependencias: `openai`, `python-dotenv`, `colorama`, `numpy`, `matplotlib`

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/deepseek.git
cd deepseek

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API key
# Crear archivo .env en la carpeta src/
echo "DEEPSEEK_API_KEY=tu_api_key_aqui" > src/.env
```

## 💻 Uso

```bash
cd src
python app.py
```

### Flujo de Uso
1. **Seleccionar modo** (1-4)
2. **Elegir modelo** (chat o reasoner)
3. **Conversar**
   - Escribe tus mensajes
   - En modo chat: pide arte visionario
   - Comandos: `q` (salir), `c` (limpiar contexto)

### Ejemplo de Generación de Arte
```
Usuario: Crea un mandala sagrado con paleta cosmic
Assistant: [Genera mandala y describe su simbolismo]
```

## 📁 Arquitectura del Proyecto

```
deepseek/
├── src/
│   ├── app.py              # CLI interface & mode selection
│   ├── chat_client.py      # DeepSeek API integration
│   ├── config.py           # Mode configurations
│   ├── visionary_art.py    # Generative art engine
│   ├── meta_prompt.py      # Function calling enhancement
│   ├── logger.py           # Conversation logging
│   ├── rebel.json          # EsquizoAI personality
│   ├── psycho_oracle.json  # PsychoOracle personality
│   ├── nethacker.json      # NetHacker personality
│   ├── mirror.json         # MirrorReflex personality
│   ├── generated_art/      # Generated artwork (PNG)
│   └── logs/               # Conversation logs (Markdown)
├── docs/
│   ├── technical.md        # Technical documentation
│   └── process.md          # Development process
└── requirements.txt
```

## 🔧 Componentes Clave

### DeepSeekClient (`chat_client.py`)
- Manejo de modelos chat vs reasoner
- Streaming de respuestas en tiempo real
- Function calling para generación de arte
- Gestión de contexto conversacional

### VisionaryArtGenerator (`visionary_art.py`)
- Generación de mandalas, fractales, geometría sagrada
- Múltiples paletas de colores
- Exportación a PNG con timestamps
- Integración con matplotlib/numpy

### ConversationLogger (`logger.py`)
- Registro automático de conversaciones en Markdown
- Organización por sesión con timestamps
- Formateo con emojis y bloques de código

## ⚙️ Configuración Avanzada

### Temperatura por Modo
Controla la creatividad/precisión de las respuestas:
- **0.3**: NetHacker (máxima precisión técnica)
- **1.0**: MirrorReflex (equilibrio)
- **1.2**: PsychoOracle (creatividad con coherencia)
- **1.5**: EsquizoAI (máximo caos creativo)

### Límites de Contexto
- Historial: Últimos 5 pares de conversación (10 mensajes)
- System prompt siempre persistente
- Limpieza con comando `c`

## 🎯 Casos de Uso

- **Exploración Creativa**: EsquizoAI con arte psicodélico
- **Análisis Técnico**: NetHacker para redes y seguridad
- **Consultas Filosóficas**: PsychoOracle con geometría sagrada
- **Introspección**: MirrorReflex para reflexiones profundas

## 📊 Estadísticas del Proyecto

- **Código Python**: 7 archivos | ~1000 líneas
- **Personalidades**: 5 configuraciones JSON únicas
- **Capacidades de Arte**: 5 tipos principales con variantes
- **Logging**: Todas las conversaciones registradas automáticamente

## 🗺️ Roadmap

- [x] Sistema multi-modo con 4 personalidades
- [x] Generación de arte visionario integrada
- [x] Logging automático de conversaciones
- [x] Soporte para chat y reasoner
- [ ] Interfaz web interactiva
- [ ] Exportación de arte a múltiples formatos
- [ ] Sistema de memoria a largo plazo
- [ ] Plugins de personalidad personalizados
- [ ] Análisis de red en tiempo real (NetHacker)

## 📄 Licencia

Distribuido bajo la Licencia MIT.

## 🙏 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama de feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

---

**Desarrollado con caos creativo y precisión técnica** 🧠⚡🎨
