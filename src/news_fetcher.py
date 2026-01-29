"""
MÓDULO DE BUSCA DE NOTÍCIAS FINANCEIRAS

Busca notícias sobre ações e empresas usando web scraping (fins educacionais).
ATENÇÃO: Para uso comercial, substitua por APIs oficiais como:
- NewsAPI, Alpha Vantage, Yahoo Finance API, etc.
"""

import requests
import time
from bs4 import BeautifulSoup
import re

# Configurações importantes
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Sites educacionais para busca (apenas para aprendizado)
SITES_BUSCA = {
    'google_news': 'https://news.google.com/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419',
    'investing_br': 'https://br.investing.com/search/?q={query}',
    'infomoney': 'https://www.infomoney.com.br/?s={query}'
}


def criar_query_noticias(ticker, empresa=None):
    """
    Cria uma query de busca inteligente para notícias.
    
    Exemplo: PETR4 → "Petrobras OR PETR4 OR PETR3 notícias"
    """
    
    # Mapeamento de alguns tickers comuns para nomes de empresas
    ticker_para_empresa = {
        'PETR4': 'Petrobras', 'PETR3': 'Petrobras',
        'VALE3': 'Vale', 'VALE5': 'Vale',
        'ITUB4': 'Itaú Unibanco', 'ITUB3': 'Itaú',
        'BBDC4': 'Bradesco', 'BBDC3': 'Bradesco',
        'BBAS3': 'Banco do Brasil',
        'WEGE3': 'WEG',
        'B3SA3': 'B3 Bolsa Balcão',
        'ABEV3': 'Ambev',
        'MGLU3': 'Magazine Luiza',
        'VIIA3': 'Via'
    }
    
    # Usar empresa fornecida ou buscar no mapeamento
    nome_empresa = empresa if empresa else ticker_para_empresa.get(ticker, ticker)
    
    # Criar query de busca
    query = f'{nome_empresa} OR {ticker} "ações" OR "resultados" OR "dividendos"'
    
    return query


def buscar_noticias_google(query, max_noticias=5):
    """
    Busca notícias no Google News (APENAS PARA FINS EDUCACIONAIS).
    Retorna lista de dicionários com {titulo, link, fonte, data_relativa}
    """
    
    noticias = []
    
    try:
        # Montar URL
        url = SITES_BUSCA['google_news'].format(query=requests.utils.quote(query))
        
        print(f"🔍 Buscando: {url}")
        
        # Fazer requisição (com timeout para não travar)
        resposta = requests.get(url, headers=HEADERS, timeout=10)
        resposta.raise_for_status()  # Verificar se deu erro
        
        # Analisar HTML
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Encontrar notícias (seletores do Google News)
        artigos = soup.find_all('article', limit=max_noticias+5)
        
        for artigo in artigos[:max_noticias]:
            try:
                # Tentar encontrar título e link
                link_tag = artigo.find('a', href=True)
                if not link_tag:
                    continue
                
                titulo = link_tag.get_text(strip=True)
                link_relativo = link_tag['href']
                
                # Converter link relativo para absoluto
                if link_relativo.startswith('./'):
                    link = 'https://news.google.com' + link_relativo[1:]
                elif link_relativo.startswith('/'):
                    link = 'https://news.google.com' + link_relativo
                else:
                    link = link_relativo
                
                # Tentar encontrar fonte e tempo
                fonte_tag = artigo.find('div', string=re.compile(r'^\w'))
                fonte = fonte_tag.get_text(strip=True) if fonte_tag else "Fonte desconhecida"
                
                tempo_tag = artigo.find('time')
                tempo = tempo_tag.get_text(strip=True) if tempo_tag else "Há algum tempo"
                
                # Adicionar à lista
                noticias.append({
                    'titulo': titulo,
                    'link': link,
                    'fonte': fonte,
                    'tempo': tempo,
                    'query': query
                })
                
            except Exception as e:
                # Ignorar erros em artigos individuais
                continue
        
        # Se não encontrou notícias no formato esperado, tentar método alternativo
        if not noticias:
            # Buscar por headings
            for h3 in soup.find_all('h3', limit=max_noticias):
                link_tag = h3.find_parent('a', href=True)
                if link_tag:
                    noticias.append({
                        'titulo': h3.get_text(strip=True),
                        'link': 'https://news.google.com' + link_tag['href'] if link_tag['href'].startswith('./') else link_tag['href'],
                        'fonte': 'Google News',
                        'tempo': 'Recente',
                        'query': query
                    })
                
    except Exception as e:
        print(f"⚠️ Erro ao buscar no Google News: {e}")
        # Retornar notícias de fallback (simuladas)
        noticias = criar_noticias_fallback(query, max_noticias)
    
    return noticias


def criar_noticias_fallback(query, max_noticias=3):
    """
    Cria notícias simuladas quando a busca real falha.
    Útil para desenvolvimento e testes.
    """
    
    # Extrair ticker da query
    ticker_match = re.search(r'([A-Z]{4}\d{1,2})', query)
    ticker = ticker_match.group(1) if ticker_match else "AÇÃO"
    
    noticias_simuladas = [
        {
            'titulo': f'Resultados do trimestre da {ticker} superam expectativas do mercado',
            'link': f'https://exemplo.com/noticias/{ticker.lower()}-resultados',
            'fonte': 'Simulado para Desenvolvimento',
            'tempo': 'Hoje',
            'query': query,
            'simulado': True
        },
        {
            'titulo': f'Analistas recomendam compra de {ticker} com alta de 15% no preço-alvo',
            'link': f'https://exemplo.com/analise/{ticker.lower()}-recomendacao',
            'fonte': 'Simulado para Desenvolvimento',
            'tempo': 'Ontem',
            'query': query,
            'simulado': True
        },
        {
            'titulo': f'{ticker} anuncia pagamento de dividendos acima da média do setor',
            'link': f'https://exemplo.com/dividendos/{ticker.lower()}-dividendos',
            'fonte': 'Simulado para Desenvolvimento',
            'tempo': '2 dias atrás',
            'query': query,
            'simulado': True
        }
    ]
    
    return noticias_simuladas[:max_noticias]


