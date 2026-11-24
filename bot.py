# ============================================================
# MAGOZAITOJIK_BOT - Боти пурраи Мағоза
# Зиёда аз 800 сатр | Render Free | Python + TeleBot
# ============================================================
import os
import threading
import json
import datetime
from flask import Flask
import telebot
from telebot import types

# ---------------- 1. ТАНЗИМОТ ----------------
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 8975989959  # <-- ID-и худро дар ин ҷо навиш
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is alive! Magozai Tojik"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

# ---------------- 2. МАЪЛУМОТ ----------------
USERS = {}
CARTS = {}
ORDERS = []
PRODUCTS = {}

# Категория 1 - Либос
PRODUCTS[1] = {"name": "Куртаи мардона", "price": 150, "cat": "Либос", "desc": "Куртаи сифати баланд, пахтагӣ", "photo": "", "stock": 20}
PRODUCTS[2] = {"name": "Куртаи занона", "price": 180, "cat": "Либос", "desc": "Куртаи зебо, нақшҳои миллӣ", "photo": "", "stock": 15}
PRODUCTS[3] = {"name": "Шим", "price": 120, "cat": "Либос", "desc": "Шими ҷинси, ҳама андоза", "photo": "", "stock": 30}
PRODUCTS[4] = {"name": "Футболка", "price": 80, "cat": "Либос", "desc": "Футболкаи пахтагӣ, сафед/сиёҳ", "photo": "", "stock": 50}
PRODUCTS[5] = {"name": "Койфта", "price": 200, "cat": "Либос", "desc": "Койфтаи гарм, зимистона", "photo": "", "stock": 10}
PRODUCTS[6] = {"name": "Доман", "price": 250, "cat": "Либос", "desc": "Домани атлас, тӯйёна", "photo": "", "stock": 8}
PRODUCTS[7] = {"name": "Чапан", "price": 300, "cat": "Либос", "desc": "Чапани миллӣ, дастӣ", "photo": "", "stock": 5}
PRODUCTS[8] = {"name": "Рӯймол", "price": 60, "cat": "Либос", "desc": "Рӯймоли атлас, гулдор", "photo": "", "stock": 40}
PRODUCTS[9] = {"name": "Ҷома", "price": 170, "cat": "Либос", "desc": "Ҷомаи мардона, тоза", "photo": "", "stock": 12}
PRODUCTS[10] = {"name": "Кулӯла", "price": 45, "cat": "Либос", "desc": "Кулӯлаи пахтагӣ", "photo": "", "stock": 60}
# Категория 2 - Телефон ва Техника
PRODUCTS[11] = {"name": "Samsung A15", "price": 1800, "cat": "Техника", "desc": "Телефони нав, 128GB", "photo": "", "stock": 7}
PRODUCTS[12] = {"name": "Redmi Note 13", "price": 2100, "cat": "Техника", "desc": "Камераи 108MP, 256GB", "photo": "", "stock": 6}
PRODUCTS[13] = {"name": "iPhone 13", "price": 5500, "cat": "Техника", "desc": "iPhone оригинал, 128GB", "photo": "", "stock": 3}
PRODUCTS[14] = {"name": "Наушник AirPods", "price": 350, "cat": "Техника", "desc": "Наушники бесим", "photo": "", "stock": 25}
PRODUCTS[15] = {"name": "Соат Smart Watch", "price": 450, "cat": "Техника", "desc": "Соати ҳушманд, пульс", "photo": "", "stock": 18}
PRODUCTS[16] = {"name": "Пуркунанда", "price": 90, "cat": "Техника", "desc": "Зарядник зуд, 25W", "photo": "", "stock": 100}
PRODUCTS[17] = {"name": "Чехол", "price": 50, "cat": "Техника", "desc": "Чехол барои ҳама модел", "photo": "", "stock": 80}
PRODUCTS[18] = {"name": "Колонка JBL", "price": 600, "cat": "Техника", "desc": "Колонкаи пурқувват", "photo": "", "stock": 9}
PRODUCTS[19] = {"name": "Ноутбук HP", "price": 4500, "cat": "Техника", "desc": "Ноутбук, 8GB RAM, SSD", "photo": "", "stock": 4}
PRODUCTS[20] = {"name": "Клавиатура", "price": 150, "cat": "Техника", "desc": "Клавиатура + муш", "photo": "", "stock": 20}
# Категория 3 - Хӯрок
PRODUCTS[21] = {"name": "Асал", "price": 120, "cat": "Хӯрок", "desc": "Асали кӯҳӣ, 1 кг", "photo": "", "stock": 30}
PRODUCTS[22] = {"name": "Қурут", "price": 40, "cat": "Хӯрок", "desc": "Қурути тоҷикӣ", "photo": "", "stock": 100}
PRODUCTS[23] = {"name": "Мурғ", "price": 55, "cat": "Хӯрок", "desc": "Гӯшти мурғ, 1 кг", "photo": "", "stock": 50}
PRODUCTS[24] = {"name": "Биринҷ", "price": 35, "cat": "Хӯрок", "desc": "Биринҷи девзира", "photo": "", "stock": 200}
PRODUCTS[25] = {"name": "Равғани зайтун", "price": 90, "cat": "Хӯрок", "desc": "Равғани табиӣ", "photo": "", "stock": 40}
PRODUCTS[26] = {"name": "Чой", "price": 25, "cat": "Хӯрок", "desc": "Чойи сабз, 500гр", "photo": "", "stock": 90}
PRODUCTS[27] = {"name": "Қаҳва", "price": 70, "cat": "Хӯрок", "desc": "Қаҳваи арабӣ", "photo": "", "stock": 60}
PRODUCTS[28] = {"name": "Шоколад", "price": 30, "cat": "Хӯрок", "desc": "Шоколади ширӣ", "photo": "", "stock": 120}
PRODUCTS[29] = {"name": "Мева хушк", "price": 80, "cat": "Хӯрок", "desc": "Мавиз, зардолу", "photo": "", "stock": 70}
PRODUCTS[30] = {"name": "Нон", "price": 5, "cat": "Хӯрок", "desc": "Нони гарм, танӯрӣ", "photo": "", "stock": 500}
# Категория 4 - Косметика
PRODUCTS[31] = {"name": "Крем рӯй", "price": 110, "cat": "Косметика", "desc": "Креми намнок", "photo": "", "stock": 35}
PRODUCTS[32] = {"name": "Атр", "price": 220, "cat": "Косметика", "desc": "Атри хушбӯй, 100мл", "photo": "", "stock": 15}
PRODUCTS[33] = {"name": "Лаб-ранг", "price": 65, "cat": "Косметика", "desc": "Лаб-ранги қимат", "photo": "", "stock": 50}
PRODUCTS[34] = {"name": "Шампун", "price": 55, "cat": "Косметика", "desc": "Шампуни мӯй", "photo": "", "stock": 80}
PRODUCTS[35] = {"name": "Собун", "price": 20, "cat": "Косметика", "desc": "Собуни табиӣ", "photo": "", "stock": 200}
PRODUCTS[36] = {"name": "Маска", "price": 40, "cat": "Косметика", "desc": "Маскаи рӯй", "photo": "", "stock": 90}
PRODUCTS[37] = {"name": "Лак", "price": 35, "cat": "Косметика", "desc": "Лаки нохун", "photo": "", "stock": 70}
PRODUCTS[38] = {"name": "Ойина", "price": 75, "cat": "Косметика", "desc": "Ойинаи зебо", "photo": "", "stock": 25}
PRODUCTS[39] = {"name": "Хати чашм", "price": 30, "cat": "Косметика", "desc": "Хати чашм, сиёҳ", "photo": "", "stock": 60}
PRODUCTS[40] = {"name": "Утюг мӯй", "price": 180, "cat": "Косметика", "desc": "Утюг барои мӯй", "photo": "", "stock": 12}
# Категория 5 - Хона
PRODUCTS[41] = {"name": "Қолин", "price": 900, "cat": "Хона", "desc": "Қолини дастӣ", "photo": "", "stock": 5}
PRODUCTS[42] = {"name": "Кӯрпа", "price": 250, "cat": "Хона", "desc": "Кӯрпаи пахтагӣ", "photo": "", "stock": 20}
PRODUCTS[43] = {"name": "Болишт", "price": 80, "cat": "Хона", "desc": "Болишти нарм", "photo": "", "stock": 40}
PRODUCTS[44] = {"name": "Дег", "price": 150, "cat": "Хона", "desc": "Деги калон, 10л", "photo": "", "stock": 15}
PRODUCTS[45] = {"name": "Табақ", "price": 60, "cat": "Хона", "desc": "Табақи чинӣ", "photo": "", "stock": 100}
PRODUCTS[46] = {"name": "Пиёла", "price": 35, "cat": "Хона", "desc": "Пиёлаи чой, 6 дона", "photo": "", "stock": 80}
PRODUCTS[47] = {"name": "Чойник", "price": 120, "cat": "Хона", "desc": "Чойники барқӣ", "photo": "", "stock": 18}
PRODUCTS[48] = {"name": "Лампа", "price": 95, "cat": "Хона", "desc": "Лампаи мизи", "photo": "", "stock": 30}
PRODUCTS[49] = {"name": "Парда", "price": 180, "cat": "Хона", "desc": "Пардаи зебо", "photo": "", "stock": 14}
PRODUCTS[50] = {"name": "Соат деворӣ", "price": 130, "cat": "Хона", "desc": "Соати деворӣ", "photo": "", "stock": 22}
# Категория 6 - Варзиш
PRODUCTS[51] = {"name": "Тӯб", "price": 90, "cat": "Варзиш", "desc": "Тӯби футбол", "photo": "", "stock": 30}
PRODUCTS[52] = {"name": "Кроссовка", "price": 280, "cat": "Варзиш", "desc": "Кроссовкаи варзишӣ", "photo": "", "stock": 16}
PRODUCTS[53] = {"name": "Форма", "price": 160, "cat": "Варзиш", "desc": "Формаи варзишӣ", "photo": "", "stock": 20}
PRODUCTS[54] = {"name": "Гантел", "price": 140, "cat": "Варзиш", "desc": "Гантел 5кг", "photo": "", "stock": 12}
PRODUCTS[55] = {"name": "Ресмон", "price": 40, "cat": "Варзиш", "desc": "Ресмони ҷаҳидан", "photo": "", "stock": 50}
PRODUCTS[56] = {"name": "Сумка варзишӣ", "price": 110, "cat": "Варзиш", "desc": "Сумкаи калон", "photo": "", "stock": 25}
PRODUCTS[57] = {"name": "Велосипед", "price": 1500, "cat": "Варзиш", "desc": "Велосипеди нав", "photo": "", "stock": 3}
PRODUCTS[58] = {"name": "Ракетка", "price": 120, "cat": "Варзиш", "desc": "Ракеткаи теннис", "photo": "", "stock": 18}
PRODUCTS[59] = {"name": "Шлем", "price": 200, "cat": "Варзиш", "desc": "Шлеми велосипед", "photo": "", "stock": 10}
PRODUCTS[60] = {"name": "Коврик йога", "price": 70, "cat": "Варзиш", "desc": "Коврик барои йога", "photo": "", "stock": 35}
# Категория 7 - Китоб
PRODUCTS[61] = {"name": "Китоби Тоҷикӣ", "price": 45, "cat": "Китоб", "desc": "Адабиёти тоҷик", "photo": "", "stock": 60}
PRODUCTS[62] = {"name": "Қуръон", "price": 120, "cat": "Китоб", "desc": "Қуръони карим", "photo": "", "stock": 20}
PRODUCTS[63] = {"name": "Луғат", "price": 60, "cat": "Китоб", "desc": "Луғати тоҷикӣ-русӣ", "photo": "", "stock": 30}
PRODUCTS[64] = {"name": "Китоби кӯдакона", "price": 35, "cat": "Китоб", "desc": "Афсонаҳо", "photo": "", "stock": 80}
PRODUCTS[65] = {"name": "Дафтар", "price": 15, "cat": "Китоб", "desc": "Дафтари 96 варақ", "photo": "", "stock": 200}
PRODUCTS[66] = {"name": "Қалам", "price": 10, "cat": "Китоб", "desc": "Қалами кабуд", "photo": "", "stock": 500}
PRODUCTS[67] = {"name": "Ранга", "price": 25, "cat": "Китоб", "desc": "Қаламҳои ранга", "photo": "", "stock": 100}
PRODUCTS[68] = {"name": "Сумка мактабӣ", "price": 150, "cat": "Китоб", "desc": "Сумка барои мактаб", "photo": "", "stock": 20}
PRODUCTS[69] = {"name": "Китоби ошпазӣ", "price": 55, "cat": "Китоб", "desc": "Таомҳои тоҷикӣ", "photo": "", "stock": 25}
PRODUCTS[70] = {"name": "Атлас", "price": 40, "cat": "Китоб", "desc": "Атласи ҷаҳон", "photo": "", "stock": 15}
# Категория 8 - Бозича
PRODUCTS[71] = {"name": "Мошинча", "price": 60, "cat": "Бозича", "desc": "Мошинчаи бозича", "photo": "", "stock": 40}
PRODUCTS[72] = {"name": "Лӯхтак", "price": 80, "cat": "Бозича", "desc": "Лӯхтаки зебо", "photo": "", "stock": 30}
PRODUCTS[73] = {"name": "Конструктор", "price": 120, "cat": "Бозича", "desc": "Лего, 200 дона", "photo": "", "stock": 20}
PRODUCTS[74] = {"name": "Тӯбча", "price": 20, "cat": "Бозича", "desc": "Тӯбчаи ранга", "photo": "", "stock": 100}
PRODUCTS[75] = {"name": "Дрон", "price": 800, "cat": "Бозича", "desc": "Дрони камерадор", "photo": "", "stock": 5}
PRODUCTS[76] = {"name": "Пазл", "price": 45, "cat": "Бозича", "desc": "Пазл 500 дона", "photo": "", "stock": 35}
PRODUCTS[77] = {"name": "Хирс", "price": 95, "cat": "Бозича", "desc": "Хирси нарм, калон", "photo": "", "stock": 18}
PRODUCTS[78] = {"name": "Гитара", "price": 250, "cat": "Бозича", "desc": "Гитараи кӯдакона", "photo": "", "stock": 8}
PRODUCTS[79] = {"name": "Шашка", "price": 30, "cat": "Бозича", "desc": "Шашка + Шоҳмот", "photo": "", "stock": 50}
PRODUCTS[80] = {"name": "Робот", "price": 180, "cat": "Бозича", "desc": "Роботи ҳушманд", "photo": "", "stock": 12}
# ---------------- 3. КЛАВИАТУРАҲО ----------------
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Каталог", "🛒 Сабад")
    kb.add("🔍 Ҷустуҷӯ", "📦 Фармоишҳои ман")
    kb.add("⭐ Тахфифҳо", "📞 Алоқа")
    kb.add("ℹ️ Дар бораи мо", "👤 Профили ман")
    return kb

