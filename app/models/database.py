"""
Database Module - SQLite Integration
Fornece interface de banco de dados usando SQLite local
"""
import sqlite3
import os
import sys
import shutil
import logging
from flask import g
from app.config import DB_PATH


logger = logging.getLogger(__name__)


def get_db():
    """
    Retorna a instância do Banco de Dados (SQLite)
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    """
    Inicializa o banco de dados.
    Se estiver rodando como executável e o banco não existir,
    copia o banco embutido para a pasta do executável.
    """
    
    # Se o arquivo do banco não existe
    if not os.path.exists(DB_PATH):
        # Verifica se estamos rodando como executável (frozen)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Caminho do banco embutido no executável
            bundled_db = os.path.join(sys._MEIPASS, 'data.db')
            
            if os.path.exists(bundled_db):
                try:
                    # Copia o banco embutido para o local de uso (DB_PATH)
                    shutil.copy2(bundled_db, DB_PATH)
                    logger.info(f"Banco de dados inicializado a partir do executável: {DB_PATH}")
                    return  # Já copiamos o banco pronto, não precisa fazer mais nada
                except Exception as e:
                    logger.error(f"Erro ao copiar banco de dados: {e}")
    
    # Se chegou aqui, ou o banco já existe, ou falhou a cópia, ou não é executável
    # Continua com a verificação padrão
    db = get_db()
    
    # Verificar se as tabelas já existem
    cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Se o banco já tem tabelas, não fazer nada
    if tables:
        logger.info(f"Banco de dados já inicializado. Tabelas encontradas: {len(tables)}")
        return
    
    # Caso contrário, criar estrutura a partir do schema
    try:
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, mode='r', encoding='utf-8') as f:
            db.executescript(f.read())
        db.commit()
        logger.info("Tabelas criadas com sucesso via schema.sql")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")


def close_connection(exception):
    """
    Fecha a conexão com o banco de dados
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

