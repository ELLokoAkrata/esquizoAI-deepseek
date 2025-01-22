import os
from dotenv import load_dotenv
from pathlib import Path

# Obtener el directorio actual (src)
CURRENT_DIR = Path(__file__).parent

# Cargar variables de entorno desde .env en src
load_dotenv(CURRENT_DIR / '.env')

# API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
BASE_URL = "https://api.deepseek.com/v1"

# Model Configuration
MODEL_NAME = "deepseek-chat" # o   
TEMPERATURE = 1.5
MAX_TOKENS = 2000
STREAM = True

# System Prompt Configuration
REBEL_JSON_PATH = str(CURRENT_DIR / 'rebel.json')