def cats_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("👕 Либос", callback_data="cat_Либос"))
    kb.add(types.InlineKeyboardButton("📱 Техника", callback_data="cat_Техника"))
    kb.add(types.InlineKeyboardButton("🍯 Хӯрок", callback_data="cat_Хӯрок"))
    kb.add(types.InlineKeyboardButton("💄 Косметика", callback_data="cat_Косметика"))
    kb.add(types.InlineKeyboardButton("🏠 Хона", callback_data="cat_Хона"))
    kb.add(types.InlineKeyboardButton("⚽ Варзиш", callback_data="cat_Варзиш"))
    kb.add(types.InlineKeyboardButton("📚 Китоб", callback_data="cat_Китоб"))
    kb.add(types.InlineKeyboardButton("🧸 Бозича", callback_data="cat_Бозича"))
    kb.add(types.InlineKeyboardButton("🔙 Меню", callback_data="back_main"))
    return kb

def products_menu(cat):
    kb = types.InlineKeyboardMarkup()
    for pid, p in PRODUCTS.items():
        if p["cat"] == cat:
            kb.add(types.InlineKeyboardButton(f"{p['name']} - {p['price']} с", callback_data=f"prod_{pid}"))
    kb.add(types.InlineKeyboardButton("🔙 Категорияҳо", callback_data="back_cats"))
    return kb

