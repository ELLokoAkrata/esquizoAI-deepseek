# Frontend para Terminal Web EsquizoAI-DeepSeek

Este frontend replica la experiencia de la terminal CLI en la web, usando React y TailwindCSS.

## Estructura sugerida

- src/
  - components/
    - Terminal.jsx
    - MessageBubble.jsx
    - InputBar.jsx
  - App.jsx
  - main.jsx
- tailwind.config.js
- postcss.config.js
- index.html
- package.json
- README.md

## Tareas iniciales

- [ ] Inicializar proyecto React (Vite recomendado)
- [ ] Instalar TailwindCSS
- [ ] Instalar xterm.js o react-terminal
- [ ] Implementar layout terminal (fondo negro, colores por rol)
- [ ] Contenedores diferenciados para usuario e IA
- [ ] Autoscroll al recibir mensajes
- [ ] Input multilinea y envío con Enter
- [ ] Conexión a backend vía SSE para streaming
- [ ] Mapear colores actuales (colorama) a clases CSS

---

Para desarrollo local:

```bash
cd web/frontend
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install xterm
```

Luego correr con:

```bash
npm run dev
```
