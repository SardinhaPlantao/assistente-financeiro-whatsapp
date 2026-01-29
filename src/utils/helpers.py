"""
FUNÇÕES AUXILIARES - UTILS/HELPERS.PY

Funções utilitárias que podem ser usadas por todos os módulos do sistema.
Mantém código organizado e evita repetição.
"""

import re
import unicodedata
from datetime import datetime
import os
import sys

# ====== FUNÇÕES DE TEXTO ======

def normalizar_texto(texto):
    """
    Normaliza texto para processamento:
    1. Converte para minúsculas
    2. Remove acentos
    3. Remove pontuação extra
    4. Remove espaços duplicados
    
    Exemplo: "Compra 100 PETR4!" → "compra 100 petr4"
    """
    if not texto or not isinstance(texto, str):
        return ""
    
    # 1. Minúsculas
    texto = texto.lower()
    
    # 2. Remover acentos
    texto = remover_acentos(texto)
    
    # 3. Remover pontuação (exceto números e letras)
    texto = re.sub(r'[^\w\s]', ' ', texto)
    
    # 4. Remover espaços duplicados
    texto = ' '.join(texto.split())
    
    return texto


def remover_acentos(texto):
    """
    Remove acentos de strings em português.
    
    Exemplo: "notícias" → "noticias", "ação" → "acao"
    """
    # Usa unicodedata para decompor caracteres acentuados
    texto = unicodedata.normalize('NFKD', texto)
    
    # Remove os caracteres de combinação (acentos)
    texto = ''.join([c for c in texto if not unicodedata.combining(c)])
    
    return texto


def extrair_numeros(texto):
    """
    Extrai todos os números de um texto.
    
    Exemplo: "compra 100 PETR4 conta 123-45" → [100, 123, 45]
    """
    if not texto:
        return []
    
    numeros = re.findall(r'\d+', texto)
    return [int(num) for num in numeros]


def extrair_primeiro_numero(texto):
    """
    Extrai o primeiro número encontrado no texto.
    Retorna None se não encontrar.
    """
    numeros = extrair_numeros(texto)
    return numeros[0] if numeros else None


# ====== FUNÇÕES DE VALIDAÇÃO ======

def validar_ticker(ticker):
    """
    Valida se um ticker tem formato correto.
    Formato esperado: 4 letras + 1-2 números (ex: PETR4, B3SA3)
    
    Retorna (True, ticker_normalizado) ou (False, mensagem_erro)
    """
    if not ticker:
        return False, "Ticker não pode ser vazio"
    
    # Converter para string e maiúsculas
    ticker_str = str(ticker).strip().upper()
    
    # Verificar formato com regex
    padrao = r'^[A-Z]{4}\d{1,2}$'
    
    if re.match(padrao, ticker_str):
        return True, ticker_str
    else:
        return False, f"Formato inválido: {ticker}. Use: 4 letras + 1-2 números (ex: PETR4)"


def validar_quantidade(quantidade):
    """
    Valida se uma quantidade é válida para ordens.
    
    Retorna (True, quantidade_int) ou (False, mensagem_erro)
    """
    if quantidade is None:
        return False, "Quantidade não especificada"
    
    try:
        qtd_int = int(quantidade)
    except (ValueError, TypeError):
        return False, "Quantidade deve ser um número"
    
    if qtd_int <= 0:
        return False, "Quantidade deve ser maior que zero"
    
    if qtd_int > 1000000:  # Limite de segurança
        return False, "Quantidade muito alta (limite: 1.000.000)"
    
    return True, qtd_int


# ====== FUNÇÕES DE FORMATAÇÃO ======

def formatar_data_hora(formato='%d/%m/%Y %H:%M:%S'):
    """
    Retorna data e hora atual formatada.
    
    Formatos comuns:
    - '%d/%m/%Y %H:%M:%S' → "30/01/2026 14:30:15"
    - '%Y-%m-%d' → "2026-01-30"
    - '%H:%M' → "14:30"
    """
    agora = datetime.now()
    return agora.strftime(formato)


