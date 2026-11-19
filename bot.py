import os, json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [9228348493]

CHOOSE, PHOTO, NAME, PRICE = range(4)

# Барои Render Web Service - сомонаи қалбакӣ, то бот хомӯш нашавад
def keep_alive():
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive")
        def log_message(self, *a):
            pass
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), H).serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except:
    products = {}

def save():
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
