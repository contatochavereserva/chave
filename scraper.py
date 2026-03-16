import feedparser
import requests
import os
import sys
import hashlib

print("--- INICIANDO SCRAPER iAUTO ---", flush=True)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("🚨 ERRO: Chaves faltando!")
    sys.exit(1)

FEEDS = [
    {"nome": "Motor1", "url": "https://motor1.uol.com.br/rss/articles/all/"},
    {"nome": "Auto Esporte", "url": "https://autoesporte.globo.com/rss/autoesporte/"}
]

def enviar_telegram(titulo, link, veiculo):
    print(f"-> Tentando enviar: {titulo[:30]}...", flush=True)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Criamos um "ID curto" a partir do link para não estourar o limite de 64 bytes do Telegram
    link_hash = hashlib.md5(link.encode()).hexdigest()[:10]
    
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Aprovar", "callback_data": f"ap|{link_hash}"},
            {"text": "❌ Descartar", "callback_data": f"dc|{link_hash}"}
        ]]
    }
    
    # Colocamos o link completo visível na mensagem, para você clicar, mas não no botão
    texto = f"🆕 *{veiculo}*\n\n{titulo}\n\n🔗 [Link Original]({link})"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"   Resposta Telegram: {response.text}", flush=True)
        if not response.json().get('ok'):
            sys.exit(1)
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}", flush=True)
        sys.exit(1)

for feed in FEEDS:
    print(f"Lendo feed: {feed['nome']}...", flush=True)
    d = feedparser.parse(feed['url'])
    if not d.entries:
        print(f"   ⚠️ Nenhuma notícia encontrada em {feed['nome']}")
        continue
        
    entry = d.entries[0]
    enviar_telegram(entry.title, entry.link, feed['nome'])

print("--- FIM DO PROCESSO ---", flush=True)