def product_menu(pid):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🛒 Ба сабад илова кун", callback_data=f"add_{pid}"))
    kb.add(types.InlineKeyboardButton("➕ 1 дона", callback_data=f"add_{pid}"), types.InlineKeyboardButton("➕ 2 дона", callback_data=f"add2_{pid}"))
    kb.add(types.InlineKeyboardButton("🔙 Бозгашт", callback_data=f"cat_{PRODUCTS[pid]['cat']}"))
    return kb

def cart_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Фармоиш додан", callback_data="checkout"))
    kb.add(types.InlineKeyboardButton("🗑 Сабадро тоза кун", callback_data="clear_cart"))
    kb.add(types.InlineKeyboardButton("🔙 Меню", callback_data="back_main"))
    return kb

def admin_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"))
    kb.add(types.InlineKeyboardButton("📦 Ҳама фармоишҳо", callback_data="admin_orders"))
    kb.add(types.InlineKeyboardButton("👥 Истифодабарандагон", callback_data="admin_users"))
    kb.add(types.InlineKeyboardButton("📢 Паёми оммавӣ", callback_data="admin_broadcast"))
    kb.add(types.InlineKeyboardButton("➕ Мол илова кун", callback_data="admin_add"))
    return kb

# ---------------- 4. ЁРДАМЧӢ ----------------
def get_cart(uid):
    if uid not in CARTS:
        CARTS[uid] = {}
    return CARTS[uid]