def formatar_moeda(valor, simbolo='R$'):
    """
    Formata valores monetários no padrão brasileiro.
    
    Exemplo: 1234.56 → "R$ 1.234,56"
    """
    try:
        valor_float = float(valor)
        # Formatar com 2 casas decimais, separador de milhares e decimal brasileiro
        formatado = f"{valor_float:,.2f}"
        formatado = formatado.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"{simbolo} {formatado}"
    except (ValueError, TypeError):
        return f"{simbolo} 0,00"


# ====== FUNÇÕES DE LOG ======

def criar_log(mensagem, tipo='INFO', arquivo_log='logs/sistema.log'):
    """
    Cria uma entrada de log formatada.
    
    Tipos: INFO, WARNING, ERROR, SUCCESS
    """
    # Criar pasta logs se não existir
    os.makedirs(os.path.dirname(arquivo_log), exist_ok=True)
    
    timestamp = formatar_data_hora()
    linha_log = f"[{timestamp}] [{tipo}] {mensagem}\n"
    
    try:
        with open(arquivo_log, 'a', encoding='utf-8') as f:
            f.write(linha_log)
        return True
    except Exception as e:
        print(f"❌ Erro ao criar log: {e}")
        return False


def log_comando(comando, resultado, usuario='SISTEMA'):
    """
    Log específico para comandos do assistente.
    """
    mensagem = f"Usuário: {usuario} | Comando: '{comando}' | Resultado: {resultado}"
    return criar_log(mensagem, tipo='INFO')


# ====== FUNÇÕES DO SISTEMA ======

def limpar_tela():
    """
    Limpa a tela do terminal (funciona em Windows, Mac e Linux).
    """
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


def pausar_execucao(segundos=2):
    """
    Pausa a execução por um número de segundos.
    Útil para simular processamento.
    """
    import time
    time.sleep(segundos)


def mostrar_progresso(etapa, total_etapas, texto=""):
    """
    Mostra uma barra de progresso simples no terminal.
    
    Exemplo: [=====>     ] 50% Buscando notícias...
    """
    percentual = int((etapa / total_etapas) * 100)
    barras = int(percentual / 5)  # 20 caracteres = 100%
    espacos = 20 - barras
    
    barra = "[" + "=" * barras + ">" + " " * espacos + "]"
    
    print(f"\r{barra} {percentual}% {texto}", end='', flush=True)
    
    if etapa == total_etapas:
        print()  # Nova linha ao finalizar


# ====== FUNÇÃO DE TESTE ======
def testar_helpers():
    """
    Testa todas as funções do módulo helpers.
    """
    
    print("🧪 TESTANDO FUNÇÕES AUXILIARES")
    print("=" * 50)
    
    # Teste 1: Normalizar texto
    print("\n1️⃣ Teste: normalizar_texto()")
    testes = ["Compra 100 PETR4!", "Notícias da VALE3", "AÇÃO pré-market"]
    for teste in testes:
        resultado = normalizar_texto(teste)
        print(f"   '{teste}' → '{resultado}'")
    
    # Teste 2: Validar ticker
    print("\n2️⃣ Teste: validar_ticker()")
    tickers = ["PETR4", "XYZ", "ABCD123", "VALE3", "1234"]
    for ticker in tickers:
        valido, mensagem = validar_ticker(ticker)
        status = "✅" if valido else "❌"
        print(f"   {status} {ticker}: {mensagem}")
    
    # Teste 3: Formatar moeda
    print("\n3️⃣ Teste: formatar_moeda()")
    valores = [1000, 1234.56, "999.99", "inválido"]
    for valor in valores:
        resultado = formatar_moeda(valor)
        print(f"   {valor} → {resultado}")
    
    # Teste 4: Data/hora
    print("\n4️⃣ Teste: formatar_data_hora()")
    print(f"   Agora: {formatar_data_hora()}")
    print(f"   Data: {formatar_data_hora('%d/%m/%Y')}")
    print(f"   Hora: {formatar_data_hora('%H:%M:%S')}")
    
    print("\n" + "=" * 50)
    print("✅ Todos os testes concluídos!")


# Executar testes se rodar arquivo diretamente
if __name__ == "__main__":
    testar_helpers()