def formatar_noticias_para_whatsapp(noticias, ticker):
    """
    Formata notícias em uma mensagem bonita para WhatsApp.
    """
    
    if not noticias:
        return f"📭 Nenhuma notícia recente encontrada para {ticker}."
    
    mensagem = f"📰 *ÚLTIMAS NOTÍCIAS - {ticker}*\n\n"
    
    for i, noticia in enumerate(noticias[:5], 1):
        emoji = "🟢" if i == 1 else "🔵" if i == 2 else "⚪"
        
        # Encurtar título se muito longo
        titulo = noticia['titulo']
        if len(titulo) > 80:
            titulo = titulo[:77] + "..."
        
        mensagem += f"{emoji} *{titulo}*\n"
        
        # Adicionar fonte e tempo se disponíveis
        if noticia.get('simulado'):
            mensagem += f"   ⏳ {noticia['tempo']} | 📰 {noticia['fonte']}\n"
        else:
            if noticia.get('fonte') and noticia.get('tempo'):
                mensagem += f"   ⏳ {noticia['tempo']} | 📰 {noticia['fonte']}\n"
        
        # Adicionar link (encurtado)
        if noticia.get('link'):
            link_display = noticia['link'][:50] + "..." if len(noticia['link']) > 50 else noticia['link']
            mensagem += f"   🔗 {link_display}\n"
        
        mensagem += "\n"
    
    mensagem += f"📊 *Total:* {len(noticias)} notícias encontradas\n"
    mensagem += "⚠️ *Nota:* Para fins educacionais. Em produção, use APIs oficiais."
    
    return mensagem


def buscar_noticias_por_ticker(ticker, max_noticias=5):
    """
    Função principal: busca notícias para um ticker específico.
    """
    
    print(f"🔎 Iniciando busca por notícias de {ticker}...")
    
    try:
        # 1. Criar query de busca
        query = criar_query_noticias(ticker)
        print(f"   Query: {query}")
        
        # 2. Buscar notícias (Google News - fins educacionais)
        print("   Buscando no Google News...")
        noticias = buscar_noticias_google(query, max_noticias)
        
        # 3. Se não encontrou, usar fallback
        if not noticias:
            print("   Usando notícias simuladas para desenvolvimento...")
            noticias = criar_noticias_fallback(query, max_noticias)
        
        print(f"   ✅ Encontradas {len(noticias)} notícias")
        
        # 4. Formatar para retorno
        resultado = {
            'ticker': ticker,
            'query': query,
            'total_noticias': len(noticias),
            'noticias': noticias,
            'formatado_whatsapp': formatar_noticias_para_whatsapp(noticias, ticker)
        }
        
        return resultado
        
    except Exception as e:
        print(f"❌ Erro na busca de notícias: {e}")
        
        # Retornar fallback em caso de erro
        return {
            'ticker': ticker,
            'query': 'FALHA',
            'total_noticias': 0,
            'noticias': [],
            'formatado_whatsapp': f"❌ Erro ao buscar notícias para {ticker}.\n\nMotivo: {str(e)[:100]}...\n\nTente novamente mais tarde.",
            'erro': str(e)
        }


# ====== FUNÇÃO DE TESTE ======
def testar_busca_noticias():
    """Testa o módulo de busca de notícias"""
    
    print("🧪 TESTANDO BUSCADOR DE NOTÍCIAS")
    print("=" * 50)
    
    # Testar com alguns tickers
    tickers_teste = ['PETR4', 'VALE3', 'ITUB4', 'XYZ123']  # Último é inválido
    
    for ticker in tickers_teste:
        print(f"\n📊 Testando para: {ticker}")
        print("-" * 30)
        
        resultado = buscar_noticias_por_ticker(ticker, max_noticias=3)
        
        print(f"\n📈 Resultado:")
        print(f"   Ticker: {resultado['ticker']}")
        print(f"   Notícias encontradas: {resultado['total_noticias']}")
        
        if resultado['noticias']:
            print("\n   📰 Primeira notícia:")
            print(f"      Título: {resultado['noticias'][0]['titulo'][:60]}...")
            print(f"      Fonte: {resultado['noticias'][0].get('fonte', 'N/A')}")
        
        # Mostrar preview da mensagem WhatsApp
        print("\n   💬 Preview WhatsApp (primeiras 2 linhas):")
        linhas = resultado['formatado_whatsapp'].split('\n')
        for linha in linhas[:2]:
            print(f"      {linha}")
        
        print("\n" + "=" * 50)


# Executar teste se rodar arquivo diretamente
if __name__ == "__main__":
    testar_busca_noticias()
    
    # Mostrar aviso importante
    print("\n" + "⚠️" * 30)
    print("AVISO LEGAL IMPORTANTE:")
    print("-" * 40)
    print("Este módulo usa web scraping APENAS para fins educacionais.")
    print("Para uso em produção:")
    print("1. Use APIs oficiais (NewsAPI, Alpha Vantage, etc.)")
    print("2. Respeite os termos de serviço dos sites")
    print("3. Considere limitações de rate limiting")
    print("4. Implemente cache para evitar excesso de requisições")
    print("⚠️" * 30)
