import os, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [9228348493]

CHOOSE, PHOTO, NAME, PRICE = range(4)

try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except:
    products = {}

def save():
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False)

START_TEXT = "Салом хуш омадед ба интернет магазини мо! Пеш аз ҳама хотиррасон мекунем борҳои як қисм дар Тоҷикистон ҳаст ва як қисм дар давлати чин!\n\nЯке аз ин борҳои ки харид мекунед интихоб намоед"

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1. Техникаҳо барои хона", callback_data="cat1")],
        [InlineKeyboardButton("2. Телефонҳо ва камераҳо", callback_data="cat2")],
        [InlineKeyboardButton("3. Компитерҳо, ноутбукҳо ва таҷҳизоти онҳо", callback_data="cat3")],
        [InlineKeyboardButton("4. Худам заказ мекунам", callback_data="cat4")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, reply_markup=main_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    if d == "back":
        await q.edit_message_text(START_TEXT, reply_markup=main_menu())
        return
    if d == "cat1":
        kb = [
            [InlineKeyboardButton("1. Телефонҳои мобилӣ", callback_data="sub1_1")],
            [InlineKeyboardButton("2. Телефонҳои симдор", callback_data="sub1_2")],
            [InlineKeyboardButton("3. Камераҳои назорати", callback_data="sub1_3")],
            [InlineKeyboardButton("4. Камера барои блогерон ва таҷҳизоти иловагӣ", callback_data="sub1_4")],
            [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")],
        ]
        await q.edit_message_text("Категорияи 1 - Техникаҳо барои хона:\n\nИнтихоб кунед:", reply_markup=InlineKeyboardMarkup(kb))
        return
    if d.startswith("sub1_"):
        items = products.get(d, [])
        if not items:
            await q.edit_message_text("Дар ин қисм ҳоло бор нест. Ба зудӣ илова мешавад. 📦\n\nБарои бозгашт /start-ро пахш кунед.")
            return
        await q.edit_message_text(f"Дар ин қисм {len(items)} бор ҳаст:")
        for it in items:
            await context.bot.send_photo(chat_id=q.message.chat_id, photo=it["photo"], caption=f"📦 {it['name']}\n💰 Нарх: {it['price']}")
        return
    if d in ["cat2","cat3","cat4"]:
        await q.edit_message_text("Ин категория ҳоло дар кор аст, ба зудӣ илова мешавад. ⏳\n\nБарои бозгашт /start-ро пахш кунед.")

async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Ту админ нестӣ! ❌")
        return ConversationHandler
