"""
Assistente Financeiro WhatsApp - Pacote principal

Versão: 1.0.0-beta
Data: Janeiro 2026
"""

__version__ = "1.0.0-beta"
__author__ = "SardinhaPlantao"

# Exportar funções principais para fácil importação
from .intent_parser import analisar_comando
from .order_formatter import formatar_ordem, criar_mensagem_broker, validar_ordem
from .news_fetcher import buscar_noticias_por_ticker
from .utils.helpers import normalizar_texto, validar_ticker, criar_log

# Lista do que está disponível
__all__ = [
    'analisar_comando',
    'formatar_ordem',
    'criar_mensagem_broker',
    'validar_ordem',
    'buscar_noticias_por_ticker',
    'normalizar_texto',
    'validar_ticker',
    'criar_log'
]
