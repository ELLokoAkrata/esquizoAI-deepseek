import os
from datetime import datetime
from pathlib import Path

class ConversationLogger:
    def __init__(self, mode_name: str = "EsquizoAI"):
        self.mode_name = mode_name
        # Crear directorio logs si no existe
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Iniciar nueva sesión
        self.session_start = datetime.now()
        self.session_file = self._create_session_file()
        self._log_session_start()
    
    def _create_session_file(self) -> Path:
        """Crea un nuevo archivo de sesión con formato: YYYY-MM-DD_HH-MM-SS.md"""
        filename = self.session_start.strftime("%Y-%m-%d_%H-%M-%S.md")
        return self.logs_dir / filename
    
    def _log_session_start(self):
        """Registra el inicio de la sesión"""
        header = f"""# Sesión {self.mode_name} 🤪

## Información de Sesión
- **Modo**: {self.mode_name}
- **Fecha**: {self.session_start.strftime("%Y-%m-%d")}
- **Hora de inicio**: {self.session_start.strftime("%H:%M:%S")}
- **Status**: Activa 💀

---
## Conversación

"""
        self._write_to_log(header)
    
    def log_message(self, role: str, content: str):
        """Registra un mensaje en el log con formato Markdown"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if role == "user":
            message = f"""### 👤 Usuario [{timestamp}]
```
{content}
```

"""
        else:
            # Procesar el contenido para mantener el formato Markdown
            message = f"""### 🤖 {self.mode_name} [{timestamp}]
{content}

"""
        
        self._write_to_log(message)
    
    def log_system_event(self, event: str):
        """Registra eventos del sistema"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"""---
> 💻 **Evento del Sistema** [{timestamp}]: {event}
---

"""
        self._write_to_log(message)
    
    def close_session(self):
        """Cierra la sesión actual"""
        end_time = datetime.now()
        duration = end_time - self.session_start
        
        footer = f"""
---
## Fin de Sesión
- **Hora de cierre**: {end_time.strftime("%H:%M:%S")}
- **Duración**: {str(duration).split('.')[0]}
- **Status**: Terminada 💀
"""
        self._write_to_log(footer)
        
        # Actualizar el status en el header
        with open(self.session_file, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace("Status**: Activa", "Status**: Terminada")
        with open(self.session_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _write_to_log(self, content: str):
        """Escribe contenido en el archivo de log"""
        with open(self.session_file, 'a', encoding='utf-8') as f:
            f.write(content) 