def cart_total(uid):
    total = 0
    cart = get_cart(uid)
    for pid, qty in cart.items():
        if pid in PRODUCTS:
            total += PRODUCTS[pid]["price"] * qty
    return total

def cart_text(uid):
    cart = get_cart(uid)
    if not cart:
        return "Сабади шумо холӣ аст! 🛒\nБарои харидорӣ ба Каталог гузаред."
    txt = "🛒 Сабади шумо:\n\n"
    for pid, qty in cart.items():
        p = PRODUCTS.get(pid)
        if p:
            txt += f"• {p['name']} x{qty} = {p['price']*qty} сомонӣ\n"
    txt += f"\n💰 Ҷамъ: {cart_total(uid)} сомонӣ"
    txt += "\n🚚 Доставка: 20 сомонӣ (Душанбе)"
    txt += f"\n💳 Ҷамъ бо доставка: {cart_total(uid)+20} сомонӣ"
    return txt

def save_user(user):
    USERS[user.id] = {"name": user.first_name, "username": user.username, "date": str(datetime.datetime.now())}

# ---------------- 5. /start ----------------
@bot.message_handler(commands=['start'])
def start_cmd(m):
    save_user(m.from_user)
    txt = f"Салом, {m.from_user.first_name}! 👋\n\n"
    txt += "Хуш омадед ба **Мағозаи Тоҷик**! 🇹🇯\n\n"
    txt += "🛍 Зиёда аз 80 мол\n"
    txt += "💰 Нархҳои арзон\n"
    txt += "🚚 Доставка дар тамоми Тоҷикистон\n"
    txt += "⭐ Тахфифҳо ҳар ҳафта\n\n"
    txt += "Барои оғоз Каталогро интихоб кунед 👇"
    bot.send_message(m.chat.id, txt, reply_markup=main_menu())

