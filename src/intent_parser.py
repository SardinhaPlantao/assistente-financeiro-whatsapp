"""
Módulo que analisa comandos em português para o assistente financeiro.
Exemplos de comandos que entende:
- "compra 100 PETR4 conta 12345"
- "notícias VALE3"
- "venda 50 ITUB4"
"""

import re

def analisar_comando(texto):
    """
    Analisa um comando em português e descobre o que o usuário quer.
    
    Retorna um dicionário com:
    {
        "acao": "compra" ou "venda" ou "noticias",
        "ticker": "PETR4" (se houver),
        "quantidade": 100 (se for ordem),
        "conta": "12345" (se mencionada),
        "mensagem_original": texto original
    }
    """
    
    # Primeiro, vamos limpar o texto
    texto_limpo = texto.lower().strip()
    
    # Resultado inicial
    resultado = {
        "acao": "desconhecida",
        "ticker": None,
        "quantidade": None,
        "conta": None,
        "mensagem_original": texto
    }
    
    # 1. VERIFICAR SE É SOBRE NOTÍCIAS
    palavras_noticias = ["noticia", "notícia", "noticias", "notícias", "news"]
    for palavra in palavras_noticias:
        if palavra in texto_limpo:
            resultado["acao"] = "noticias"
            break
    
    # 2. VERIFICAR SE É COMPRA OU VENDA
    if "compra" in texto_limpo or "comprar" in texto_limpo:
        resultado["acao"] = "compra"
    elif "venda" in texto_limpo or "vender" in texto_limpo:
        resultado["acao"] = "venda"
    
    # 3. PROCURAR TICKER (ex: PETR4, VALE3)
    # Padrão: 4 letras + 1 número (ex: PETR4) ou 4 letras + 2 números (ex: B3SA3)
    padrao_ticker = re.search(r'([a-z]{4}\d{1,2})', texto_limpo)
    if padrao_ticker:
        resultado["ticker"] = padrao_ticker.group(1).upper()
    
    # 4. PROCURAR QUANTIDADE (apenas números)
    padrao_quantidade = re.search(r'(\d+)', texto_limpo)
    if padrao_quantidade:
        resultado["quantidade"] = int(padrao_quantidade.group(1))
    
    # 5. PROCURAR CONTA
    if "conta" in texto_limpo:
        # Procura número após "conta"
        partes = texto_limpo.split("conta")
        if len(partes) > 1:
            # Pega o que vem depois de "conta"
            depois_conta = partes[1].strip()
            # Procura números nessa parte
            numeros_conta = re.search(r'(\d+)', depois_conta)
            if numeros_conta:
                resultado["conta"] = numeros_conta.group(1)
    
    return resultado


# ====== FUNÇÃO DE TESTE ======
def testar():
    """Testa o analisador com exemplos"""
    
    exemplos = [
        "compra 100 PETR4 conta 12345",
        "venda 50 VALE3",
        "notícias sobre ITSA4",
        "quero comprar 200 WEGE3",
        "vender 1000",
        "algo completamente diferente"
    ]
    
    print("🧪 TESTANDO ANALISADOR DE COMANDOS")
    print("=" * 50)
    
    for exemplo in exemplos:
        print(f"\n📝 Comando: '{exemplo}'")
        resultado = analisar_comando(exemplo)
        
        print(f"   Ação detectada: {resultado['acao']}")
        if resultado['ticker']:
            print(f"   Ticker: {resultado['ticker']}")
        if resultado['quantidade']:
            print(f"   Quantidade: {resultado['quantidade']}")
        if resultado['conta']:
            print(f"   Conta: {resultado['conta']}")


# Isso faz o teste rodar se executarmos o arquivo diretamente
if __name__ == "__main__":
    testar()
