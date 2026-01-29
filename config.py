"""
Konfiguratsiya sozlamalari
"""

import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

class Config:
    """Bot konfiguratsiya klassi"""

    BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'reja_bot.db')
    
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    LOG_LEVEL = 'INFO' if not DEBUG else 'DEBUG'
