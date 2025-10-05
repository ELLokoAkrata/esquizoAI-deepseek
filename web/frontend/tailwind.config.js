/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Mapeo de colores del CLI (colorama) a CSS
        terminal: {
          bg: '#000000',
          text: '#ffffff',
          // Colores por modo
          esquizo: {
            banner: '#ffffff',
            prompt: '#ff0000',  // Rojo como pediste
            response: '#ff0000'
          },
          oracle: {
            banner: '#ffff00',  // Yellow
            prompt: '#ffff00',
            response: '#ffffff'
          },
          nethacker: {
            banner: '#00ff00',  // Green
            prompt: '#00ff00',
            response: '#ffffff'
          },
          mirror: {
            banner: '#ff00ff',  // Magenta
            prompt: '#ff00ff',
            response: '#ffffff'
          }
        }
      },
      fontFamily: {
        'mono': ['Consolas', 'Monaco', 'Courier New', 'monospace']
      }
    },
  },
  plugins: [],
}