@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.send_message(m.chat.id, "Ёрдам:\n/start - Оғоз\n/catalog - Каталог\n/cart - Сабад\n/admin - Админ\nБарои фармоиш: Каталог -> Мол -> Ба сабад -> Фармоиш")

@bot.message_handler(commands=['catalog'])
def catalog_cmd(m):
    bot.send_message(m.chat.id, "Категорияро интихоб кунед:", reply_markup=cats_menu())

@bot.message_handler(commands=['cart'])
def cart_cmd(m):
    bot.send_message(m.chat.id, cart_text(m.from_user.id), reply_markup=cart_menu())

@bot.message_handler(commands=['admin'])
def admin_cmd(m):
    if m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, "Админ-панел:", reply_markup=admin_menu())
    else:
        bot.send_message(m.chat.id, "Шумо админ нестед!")

# ---------------- 6. ТЕКСТҲО ----------------
@bot.message_handler(func=lambda m: m.text == "🛍 Каталог")
def btn_catalog(m):
    bot.send_message(m.chat.id, "Категорияро интихоб кунед:", reply_markup=cats_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 Сабад")
def btn_cart(m):
    bot.send_message(m.chat.id, cart_text(m.from_user.id), reply_markup=cart_menu())

@bot.message_handler(func=lambda m: m.text == "⭐ Тахфифҳо")
def btn_sale(m):
    txt = "⭐ ТАХФИФҲОИ ҲАФТА:\n\n"
    txt += "• Ҳама либос -20%\n• Техника -10%\n• Хӯрок -15%\n• Ҳангоми харидории 3 мол - 1 мол ТУҲФА!\n\n"
    txt += "Код: SALE20\n"
    bot.send_message(m.chat.id, txt)

@bot.message_handler(func=lambda m: m.text == "📞 Алоқа")
def btn_contact(m):
    bot.send_message(m.chat.id, "📞 Алоқа:\nТелефон: +992 900 00 00 00\nTelegram: @magozaitojik\nСурога: Душанбе, кӯчаи Рӯдакӣ 123\nСоат: 9:00 - 21:00")

@bot.message_handler(func=lambda m: m.text == "ℹ️ Дар бораи мо")
def btn_about(m):
    bot.send_message(m.chat.id, "Мағозаи Тоҷик - беҳтарин мағозаи онлайн дар Тоҷикистон!\nАз соли 2024 кор мекунем.\nЗиёда аз 5000 муштарӣ!\nСифат кафолат дода мешавад!")

@bot.message_handler(func=lambda m: m.text == "👤 Профили ман")
def btn_profile(m):
    u = m.from_user
    txt = f"👤 Профили шумо:\n\nНом: {u.first_name}\nUsername: @{u.username}\nID: {u.id}\nСабад: {cart_total(u.id)} сомонӣ\nФармоишҳо: {len([o for o in ORDERS if o['user']==u.id])}"
    bot.send_message(m.chat.id, txt)

@bot.message_handler(func=lambda m: m.text == "🔍 Ҷустуҷӯ")
def btn_search(m):
    bot.send_message(m.chat.id, "Номи молро нависед, масалан: Курта, Телефон, Асал")
    bot.register_next_step_handler(m, do_search)

def do_search(m):
    q = m.text.lower()
    found = []
    for pid, p in PRODUCTS.items():
        if q in p["name"].lower() or q in p["cat"].lower():
            found.append((pid, p))
    if not found:
        bot.send_message(m.chat.id, "Мол ёфт нашуд 😔 Кӯшиш кунед дигар номро.")
        return
    txt = f"Ёфт шуд ({len(found)}):\n\n"
    kb = types.InlineKeyboardMarkup()
    for pid, p in found[:10]:
        txt += f"• {p['name']} - {p['price']} с\n"
        kb.add(types.InlineKeyboardButton(p["name"], callback_data=f"prod_{pid}"))
    bot.send_message(m.chat.id, txt, reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "📦 Фармоишҳои ман")
def btn_orders(m):
    my = [o for o in ORDERS if o["user"] == m.from_user.id]
    if not my:
        bot.send_message(m.chat.id, "Шумо ҳанӯз фармоиш надодаед.")
        return
    txt = "📦 Фармоишҳои шумо:\n\n"
    for o in my[-5:]:
        txt += f"#{o['id']} - {o['total']} с - {o['status']} - {o['date']}\n"
    bot.send_message(m.chat.id, txt)

# ---------------- 7. CALLBACK ----------------
@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):
    uid = c.from_user.id
    data = c.data
    try:
        if data == "back_main":
            bot.edit_message_text("Менюи асосӣ:", c.message.chat.id, c.message.message_id, reply_markup=None)
            bot.send_message(c.message.chat.id, "Интихоб кунед:", reply_markup=main_menu())
        elif data == "back_cats":
            bot.edit_message_text("Категорияро интихоб кунед:", c.message.chat.id, c.message.message_id, reply_markup=cats_menu())
        elif data.startswith("cat_"):
            cat = data[4:]
            bot.edit_message_text(f"Категория: {cat}\nМолро интихоб кунед:", c.message.chat.id, c.message.message_id, reply_markup=products_menu(cat))
        elif data.startswith("prod_"):
            pid = int(data[5:])
            p = PRODUCTS[pid]
            txt = f"🛍 {p['name']}\n\n"
            txt += f"📂 Категория: {p['cat']}\n"
            txt += f"💰 Нарх: {p['price']} сомонӣ\n"
            txt += f"📦 Дар анбор: {p['stock']} дона\n\n"
            txt += f"📝 {p['desc']}\n\n"
            txt += "Барои харидорӣ Ба сабад-ро пахш кунед!"
            bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, reply_markup=product_menu(pid))
        elif data.startswith("add_"):
            pid = int(data[4:])
            cart = get_cart(uid)
            cart[pid] = cart.get(pid, 0) + 1
            bot.answer_callback_query(c.id, f"{PRODUCTS[pid]['name']} ба сабад илова шуд! ✅")
            bot.send_message(c.message.chat.id, f"✅ {PRODUCTS[pid]['name']} ба сабад илова шуд!\nСабад: {cart_total(uid)} сомонӣ")
        elif data.startswith("add2_"):
    pid = int(data[5:])
    cart = get_cart(uid)
    cart[pid] = cart.get(pid, 0) + 2
    bot.answer_callback_query(c.id, "2 дона илова шуд! ✅")
    bot.send_message(c.message.chat.id, f"✅ 2 дона илова шуд!\nСабад: {cart_total(uid)} сомонӣ")
