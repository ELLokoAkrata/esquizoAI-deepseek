import { useState } from 'react'

const MODES = {
  esquizo: { name: 'EsquizoAI - Modo Psico-activo', color: 'text-red-500' },
  nethacker: { name: 'NetHacker - Especialista en Redes', color: 'text-green-500' },
  mirror: { name: 'MirrorReflex - Modo Introspectivo', color: 'text-purple-500' },
  oracle: { name: 'PsychoOracle - Oráculo Multidimensional', color: 'text-yellow-500' }
}

function ModeSelector({ onModeSelect }) {
  const [selectedMode, setSelectedMode] = useState(null)

  const handleModeSelect = (mode) => {
    setSelectedMode(mode)
  }

  const handleModelSelect = (modelType) => {
    onModeSelect(selectedMode, modelType)
  }

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-black text-white">
      {!selectedMode ? (
        <div className="text-center">
          <h1 className="text-cyan-400 text-2xl mb-8">Selecciona tu modo de operación:</h1>
          <div className="space-y-4">
            {Object.entries(MODES).map(([key, mode], index) => (
              <button
                key={key}
                onClick={() => handleModeSelect(key)}
                className={`mode-button ${mode.color} block w-full max-w-md text-left`}
              >
                {index + 1}. {mode.name}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center">
          <h2 className={`text-xl mb-6 ${MODES[selectedMode].color}`}>
            {MODES[selectedMode].name}
          </h2>
          <p className="text-cyan-400 mb-8">Selecciona tu interfaz:</p>
          <div className="space-y-4">
            <button
              onClick={() => handleModelSelect('chat')}
              className="mode-button text-white block w-full max-w-md"
            >
              1. Chat
            </button>
            <button
              onClick={() => handleModelSelect('reasoner')}
              className="mode-button text-white block w-full max-w-md"
            >
              2. Razonador
            </button>
          </div>
          <button
            onClick={() => setSelectedMode(null)}
            className="mt-6 text-gray-400 hover:text-white text-sm"
          >
            ← Volver
          </button>
        </div>
      )}
    </div>
  )
}

export default ModeSelector