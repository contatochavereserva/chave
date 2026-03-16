import feedparser
import requests
import os
import sys

# Força o Python a mostrar as mensagens na hora
print("--- INICIANDO SCRAPER iAUTO ---", flush=True)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# Verificação básica de chaves
if not TOKEN or not CHAT_ID:
    print(f"🚨 ERRO: Chaves faltando! TOKEN: {'OK' if TOKEN else 'FALTA'}, CHAT_ID: {'OK' if CHAT_ID else 'FALTA'}")
    sys.exit(1)

FEEDS = [
    {"nome": "Motor1", "url": "https://motor1.uol.com.br/rss/articles/all/"},
    {"nome": "Auto Esporte", "url": "https://autoesporte.globo.com/rss/autoesporte/"}
]

def enviar_telegram(titulo, link, veiculo):
    print(f"-> Tentando enviar: {titulo[:30]}...", flush=True)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Aprovar", "callback_data": f"aprovar|{link}"},
            {"text": "❌ Descartar", "callback_data": f"descartar|{link}"}
        ]]
    }
    
    payload = {
        "chat_id": CHAT_ID,
        "text": f"🆕 *{veiculo}*\n\n{titulo}\n\n[Ler matéria]({link})",
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

# Execução
for feed in FEEDS:
    print(f"Lendo feed: {feed['nome']}...", flush=True)
    d = feedparser.parse(feed['url'])
    if not d.entries:
        print(f"   ⚠️ Nenhuma notícia encontrada em {feed['nome']}")
        continue
        
    # Pega a primeira notícia
    entry = d.entries[0]
    enviar_telegram(entry.title, entry.link, feed['nome'])

print("--- FIM DO PROCESSO ---", flush=True)