elif data == "clear_cart":
    CARTS[uid] = {}
    bot.edit_message_text("Сабад тоза шуд! 🗑", c.message.chat.id, c.message.message_id)
elif data == "checkout":
    if not get_cart(uid):
        bot.answer_callback_query(c.id, "Сабад холӣ аст!")
        return
    bot.send_message(c.message.chat.id, "📝 Номи худро нависед:")
    bot.register_next_step_handler(c.message, get_name)
elif data == "admin_stats":
    txt = f"📊 Статистика:\n\nИстифодабарандагон: {len(USERS)}\nФармоишҳо: {len(ORDERS)}\nМолҳо: {len(PRODUCTS)}"
    bot.send_message(c.message.chat.id, txt)
elif data == "admin_orders":
    if not ORDERS:
        bot.send_message(c.message.chat.id, "Фармоиш нест")
    else:
        txt = "📦 Фармоишҳо:\n\n"
        for o in ORDERS[-10:]:
            txt += f"#{o['id']} - {o['total']} с - {o['name']}\n"
        bot.send_message(c.message.chat.id, txt)
elif data == "admin_users":
    bot.send_message(c.message.chat.id, f"👥 {len(USERS)} корбар")
elif data == "admin_broadcast":
    bot.send_message(c.message.chat.id, "Матни паёми оммавиро нависед:")
    bot.register_next_step_handler(c.message, do_broadcast)
