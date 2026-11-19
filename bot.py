import os, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [9228348493]
CHOOSE, PHOTO, NAME, PRICE_SOM, PRICE_DOL, PRICE_YUAN = range(6)

try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except:
    products = {}

def save():
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

# ===== ҲАМАИ ШОХАҲО - ПУРРА =====
CATEGORIES = {
    "cat1": {"name": "📱 1. Таҷҳизоти телефон", "subs": {
        "cat1_tel": {"name": "📱 Телефон", "brands": ["Apple / iPhone", "Samsung", "Xiaomi / Redmi", "Honor", "Huawei", "Vivo", "Oppo"]},
        "cat1_naush": {"name": "🎧 Наушник", "brands": ["1. Беспроводное", "2. Проводное"]},
        "cat1_zar": {"name": "🔌 Зарядник", "brands": ["Зарядник 20W", "Зарядник 33W", "Зарядник 67W", "Зарядник 120W"]},
        "cat1_kabel": {"name": "🔗 Кабел", "brands": ["Кабел Type-C", "Кабел Lightning", "Кабел Micro-USB"]},
        "cat1_chehol": {"name": "📱 Чехол", "brands": ["Чехол iPhone", "Чехол Samsung", "Чехол Xiaomi"]},
        "cat1_lam": {"name": "🛡️ Ламинат / Шиша", "brands": ["Шиша iPhone", "Шиша Samsung", "Шиша Xiaomi", "Ламинат"]},
    }},
    "cat2": {"name": "🍳 2. Таҷҳизоти ошхона", "subs": {
        "cat2_blender": {"name": "🥤 Блендер / Миксер", "brands": ["Xiaomi", "Philips", "Bosch"]},
        "cat2_chay": {"name": "🫖 Чойник / Кофеварка", "brands": ["Xiaomi", "Philips", "Tefal"]},
        "cat2_tabaq": {"name": "🍳 Табақ / Дег", "brands": ["Tefal", "Xiaomi", "Nodir"]},
        "cat2_kord": {"name": "🔪 Корд / Тахта", "brands": ["Корд", "Тахта", "Комплект"]},
    }},
    "cat3": {"name": "📺 3. Техникаи хона", "subs": {
        "cat3_tv": {"name": "📺 Телевизор", "brands": ["Samsung", "LG", "Xiaomi / Mi", "Hisense", "Artel"]},
        "cat3_hol": {"name": "🧊 Холодильник", "brands": ["Samsung", "LG", "Hisense", "Artel", "Bosch"]},
        "cat3_kond": {"name": "❄️ Кондиционер", "brands": ["Samsung", "LG", "Midea", "Hisense", "Artel"]},
        "cat3_jom": {"name": "👕 Мошинаи ҷомашӯӣ", "brands": ["Samsung", "LG", "Hisense", "Artel", "Bosch"]},
        "cat3_chang": {"name": "🧹 Чангкашак", "brands": ["Xiaomi", "Samsung", "Dyson"]},
    }},
    "cat4": {"name": "💻 4. Компьютер", "subs": {
        "cat4_note": {"name": "💻 Ноутбук", "brands": ["HP", "Lenovo", "Asus", "Apple MacBook", "Acer"]},
        "cat4_mon": {"name": "🖥️ Монитор", "brands": ["Samsung", "LG", "Xiaomi", "HP"]},
        "cat4_klav": {"name": "⌨️ Клавиатура / Мышка", "brands": ["Logitech", "Xiaomi", "HP"]},
        "cat4_kol": {"name": "🔊 Колонка", "brands": ["JBL", "Xiaomi", "Sony"]},
        "cat4_naush_pc": {"name": "🎧 Наушник компю
