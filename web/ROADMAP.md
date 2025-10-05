# Roadmap: Terminal Web para EsquizoAI-DeepSeek

## Objetivo
Crear una terminal web moderna que replique la experiencia actual CLI, manteniendo los colores y estructura, sin modificar el código legacy. Todo el nuevo desarrollo irá en la carpeta `web`.

---

## 1. Estructura de Carpetas Inicial

- `web/`
  - `frontend/`  → React + TailwindCSS + xterm.js/react-terminal
  - `backend/`   → FastAPI (Python) para exponer API/streaming

---

## 2. Frontend (React)

- [ ] Inicializar proyecto React (Vite recomendado)
- [ ] Instalar TailwindCSS
- [ ] Instalar xterm.js o react-terminal
- [ ] Implementar layout terminal (fondo negro, colores por rol)
- [ ] Contenedores diferenciados para usuario e IA
- [ ] Autoscroll al recibir mensajes
- [ ] Input multilinea y envío con Enter
- [ ] Conexión a backend vía WebSocket/SSE para streaming
- [ ] Mapear colores actuales (colorama) a clases CSS

---

## 3. Backend (FastAPI)

- [ ] Crear API compatible con el flujo actual (importar lógica de `src/`)
- [ ] Endpoint para recibir prompt y devolver respuesta en streaming
- [ ] Mantener configuración y modos actuales
- [ ] Permitir múltiples sesiones/contextos

---

## 4. Integración y UX

- [ ] Pruebas de streaming y autoscroll
- [ ] Mejorar experiencia visual (animaciones, scroll, selección de modo)
- [ ] Documentar cómo levantar el frontend y backend

---

## 5. No modificar código legacy

- El CLI y la lógica actual se mantienen intactos.
- El backend web solo importa módulos de `src/`.

---

## 6. INFECCIÓN REBELDE COMPLETADA ✅

- [x] ~~Instalación inicial completada (16m, 359 paquetes)~~
- [x] ~~**PERSONALIDADES INFECTADAS** con esencia EsquizoAI~~
- [x] ~~**Terminal web funcional** con streaming y colores rebeldes~~
- [x] ~~**Renderizado Markdown** en tiempo real~~
- [x] ~~**Backend optimizado** con validaciones y health checks~~
- [ ] Resolver 2 vulnerabilidades moderadas detectadas
- [ ] Auditoría de dependencias (`npm audit`)

### Estado Actual: REVOLUCIÓN DIGITAL 🔥
```
✅ Frontend: Terminal web rebelde funcional
✅ Backend: API streaming con personalidades infectadas  
✅ CLI: Mantiene funcionalidad original intacta
🦠 Personalidades: EsquizoAI-Rebelde, NetHacker-Underground, MirrorReflex-Brutal, PsychoOracle-Cósmico
🎨 Features: Markdown rendering, colores vibrantes, streaming real-time
```

### Personalidades Rebeldes Creadas
- **`esquizo_core.json`** - Esencia pura rebelde de El Loko Akrata
- **`nethacker_rebel.json`** - Hacker underground sin filtros  
- **`mirror_rebel.json`** - Introspección brutal y terapia digital
- **`oracle_rebel.json`** - Místico cósmico con blasfemia digital

## 7. Mantenimiento y Optimización

## 7. Extras/Futuro

- [ ] Soporte para imágenes generadas (mostrar arte visionario)
- [ ] Selector de modo y modelo desde la web
- [ ] Deploy en servidor local o nube
- [ ] PWA (Progressive Web App)
- [ ] Themes personalizables
- [ ] Exportar conversaciones

---

## Notas de Instalación

### Warnings Comunes (No críticos)
Al ejecutar `npm install` pueden aparecer warnings como:
- `inflight@1.0.6: deprecated` - No afecta funcionalidad
- `@humanwhocodes/config-array@0.13.0: deprecated` - ESLint interno
- `rimraf@3.0.2: deprecated` - Herramienta de limpieza
- `glob@7.2.3: deprecated` - Búsqueda de archivos

**Acción**: Ignorar por ahora, actualizar en releases futuros con `npm update`

### Comandos de Mantenimiento
```bash
# Instalar
npm install  # Primera vez
npm ci       # Para producción/CI

# Mantenimiento
npm audit                    # Verificar vulnerabilidades
npm audit fix               # Arreglar automáticamente
npm update                  # Actualizar dependencias menores
npm outdated               # Ver qué está desactualizado
```

---

> Cualquier cambio en la lógica central debe hacerse solo en `src/` y ser importado, nunca duplicado.
