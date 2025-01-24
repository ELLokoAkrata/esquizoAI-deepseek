import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
BASE_URL = "https://api.deepseek.com"  # Se ajusta automáticamente
MODEL_NAME = "deepseek-reasoner"
TEMPERATURE = 0.7
MAX_TOKENS = 3000
STREAM = True
REBEL_JSON_PATH = str(Path(__file__).parent / 'rebel.json')