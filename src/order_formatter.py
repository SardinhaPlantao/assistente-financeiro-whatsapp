"""
Módulo que formata ordens financeiras para envio ao broker.
Transforma dados técnicos em mensagens claras e profissionais.
"""

def formatar_ordem(dados_ordem):
    """
    Recebe um dicionário com dados da ordem e retorna texto formatado.
    
    Exemplo de entrada:
    {
        "acao": "compra",
        "ticker": "PETR4",
        "quantidade": 100,
        "conta": "12345",
        "tipo": "mercado"  # opcional
    }
    
    Retorna uma string formatada para envio ao broker.
    """
    
    # Validação básica
    if not dados_ordem.get("ticker") or not dados_ordem.get("quantidade"):
        return "❌ ERRO: Dados incompletos para formatar ordem."
    
    # Pegar valores ou usar padrões
    acao = dados_ordem.get("acao", "compra").upper()
    ticker = dados_ordem.get("ticker", "DESCONHECIDO")
    quantidade = dados_ordem.get("quantidade", 0)
    conta = dados_ordem.get("conta", "NÃO INFORMADA")
    tipo_ordem = dados_ordem.get("tipo", "mercado").upper()
    
    # Construir mensagem formatada
    mensagem = f"""
╔══════════════════════════════════════════╗
║          📊 ORDEM FINANCEIRA              ║
╠══════════════════════════════════════════╣
║                                          ║
║  🔹 AÇÃO: {acao:<30} ║
║  🔹 ATIVO: {ticker:<29} ║
║  🔹 QUANTIDADE: {quantidade:<23} ║
║  🔹 TIPO: {tipo_ordem:<28} ║
║  🔹 CONTA: {conta:<28} ║
║                                          ║
║  📅 Data/Hora: AGORA                     ║
║  👤 Origem: Sistema Automático           ║
║                                          ║
╠══════════════════════════════════════════╣
║   ✅ CONFIRMAR EXECUÇÃO?                  ║
╚══════════════════════════════════════════╝
"""
    
    # Versão simples (sem bordas) para WhatsApp
    mensagem_simples = f"""
📊 *ORDEM {acao}*

• *Ativo:* {ticker}
• *Quantidade:* {quantidade}
• *Tipo:* {tipo_ordem}
• *Conta:* {conta}
• *Origem:* Sistema Automático

_Esta ordem está pronta para execução._
"""
    
    return mensagem_simples


def criar_mensagem_broker(dados_ordem):
    """
    Cria mensagem URGENTE para enviar diretamente ao broker via WhatsApp.
    Mais direta e objetiva.
    """
    
    acao = "COMPRA" if dados_ordem.get("acao") == "compra" else "VENDA"
    ticker = dados_ordem.get("ticker", "ERRO")
    quantidade = dados_ordem.get("quantidade", 0)
    conta = dados_ordem.get("conta", "NÃO INFORMADA")
    
    mensagem = f"""
🚨 *ORDEM URGENTE - EXECUTAR IMEDIATAMENTE*

{acao} {quantidade} {ticker}

📋 Detalhes:
• Conta cliente: {conta}
• Tipo: Mercado
• Prazo: Dia
• Origem: Sistema Automático

⚠️ Confirmar execução em até 2 minutos.
"""
    
    return mensagem


def validar_ordem(dados_ordem):
    """
    Valida se uma ordem tem todos os dados necessários.
    Retorna (True, "") se válida, ou (False, mensagem_erro) se inválida.
    """
    
    erros = []
    
    # Verificar ticker
    if not dados_ordem.get("ticker"):
        erros.append("❌ Ticker não especificado")
    elif len(dados_ordem["ticker"]) < 4:
        erros.append("❌ Ticker inválido")
    
    # Verificar quantidade
    quantidade = dados_ordem.get("quantidade")
    if not quantidade:
        erros.append("❌ Quantidade não especificada")
    elif not isinstance(quantidade, int):
        erros.append("❌ Quantidade deve ser número inteiro")
    elif quantidade <= 0:
        erros.append("❌ Quantidade deve ser maior que zero")
    elif quantidade > 100000:  # Limite razoável
        erros.append("⚠️ Quantidade muito alta - confirmar?")
    
    # Verificar ação
    acao = dados_ordem.get("acao", "").lower()
    if acao not in ["compra", "venda"]:
        erros.append("❌ Ação deve ser 'compra' ou 'venda'")
    
    if erros:
        return False, " | ".join(erros)
    else:
        return True, "✅ Ordem válida"


# ====== FUNÇÃO DE TESTE ======
def testar_formatador():
    """Testa todas as funções do formatador"""
    
    print("🧪 TESTANDO FORMATADOR DE ORDENS")
    print("=" * 50)
    
    # Exemplo de ordem
    ordem_teste = {
        "acao": "compra",
        "ticker": "PETR4",
        "quantidade": 100,
        "conta": "XP-12345",
        "tipo": "mercado"
    }
    
    print("\n1️⃣ Testando validação:")
    valido, mensagem = validar_ordem(ordem_teste)
    print(f"   Resultado: {mensagem}")
    
    print("\n2️⃣ Testando formatação básica:")
    formatado = formatar_ordem(ordem_teste)
    print(formatado)
    
    print("\n3️⃣ Testando mensagem para broker:")
    msg_broker = criar_mensagem_broker(ordem_teste)
    print(msg_broker)
    
    print("\n4️⃣ Testando ordem inválida:")
    ordem_invalida = {"acao": "compra", "ticker": "PET"}
    valido, mensagem = validar_ordem(ordem_invalida)
    print(f"   Resultado: {mensagem}")


# Executar testes se arquivo rodado diretamente
if __name__ == "__main__":
    testar_formatador()
