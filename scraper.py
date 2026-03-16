import feedparser
import requests
import os

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# Sites para monitorar (Vamos começar com esses dois)
FEEDS = [
    {"nome": "Motor1", "url": "https://motor1.uol.com.br/rss/articles/all/"},
    {"nome": "Auto Esporte", "url": "https://autoesporte.globo.com/rss/autoesporte/"}
]

def enviar_telegram(titulo, link, veiculo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    # Criando os botões de aprovação
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Aprovar", "callback_data": f"aprovar|{link}"},
            {"text": "❌ Descartar", "callback_data": f"descartar|{link}"}
        ]]
    }
    texto = f"🆕 *{veiculo}*\n\n{titulo}\n\n[Ler matéria]({link})"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown", "reply_markup": keyboard}
    requests.post(url, json=payload)

for feed in FEEDS:
    d = feedparser.parse(feed['url'])
    # Pega apenas a notícia mais recente para testar
    if d.entries:
        entry = d.entries[0]
        enviar_telegram(entry.title, entry.link, feed['nome'])