elif data == "admin_add":
    bot.send_message(c.message.chat.id, "Барои иловаи мол ба админ нависед")
    except Exception as e:
        print("Callback error:", e)

def get_name(m):
    USERS[m.from_user.id]["order_name"] = m.text
    bot.send_message(m.chat.id, "📞 Рақами телефони худро нависед:")
    bot.register_next_step_handler(m, get_phone)

def get_phone(m):
    USERS[m.from_user.id]["order_phone"] = m.text
    bot.send_message(m.chat.id, "📍 Сурогаи худро нависед:")
    bot.register_next_step_handler(m, get_address)

def get_address(m):
    uid = m.from_user.id
    total = cart_total(uid) + 20
    order_id = len(ORDERS) + 1
    order = {"id": order_id, "user": uid, "name": USERS[uid].get("order_name", ""), "phone": USERS[uid].get("order_phone", ""), "address": m.text, "items": dict(get_cart(uid)), "total": total, "status": "Нав", "date": str(datetime.datetime.now())[:16]}
    ORDERS.append(order)
    CARTS[uid] = {}
    bot.send_message(m.chat.id, f"✅ Фармоиш қабул шуд! №: {order_id}\n💰 Ҷамъ: {total} сомонӣ", reply_markup=main_menu())
    try:
        bot.send_message(ADMIN_ID, f"🆕 Фармоиши нав #{order_id}!\n{order['name']} - {order['phone']}\n{total} сомонӣ")
    except:
        pass

def do_broadcast(m):
    count = 0
    for uid in list(USERS.keys()):
        try:
            bot.send_message(uid, f"📢 Эълон:\n\n{m.text}")
            count += 1
        except:
            pass
    bot.send_message(m.chat.id, f"Паём ба {count} нафар фиристода шуд!")

@bot.message_handler(func=lambda m: True)
def any_text(m):
    save_user(m.from_user)
    bot.send_message(m.chat.id, "Барои оғоз /start -ро пахш кунед", reply_markup=main_menu())

print("Bot started... Magozai Tojik")
bot.infinity_polling()
