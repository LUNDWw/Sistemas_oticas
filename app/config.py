import os
import sys
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    
    if hasattr(sys, '_MEIPASS'):
        INTERNAL_DIR = sys._MEIPASS
    else:
        INTERNAL_DIR = BASE_DIR

    TEMPLATE_DIR = os.path.join(INTERNAL_DIR, 'app', 'templates')
    STATIC_DIR = os.path.join(INTERNAL_DIR, 'app', 'static')
    
    try:
        with open(os.path.join(BASE_DIR, 'debug_paths.txt'), 'w') as f:
            f.write(f"Executable: {sys.executable}\n")
            f.write(f"Base Dir: {BASE_DIR}\n")
            f.write(f"Internal Dir: {INTERNAL_DIR}\n")
            f.write(f"Static Dir: {STATIC_DIR}\n")
            f.write(f"Template Dir: {TEMPLATE_DIR}\n")
            if os.path.exists(STATIC_DIR):
                f.write(f"Static contents: {os.listdir(STATIC_DIR)}\n")
            else:
                f.write("Static dir does not exist!\n")
    except Exception as e:
        pass
else:
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'app', 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'app', 'static')

DB_PATH = os.path.join(BASE_DIR, 'data.db')

# Variáveis de segurança - ler de .env
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não configurada no .env")

LOG_FILE = os.path.join(BASE_DIR, 'error.log')
LOG_LEVEL = logging.ERROR
HOST = '127.0.0.1'
PORT = 5000
DEBUG_MODE = not getattr(sys, 'frozen', False)

