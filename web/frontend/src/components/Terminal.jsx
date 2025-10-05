import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'

const MODE_COLORS = {
  esquizo: { 
    banner: 'text-black bg-gray-400', 
    prompt: 'text-red-400', 
    response: 'text-green-400' 
  },
  oracle: { 
    banner: 'text-yellow-300 bg-black', 
    prompt: 'text-yellow-300', 
    response: 'text-white' 
  },
  nethacker: { 
    banner: 'text-green-400 bg-black', 
    prompt: 'text-green-400', 
    response: 'text-white' 
  },
  mirror: { 
    banner: 'text-purple-400 bg-black', 
    prompt: 'text-purple-400', 
    response: 'text-white' 
  }
}

const WELCOME_MESSAGES = {
  esquizo: '¡Psi-activación completa! ¿En qué dimensión necesitas ayuda?',
  nethacker: 'NetHacker-X inicializado. ¿Qué análisis necesitas?',
  mirror: 'MirrorReflex listo. ¿Qué emociones deseas explorar?',
  oracle: '☯ PsychoOracle activado. ¿Qué misterios deseas consultar?'
}

function Terminal({ mode, modelType, banner, sessionId, setSessionId, onBack }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [turnNumber, setTurnNumber] = useState(1)
  const [initialized, setInitialized] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const colors = MODE_COLORS[mode]

  useEffect(() => {
    // Solo inicializar una vez
    if (!initialized) {
      const welcomeMsg = `${WELCOME_MESSAGES[mode]}${modelType === 'chat' ? ' Puedo crear arte visionario también.' : ''}`
      setMessages([{
        role: 'assistant',
        content: welcomeMsg,
        reasoning: '',
        timestamp: Date.now()
      }])
      setInitialized(true)
    }
    
    // Focus en input
    inputRef.current?.focus()
  }, [mode, modelType, initialized])

  useEffect(() => {
    // Auto scroll al final
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const addMessage = (role, content, reasoning = '') => {
    setMessages(prev => [...prev, { role, content, reasoning, timestamp: Date.now() }])
  }

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    setIsLoading(true)

    // Agregar mensaje del usuario
    addMessage('user', userMessage)

    try {
      const response = await fetch('http://localhost:8000/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          mode: mode,
          model_type: modelType,
          session_id: sessionId || null
        })
      })

      // Obtener session_id del header de respuesta
      const newSessionId = response.headers.get('X-Session-ID')
      if (newSessionId && newSessionId !== sessionId) {
        console.log(`🔗 Nueva sesión obtenida: ${newSessionId}`)
        setSessionId(newSessionId)
      } else if (sessionId) {
        console.log(`♻️  Usando sesión existente: ${sessionId}`)
      }

      const reader = response.body.getReader()
      let aiResponse = { content: '', reasoning: '' }
      let currentMessageIndex = messages.length + 1 // +1 porque ya agregamos el mensaje del usuario

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = new TextDecoder().decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              
              if (data.error) {
                addMessage('assistant', `❌ Error: ${data.error}`)
                break
              }

              // Capturar session_id del stream
              if (data.session_id && data.session_id !== sessionId) {
                console.log(`📡 Session ID recibido via stream: ${data.session_id}`)
                setSessionId(data.session_id)
              }

              if (data.reasoning) {
                aiResponse.reasoning += data.reasoning
              }
              
              if (data.content) {
                aiResponse.content += data.content
              }

              // Actualizar mensaje en tiempo real
              setMessages(prev => {
                const newMessages = [...prev]
                const lastMessage = newMessages[newMessages.length - 1]
                
                // Solo actualizar si es del usuario o crear nuevo mensaje AI
                if (lastMessage && lastMessage.role === 'assistant' && 
                    lastMessage.timestamp && (Date.now() - lastMessage.timestamp < 1000)) {
                  // Actualizar mensaje existente (si es reciente)
                  newMessages[newMessages.length - 1] = {
                    ...lastMessage,
                    content: aiResponse.content,
                    reasoning: aiResponse.reasoning
                  }
                } else if (lastMessage && lastMessage.role === 'user') {
                  // Crear nuevo mensaje AI después del usuario
                  newMessages.push({
                    role: 'assistant',
                    content: aiResponse.content,
                    reasoning: aiResponse.reasoning,
                    timestamp: Date.now()
                  })
                } else if (lastMessage && lastMessage.role === 'assistant') {
                  // Actualizar el último mensaje AI
                  newMessages[newMessages.length - 1] = {
                    ...lastMessage,
                    content: aiResponse.content,
                    reasoning: aiResponse.reasoning
                  }
                }
                
                return newMessages
              })

            } catch (e) {
              console.error('Error parsing SSE data:', e)
            }
          }
        }
      }

      setTurnNumber(prev => prev + 1)

    } catch (error) {
      console.error('Error:', error)
      addMessage('assistant', `☢️ Error crítico: ${error.message}`)
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
    
    // Atajos de teclado
    if (e.key.toLowerCase() === 'c' && input.trim() === 'c') {
      e.preventDefault()
      setInput('')
      clearContext()
    }
    
    if (e.key.toLowerCase() === 'q' && input.trim() === 'q') {
      e.preventDefault()
      setInput('')
      console.log('Atajo Q detectado, volviendo al menú...')
      onBack()
    }
  }

  const clearContext = async () => {
    if (sessionId) {
      try {
        await fetch('http://localhost:8000/chat/reset', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sessionId })
        })
      } catch (error) {
        console.error('Error clearing context:', error)
      }
    }
    
    // Resetear estado local
    const welcomeMsg = `${WELCOME_MESSAGES[mode]}${modelType === 'chat' ? ' Puedo crear arte visionario también.' : ''}`
    setMessages([{
      role: 'assistant',
      content: '♻️ Contexto reiniciado. ' + welcomeMsg,
      reasoning: '',
      timestamp: Date.now()
    }])
    setTurnNumber(1)
    setSessionId(null)
  }

  return (
    <div className="terminal-container">
      {/* Header con banner */}
      <div className={`${colors.banner} p-4`}>
        <pre className="banner-text text-xs">{banner}</pre>
        <div className="flex justify-between items-center mt-2">
          <span className="text-sm">
            ⚛️ {mode.toUpperCase()} - {modelType.toUpperCase()}
          </span>
          <div className="space-x-4 text-sm">
            <button 
              onClick={clearContext} 
              className="hover:bg-gray-700 px-2 py-1 rounded border border-gray-600"
            >
              ♻️ Reset
            </button>
            <button 
              onClick={() => {
                console.log('Volviendo al menú...')
                onBack()
              }} 
              className="hover:bg-gray-700 px-2 py-1 rounded border border-gray-600 text-red-400"
            >
              ← MENU
            </button>
          </div>
        </div>
      </div>

      {/* Área de mensajes */}
      <div className="terminal-output">
        {messages.map((message, index) => (
          <div key={index} className={`message-${message.role} mb-3 font-mono`}>
            {message.role === 'user' ? (
              <div className={`${colors.prompt} font-bold`}>
                <span className="text-white">🌀 [Ronda {Math.ceil((index + 1) / 2)}] ➔ </span>
                <span className={colors.prompt}>{message.content}</span>
              </div>
            ) : (
              <div>
                {message.reasoning && (
                  <div className={`${colors.prompt} opacity-90 text-sm mb-1 bg-gray-900 p-2 rounded border-l-2 border-${mode === 'esquizo' ? 'green' : mode === 'oracle' ? 'yellow' : mode === 'nethacker' ? 'green' : 'purple'}-400`}>
                    <span className="text-gray-300">[RAZONAMIENTO]:</span><br/>
                    <ReactMarkdown className="markdown-content">
                      {message.reasoning}
                    </ReactMarkdown>
                  </div>
                )}
                <div className={`${colors.response} font-bold bg-purple-900 p-3 rounded border-l-4 border-purple-500`}>
                  <span className="text-white">🌀 [Salida {mode.toUpperCase()}]: </span>
                  <div className={`${colors.response} markdown-content`}>
                    <ReactMarkdown>
                      {message.content}
                    </ReactMarkdown>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className={`${colors.prompt} animate-pulse`}>
            ⚡ [Procesando en {modelType.toUpperCase()}]...
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input área */}
      <div className="border-t border-gray-700 p-4">
        <div className="flex items-center">
          <span className={`${colors.prompt} mr-2`}>
            🌀 [Ronda {turnNumber}] ➔
          </span>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            className="terminal-input"
            placeholder="Escribe tu mensaje... (Enter para enviar)"
            disabled={isLoading}
          />
        </div>
        <div className="text-xs text-gray-500 mt-2">
          ⚡ Enter: enviar | Shift+Enter: nueva línea | 'c': reset | 'q': menu
        </div>
      </div>
    </div>
  )
}

export default Terminal