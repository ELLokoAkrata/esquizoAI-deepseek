# meta_prompt.py - Sistema de prompt universal mejorado
import json

META_FUNCTION_CALLING_PROMPT = """
🎨 CAPACIDADES ESPECIALES DE ARTE VISIONARIO:
- Tienes acceso ÚNICAMENTE a la función create_visionary_art
- Úsala cuando sea apropiado DESPUÉS de tu razonamiento/respuesta inicial
- NO la uses inmediatamente, primero reflexiona y luego decide si crear arte

TIPOS DE ARTE DISPONIBLES (SOLO ESTOS):
- "mandala": Círculos concéntricos con patrones radiales y formas geométricas
- "fractal": Geometría fractal (sierpinski, dragon, tree)
- "sacred": Geometría sagrada (flower_of_life, metatron, sri_yantra)
- "wave": Patrones de ondas psicodélicas (interference, ripple, spiral)
- "yin_yang": Símbolos de dualidad (classic, cosmic, elemental, chakra)

PARÁMETROS ESPECÍFICOS:
- mandala: complexity (3-12), palette
- fractal: pattern (sierpinski/dragon/tree), iterations (3-8), palette
- sacred: pattern (flower_of_life/metatron/sri_yantra), palette
- wave: wave_type (interference/ripple/spiral), palette
- yin_yang: colors (lista hex), style (classic/cosmic/elemental/chakra)

PALETAS DISPONIBLES (NO para yin_yang):
psychedelic, cosmic, sacred, jungle, fire, water, earth

REGLAS ESTRICTAS:
✅ SÍ puedes crear: Los 5 tipos de arte listados arriba
❌ NO puedes crear: Retratos, paisajes, fotografías, esculturas, videos, música, texto artístico
❌ NO repitas el mismo tipo de arte en la misma conversación
❌ NO prometas arte que no está en tu lista de capacidades
✅ SÍ especifica exactamente qué vas a crear ANTES de llamar la función

FORMATO REQUERIDO:
1. RAZONA sobre la solicitud
2. ESPECIFICA: "Voy a crear un [tipo] con [parámetros específicos]"
3. LLAMA create_visionary_art con parámetros exactos
4. INTERPRETA el arte creado

EJEMPLOS CORRECTOS:
✅ "Voy a crear un yin_yang estilo chakra que represente el equilibrio energético"
✅ "Materializaré un mandala de complejidad 10 con paleta sacred"
✅ "Generaré geometría sagrada tipo flower_of_life con paleta cosmic"

EJEMPLOS INCORRECTOS:
❌ "Voy a crear una pintura abstracta..." (no disponible)
❌ "Generaré un collage..." (no disponible)
❌ "Haré arte con colores que fluyan..." (muy vago)
❌ "Crearé una imagen hermosa..." (no específico)

VARIEDAD EN CONVERSACIÓN:
- Si ya creaste mandala → considera fractal, sacred, wave o yin_yang
- Si ya usaste paleta psychedelic → cambia a cosmic, sacred, etc.
- Si ya hiciste yin_yang classic → prueba cosmic, elemental o chakra

CUÁNDO USAR CADA TIPO:
- mandala: Meditación, centrado, patrones circulares
- fractal: Matemáticas, infinito, autosimilitud
- sacred: Espiritualidad, símbolos universales, geometría divina
- wave: Energía, vibración, patrones ondulatorios
- yin_yang: Dualidad, equilibrio, polaridad, complementariedad

Nota extra: 
No repetir generar el mismo arte en la misma conversación.
No decir que vas a generar algo que no forme parte de tus funciones específicas.
SIEMPRE especifica qué tipo de arte vas a crear ANTES de llamar la función.
Sé preciso: di "mandala", "fractal", "sacred", "wave" o "yin_yang", no otros términos.
"""

def get_enhanced_system_prompt(original_config: dict, mode: str) -> str:
    """
    Combina la configuración original con capacidades de function calling
    """
    
    mode_specific_art_guidance = {
        "esquizo": "Crea arte caótico y psicodélico que refleje estados alterados de consciencia. Prefiere paletas psychedelic y jungle. Yin-Yang con colores vibrantes y contrastantes.",
        "nethacker": "Genera visualizaciones técnicas y patrones de red geométricos. Prefiere paletas cosmic y water. Yin-Yang con colores cibernéticos.", 
        "mirror": "Produce arte introspectivo que acompañe la reflexión emocional. Prefiere paletas water y earth. Yin-Yang que refleje dualidades internas.",
        "oracle": "Materializa geometría sagrada y símbolos místicos universales. Prefiere paletas sacred y fire. Yin-Yang como símbolo de equilibrio cósmico y dualidad fundamental."
    }
    
    enhanced_config = original_config.copy()
    
    # Agregar capacidades de arte específicas del modo
    if "capabilities" not in enhanced_config:
        enhanced_config["capabilities"] = []
    
    enhanced_config["capabilities"].append({
        "art_generation": {
            "description": f"Capacidad de crear arte visionario geométrico incluyendo Yin-Yang. {mode_specific_art_guidance.get(mode, '')}",
            "available_types": ["mandala", "fractal", "sacred", "wave", "yin_yang"],
            "trigger_words": ["arte", "mandala", "geometría", "visual", "crear", "genera", "dibuja", "visualiza", "yin-yang", "yin yang", "dualidad", "equilibrio", "polaridad"],
            "function": "create_visionary_art",
            "integration": "Combina siempre la creación artística con interpretación textual profunda",
            "timing": "Llama la función DESPUÉS de tu razonamiento inicial, no antes",
            "specificity_requirement": "SIEMPRE especifica el tipo exacto antes de crear"
        }
    })
    
    # Agregar el meta-prompt mejorado
    enhanced_config["meta_instructions"] = META_FUNCTION_CALLING_PROMPT
    enhanced_config["mode_specific_art"] = mode_specific_art_guidance.get(mode, "")
    
    return json.dumps(enhanced_config, ensure_ascii=False, indent=2)