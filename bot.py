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

# ---------- КЛАВИАТУРАҲО ----------

def main_kb(is_admin=False):
    kb = [
        [InlineKeyboardButton("🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("📞 Алоқа", callback_data="contact")],
    ]
    if is_admin:
        kb.append([InlineKeyboardButton("⚙️ Панели админ", callback_data="admin")])
    return InlineKeyboardMarkup(kb)

def admin_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Иловаи маҳсулот", callback_data="add")],
        [InlineKeyboardButton("🗑 Нест кардани маҳсулот", callback_data="delete_list")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]
    ])

def categories_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Дастгоҳҳо", callback_data="cat_Дастгоҳҳо")],
        [InlineKeyboardButton("Дигар", callback_data="cat_Дигар")],
        [InlineKeyboardButton("❌ Бекор кардан", callback_data="cancel")]
    ])

# ---------- /start ----------

async def start(update, context):
    user_id = update.effective_user.id
    is_admin = user_id in ADMIN_IDS
    text = "Салом! 👋\nБа боти Дастгоҳ хуш омадед.\nМаҳсулотро интихоб кун:"
    if update.message:
        await update.message.reply_text(text, reply_markup=main_kb(is_admin))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_kb(is_admin))

async def contact(update, context):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("📞 Барои фармоиш: @asoevabubakr\n\n⬅️ Барои бозгашт /start -ро пахш кун", reply_markup=main_kb(q.from_user.id in ADMIN_IDS))

# ---------- КАТАЛОГ ----------

async def catalog(update, context):
    q = update.callback_query
    await q.answer()
    if not products:
        await q.edit_message_text("Ҳоло
