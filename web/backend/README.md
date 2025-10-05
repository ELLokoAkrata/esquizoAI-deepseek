# FastAPI backend para Terminal Web EsquizoAI-DeepSeek

Este backend expone la lógica de src/ vía API para el frontend web. No modifica el código legacy.

## Estructura sugerida

- main.py         # Punto de entrada FastAPI
- requirements.txt
- README.md

## Tareas iniciales

- [ ] Crear endpoint POST /chat para recibir mensajes y devolver respuestas (streaming)
- [ ] Importar lógica de src/ (chat_client, config, etc.)
- [ ] Mantener compatibilidad con los modos y configuraciones actuales
- [ ] Soporte para múltiples sesiones/contextos
- [ ] Documentar cómo levantar el backend

---

Para desarrollo local:

```bash
cd web/backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install fastapi uvicorn
```

Luego correr con:

```bash
uvicorn main:app --reload
```
