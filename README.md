# 🧠 DeepSeek - Sistema Dual de IA

## Descripción
Sistema avanzado de IA con dos modos de operación:
- **EsquizoAI**: Modo psico-activo para interacciones no-lineales y pensamiento divergente
- **NetHacker**: Especialista en análisis de redes, seguridad y hacking ético

## 🚀 Características
- Sistema dual con personalidades especializadas
- Procesamiento de lenguaje natural avanzado
- Interfaz CLI con diseño visual distintivo
- Logging y gestión de contexto
- Modos de chat y razonamiento

## 🛠 Requisitos
- Python 3.8+
- OpenAI API Key
- DeepSeek API Key

## 📦 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/deepseek.git
cd deepseek
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
Crear archivo `.env` en la carpeta `src/` con:
```env
DEEPSEEK_API_KEY=tu_api_key_aqui
```

## 🎮 Uso

1. Ejecutar la aplicación:
```bash
cd src
python app.py
```

2. Seleccionar modo:
- 1: EsquizoAI - Modo Psico-activo
- 2: NetHacker - Especialista en Redes

3. Seleccionar interfaz:
- 1: Chat
- 2: Razonador

## 🔧 Estructura del Proyecto
```
deepseek/
├── src/
│   ├── app.py           # Aplicación principal
│   ├── chat_client.py   # Cliente de chat
│   ├── config.py        # Configuración
│   ├── rebel.json       # Config EsquizoAI
│   └── nethacker.json   # Config NetHacker
├── docs/                # Documentación
├── requirements.txt     # Dependencias
└── README.md           # Este archivo
```

## 🤝 Contribución
¡Las contribuciones son bienvenidas! Por favor, asegúrate de:
1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia
Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## 🎯 Roadmap
- [ ] Integración con más modelos de IA
- [ ] Interfaz web
- [ ] Plugins personalizados
- [ ] Análisis de red en tiempo real
- [ ] Sistema de templates para respuestas 