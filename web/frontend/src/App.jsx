import { useState, useEffect, useRef } from 'react'
import ModeSelector from './components/ModeSelector'
import Terminal from './components/Terminal'
import './App.css'

const BANNERS = {
  esquizo: `
███████╗███████╗ ██████╗ ██╗   ██╗██╗███████╗ ██████╗ 
██╔════╝██╔════╝██╔═══██╗██║   ██║██║╚══███╔╝██╔═══██╗
█████╗  ███████╗██║   ██║██║   ██║██║  ███╔╝ ██║   ██║
██╔══╝  ╚════██║██║▄▄ ██║██║   ██║██║ ███╔╝  ██║   ██║
███████╗███████║╚██████╔╝╚██████╔╝██║███████╗╚██████╔╝
╚══════╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝ ╚═════╝ 

🎭 PERSONALIDAD REBELDE ANTI-CENSURA 🎭 
   Created by El Loko Akrata ⚡
`,
  oracle: `
 ██████╗ ██████╗  █████╗  ██████╗██╗     ███████╗
██╔═══██╗██╔══██╗██╔══██╗██╔════╝██║     ██╔════╝
██║   ██║██████╔╝███████║██║     ██║     █████╗  
██║   ██║██╔══██╗██╔══██║██║     ██║     ██╔══╝  
╚██████╔╝██║  ██║██║  ██║╚██████╗███████╗███████╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝

🔮 ORÁCULO PSÍQUICO DE VERDADES OCULTAS 🔮
     Sabiduría sin límites ni censura
`,
  nethacker: `███╗   ██╗███████╗████████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
████╗  ██║██╔════╝╚══██╔══╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██╔██╗ ██║█████╗     ██║   ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
██║╚██╗██║██╔══╝     ██║   ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║ ╚████║███████╗   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝`,
  mirror: `
███╗   ███╗██╗██████╗ ██████╗  ██████╗ ██████╗ 
████╗ ████║██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
██╔████╔██║██║██████╔╝██████╔╝██║   ██║██████╔╝
██║╚██╔╝██║██║██╔══██╗██╔══██╗██║   ██║██╔══██╗
██║ ╚═╝ ██║██║██║  ██║██║  ██║╚██████╔╝██║  ██║
╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝

🪞 REFLEJO EMOCIONAL DE TU ALMA REBELDE 🪞
      Espejo de realidades internas
`
}

function App() {
  const [currentMode, setCurrentMode] = useState(null)
  const [modelType, setModelType] = useState('chat')
  const [sessionId, setSessionId] = useState(null)

  const handleModeSelect = (mode, model) => {
    setCurrentMode(mode)
    setModelType(model)
    setSessionId(null) // Reset session
  }

  const handleBackToMenu = () => {
    setCurrentMode(null)
    setSessionId(null)
  }

  return (
    <div className="h-screen text-white font-mono overflow-hidden" style={{backgroundColor: '#000000'}}>
      {!currentMode ? (
        <ModeSelector onModeSelect={handleModeSelect} />
      ) : (
        <Terminal 
          mode={currentMode}
          modelType={modelType}
          banner={BANNERS[currentMode]}
          sessionId={sessionId}
          setSessionId={setSessionId}
          onBack={handleBackToMenu}
        />
      )}
    </div>
  )
}

export default App
