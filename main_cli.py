#!/usr/bin/env python3
"""
ASSISTENTE FINANCEIRO - PROGRAMA PRINCIPAL

Este é o programa que você vai executar para testar o sistema.
Ele conecta todos os módulos:
1. intent_parser.py - entende o que você quer
2. order_formatter.py - formata ordens bonitas
3. (em breve) news_fetcher.py - busca notícias

Como usar:
1. Execute: python main_cli.py
2. Digite comandos como:
   - "compra 100 PETR4 conta 12345"
   - "notícias VALE3"
   - "venda 50 ITUB4"
3. Veja o sistema funcionando!
"""

# Importar nossos módulos
import sys
import os

# Adicionar a pasta 'src' ao caminho do Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Agora podemos importar nossos módulos
from intent_parser import analisar_comando
from order_formatter import formatar_ordem, criar_mensagem_broker, validar_ordem


def mostrar_banner():
    """Mostra um banner bonito quando o programa inicia"""
    
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║     🤖 ASSISTENTE FINANCEIRO WHATSAPP (MVP)          ║
    ║                                                      ║
    ║     Versão: 1.0.0-beta                               ║
    ║     Data: 2026                                       ║
    ║                                                      ║
    ╠══════════════════════════════════════════════════════╣
    ║                                                      ║
    ║  📝 COMANDOS SUPORTADOS:                             ║
    ║                                                      ║
    ║  • "compra 100 PETR4 conta 12345"                    ║
    ║  • "venda 50 VALE3"                                  ║
    ║  • "notícias ITSA4"                                  ║
    ║  • "sair" para encerrar                              ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    
    💡 Dica: Você pode copiar e colar os exemplos acima!
    """
    print(banner)


def processar_comando(comando):
    """
    Processa um comando do usuário usando todos os módulos
    """
    
    print(f"\n🔍 Analisando: '{comando}'")
    print("-" * 50)
    
    # 1. USAR O ANALISADOR PARA ENTENDER
    resultado = analisar_comando(comando)
    
    print(f"✅ Ação detectada: {resultado['acao']}")
    
    # 2. DECIDIR O QUE FAZER BASEADO NA AÇÃO
    if resultado['acao'] in ['compra', 'venda']:
        # É UMA ORDEM DE COMPRA/VENDA
        
        # Verificar se temos dados suficientes
        if not resultado['ticker']:
            print("❌ ERRO: Não consegui identificar o ticker (ex: PETR4)")
            return
        
        if not resultado['quantidade']:
            print("❌ ERRO: Não consegui identificar a quantidade")
            return
        
        print(f"   📊 Ticker: {resultado['ticker']}")
        print(f"   🔢 Quantidade: {resultado['quantidade']}")
        if resultado['conta']:
            print(f"   🏦 Conta: {resultado['conta']}")
        
        # Validar a ordem
        valido, mensagem = validar_ordem(resultado)
        print(f"   📋 Validação: {mensagem}")
        
        if valido:
            # Formatar ordem bonita
            ordem_formatada = formatar_ordem(resultado)
            print("\n💼 ORDEM FORMATADA PARA BROKER:")
            print("=" * 40)
            print(ordem_formatada)
            
            # Mostrar também versão WhatsApp
            print("\n📱 PRONTO PARA WHATSAPP:")
            print("-" * 30)
            msg_whatsapp = criar_mensagem_broker(resultado)
            print(msg_whatsapp)
            
            print("\n✅ Ação sugerida: Enviar esta mensagem ao broker via WhatsApp")
            
    elif resultado['acao'] == 'noticias':
        # É UM PEDIDO DE NOTÍCIAS
        if resultado['ticker']:
            print(f"📰 Buscando notícias para: {resultado['ticker']}")
            print("   (Módulo de notícias em desenvolvimento...)")
            print("   ⏳ Em breve: notícias reais da web!")
        else:
            print("📰 Notícias gerais do mercado")
            print("   (Módulo em desenvolvimento...)")
    
    else:
        # AÇÃO DESCONHECIDA
        print("🤔 Não entendi o comando.")
        print("💡 Tente:")
        print("   • 'compra 100 PETR4 conta 12345'")
        print("   • 'notícias VALE3'")
        print("   • 'venda 50 ITUB4'")


def modo_interativo():
    """Modo interativo: fica esperando comandos do usuário"""
    
    mostrar_banner()
    
    print("\n🎯 MODO INTERATIVO ATIVADO")
    print("   Digite 'sair' para encerrar")
    print("   Digite 'ajuda' para ver exemplos")
    print("=" * 50)
    
    while True:
        try:
            # Pedir comando ao usuário
            comando = input("\n💬 Digite um comando: ").strip()
            
            # Verificar se quer sair
            if comando.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\n👋 Encerrando assistente. Até logo!")
                break
            
            # Verificar se quer ajuda
            if comando.lower() in ['ajuda', 'help', '?']:
                mostrar_banner()
                continue
            
            # Processar o comando
            if comando:  # Se não for vazio
                processar_comando(comando)
            else:
                print("⚠️  Digite algo ou 'sair' para encerrar")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompido pelo usuário. Encerrando...")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            print("💡 Tente novamente ou digite 'sair'")


def modo_unico_comando(comando):
    """Modo para testar um único comando"""
    print(f"🚀 Testando comando: '{comando}'")
    print("=" * 50)
    processar_comando(comando)


# ====== PROGRAMA PRINCIPAL ======
if __name__ == "__main__":
    """
    Ponto de entrada do programa.
    Decide se roda em modo interativo ou comando único.
    """
    
    # Verificar se recebeu argumentos (modo comando único)
    if len(sys.argv) > 1:
        # Juntar todos os argumentos em um comando
        comando_teste = " ".join(sys.argv[1:])
        modo_unico_comando(comando_teste)
    else:
        # Modo interativo (padrão)
        modo_interativo()
