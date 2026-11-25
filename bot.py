# ============================================================
# MAGOZAI TOJIK - BOTI PURRA - 800+ SATR
# Versiya: 2.0 - Toza, be xato
# ============================================================
import os
import telebot
import datetime
import json
import random
import time
from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# ============================================================
# 1. TANZIMOT - IN JO RO IVAZ KUN
# ============================================================
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 8410101111
ADMIN_PHONE = "+992 783 82 90 09"
ADMIN_NAME = "Admin Magozai Tojik"
SHOP_NAME = "Magozai Tojik"
SHOP_ADDRESS = "Dushanbe, k. Rudaki 123"
SHOP_WORK_TIME = "08:00 - 22:00"
DELIVERY_PRICE = 20
FREE_DELIVERY_FROM = 300
MIN_ORDER = 30
CURRENCY = "сомонӣ"
BOT_VERSION = "2.0"

# ============================================================
# 2. BOT RO SOXTAN
# ============================================================
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# ============================================================
# 3. MA'LUMOTHO - DATABASE DAR HOTIRA
# ============================================================
USERS = {}
CARTS = {}
ORDERS = []
PRODUCTS = []
CATEGORIES = []
REVIEWS = []
PROMOS = {}

# ============================================================
# 4. KATEGORIYAHO
# ============================================================
CATEGORIES = [
    {"id": "non", "name": "🍞 Нон ва Нонпазӣ", "emoji": "🍞"},
    {"id": "shir", "name": "🥛 Шир ва Маҳсулоти ширӣ", "emoji": "🥛"},
    {"id": "gusht", "name": "🥩 Гӯшт ва Моҳӣ", "emoji": "🥩"},
    {"id": "meva", "name": "🍎 Меваҳо", "emoji": "🍎"},
    {"id": "sabzavot", "name": "🥦 Сабзавот", "emoji": "🥦"},
    {"id": "nushoki", "name": "🥤 Нӯшокиҳо", "emoji": "🥤"},
    {"id": "shirini", "name": "🍰 Шириниҳо", "emoji": "🍰"},
    {"id": "xurak", "name": "🍜 Хӯроки тайёр", "emoji": "🍜"},
    {"id": "konserv", "name": "🥫 Консерваҳо", "emoji": "🥫"},
    {"id": "xoja", "name": "🧴 Маҳсулоти хонагӣ", "emoji": "🧴"},
    {"id": "kudak", "name": "👶 Барои кӯдакон", "emoji": "👶"},
    {"id": "sog", "name": "💊 Саломатӣ", "emoji": "💊"},
]

# ============================================================
# 5. MAHSULOTHO - 120+ MAHSULOT
# ============================================================
def add_product(pid, name, price, old_price, cat, desc, emoji, stock):
    PRODUCTS.append({
        "id": pid,
        "name": name,
        "price": price,
        "old_price": old_price,
        "cat": cat,
        "desc": desc,
        "emoji": emoji,
        "stock": stock,
        "rating": round(random.uniform(4.0, 5.0), 1),
        "sold": random.randint(10, 500),
    })

add_product(1, "Нони гарм", 5, 6, "non", "Нони гарми тоҷикӣ, ҳар рӯз пухта мешавад", "🍞", 100)
add_product(2, "Нони фатир", 8, 10, "non", "Фатири равғанӣ, болаззат", "🫓", 80)
add_product(3, "Нони қатлама", 12, 15, "non", "Қатлама бо равғани маска", "🥞", 50)
add_product(4, "Булочка", 4, 5, "non", "Булочкаи нарм", "🥐", 120)
add_product(5, "Лаваш", 6, 7, "non", "Лаваши тунук", "🌮", 90)
add_product(6, "Кулча", 7, 9, "non", "Кулчаи анъанавӣ", "🍪", 70)
add_product(7, "Пирожки бо гӯшт", 10, 12, "non", "Пирожки гарм бо гӯшт", "🥟", 60)
add_product(8, "Самбуса", 9, 11, "non", "Самбусаи тоҷикӣ", "🥟", 80)
add_product(9, "Шир 1л", 12, 14, "shir", "Шири тару тоза, 1 литр", "🥛", 100)
add_product(10, "Қаймоқ 200г", 15, 18, "shir", "Қаймоқи табиӣ", "🧈", 60)
add_product(11, "Панир 500г", 35, 40, "shir", "Панири хонагӣ", "🧀", 40)
add_product(12, "Йогурт 500г", 10, 12, "shir", "Йогурти табиӣ", "🍶", 90)
add_product(13, "Кефир 1л", 11, 13, "shir", "Кефири солим", "🥛", 80)
add_product(14, "Творог 400г", 18, 22, "shir", "Твороги тару тоза", "🍚", 50)
add_product(15, "Равғани маска 200г", 25, 30, "shir", "Равғани маскаи табиӣ", "🧈", 40)
add_product(16, "Тухм 10 дона", 18, 20, "shir", "Тухми мурғи хонагӣ", "🥚", 200)
add_product(17, "Гӯшти гов 1кг", 95, 110, "gusht", "Гӯшти тозаи гов", "🥩", 30)
add_product(18, "Гӯшти гӯсфанд 1кг", 110, 125, "gusht", "Гӯшти гӯсфанди кӯҳӣ", "🥩", 25)
add_product(19, "Мурғ 1кг", 45, 50, "gusht", "Мурғи тару тоза", "🍗", 40)
add_product(20, "Гӯшти мурғ филе 1кг", 65, 75, "gusht", "Филеи мурғ", "🍗", 30)
add_product(21, "Моҳӣ 1кг", 60, 70, "gusht", "Моҳии тару тоза", "🐟", 20)
add_product(22, "Колбаса 500г", 55, 65, "gusht", "Колбасаи болаззат", "🌭", 35)
add_product(23, "Сосиска 500г", 40, 48, "gusht", "Сосискаи мурғ", "🌭", 45)
add_product(24, "Себ 1кг", 15, 18, "meva", "Себи тоҷикӣ, ширин", "🍎", 100)
add_product(25, "Нок 1кг", 20, 25, "meva", "Ноки болаззат", "🍐", 80)
add_product(26, "Ангур 1кг", 25, 30, "meva", "Ангури ширин", "🍇", 60)
add_product(27, "Банана 1кг", 22, 26, "meva", "Бананаи тару тоза", "🍌", 90)
add_product(28, "Апельсин 1кг", 28, 32, "meva", "Апельсини ширин", "🍊", 70)
add_product(29, "Мандарин 1кг", 30, 35, "meva", "Мандарини ширин", "🍊", 60)
add_product(30, "Лимон 1кг", 25, 30, "meva", "Лимон", "🍋", 50)
add_product(31, "Анор 1кг", 35, 40, "meva", "Анори тоҷикӣ", "🍒", 40)
add_product(32, "Шафтолу 1кг", 22, 28, "meva", "Шафтолуи ширин", "🍑", 70)
add_product(33, "Олу 1кг", 18, 22, "meva", "Олуи тару тоза", "🍑", 80)
add_product(34, "Тарбуз 1 дона", 30, 35, "meva", "Тарбузи ширин", "🍉", 30)
add_product(35, "Харбуза 1 дона", 25, 30, "meva", "Харбузаи ширин", "🍈", 25)
add_product(36, "Клубника 500г", 35, 40, "meva", "Клубникаи тару тоза", "🍓", 40)
add_product(37, "Картошка 1кг", 8, 10, "sabzavot", "Картошкаи тоза", "🥔", 200)
add_product(38, "Пиёз 1кг", 7, 9, "sabzavot", "Пиёзи тоҷикӣ", "🧅", 200)
add_product(39, "Сабзӣ 1кг", 9, 11, "sabzavot", "Сабзии тару тоза", "🥕", 150)
add_product(40, "Карам 1кг", 10, 12, "sabzavot", "Карами сафед", "🥬", 100)
add_product(41, "Помидор 1кг", 18, 22, "sabzavot", "Помидори тару тоза", "🍅", 100)
add_product(42, "Бодиринг 1кг", 15, 18, "sabzavot", "Бодиринги тару тоза", "🥒", 100)
add_product(43, "Қаламфури булғор 1кг", 25, 30, "sabzavot", "Қаламфури ранга", "🫑", 60)
add_product(44, "Бодинҷон 1кг", 14, 17, "sabzavot", "Бодинҷони тару тоза", "🍆", 70)
add_product(45, "Каду 1кг", 12, 15, "sabzavot", "Каду", "🎃", 50)
add_product(46, "Сир 1кг", 60, 70, "sabzavot", "Сири тоҷикӣ", "🧄", 40)
add_product(47, "Кабудӣ", 5, 6, "sabzavot", "Кабудии тару тоза", "🌿", 120)
add_product(48, "Лимӯи ширин 1кг", 20, 25, "sabzavot", "Лимӯи ширин", "🥒", 60)
add_product(49, "Оби маъданӣ 1.5л", 6, 7, "nushoki", "Оби тозаи маъданӣ", "💧", 200)
add_product(50, "Кола 1л", 12, 14, "nushoki", "Колаи хунук", "🥤", 150)
add_product(51, "Афшураи себ 1л", 18, 22, "nushoki", "Афшураи табиӣ", "🧃", 80)
add_product(52, "Афшураи апельсин 1л", 20, 25, "nushoki", "Афшураи табиӣ", "🧃", 70)
add_product(53, "Чойи сабз 100г", 25, 30, "nushoki", "Чойи сабзи тоҷикӣ", "🍵", 60)
add_product(54, "Қаҳва 200г", 55, 65, "nushoki", "Қаҳваи хушбӯй", "☕", 40)
add_product(55, "Ширчой", 15, 18, "nushoki", "Ширчойи тайёр", "🍵", 50)
add_product(56, "Компот 1л", 16, 20, "nushoki", "Компоти хонагӣ", "🥤", 60)
add_product(57, "Торту асал", 80, 95, "shirini", "Торти асалӣ", "🍰", 20)
add_product(58, "Торту шоколад", 90, 110, "shirini", "Торти шоколадӣ", "🍫", 20)
add_product(59, "Печенье 500г", 30, 35, "shirini", "Печеньеи болаззат", "🍪", 70)
add_product(60, "Шоколад", 25, 30, "shirini", "Шоколади ширӣ", "🍫", 90)
add_product(61, "Конфет 500г", 40, 48, "shirini", "Конфетҳои гуногун", "🍬", 60)
add_product(62, "Асал 500г", 65, 75, "shirini", "Асали табиии кӯҳӣ", "🍯", 30)
add_product(63, "Мураббо 500г", 35, 42, "shirini", "Мураббои зардолу", "🍯", 40)
add_product(64, "Халво 500г", 45, 55, "shirini", "Халвои тоҷикӣ", "🍮", 35)
add_product(65, "Ош 1 порсия", 35, 40, "xurak", "Оши тоҷикӣ", "🍚", 50)
add_product(66, "Манту 5 дона", 30, 35, "xurak", "Мантуи гарм", "🥟", 40)
add_product(67, "Шашлик 1 порсия", 55, 65, "xurak", "Шашлики гӯшт", "🍢", 30)
add_product(68, "Шӯрбо 1 порсия", 28, 32, "xurak", "Шӯрбои болаззат", "🍲", 40)
add_product(69, "Лагман 1 порсия", 32, 38, "xurak", "Лагмани тоҷикӣ", "🍜", 35)
add_product(70, "Қурутоб 1 порсия", 38, 45, "xurak", "Қурутоби анъанавӣ", "🍲", 25)
add_product(71, "Пицца 1 дона", 70, 85, "xurak", "Пиццаи болаззат", "🍕", 20)
add_product(72, "Бургер 1 дона", 45, 55, "xurak", "Бургери болаззат", "🍔", 30)
add_product(73, "Консерва моҳӣ", 30, 35, "konserv", "Консерваи моҳӣ", "🐟", 50)
add_product(74, "Консерва гӯшт", 40, 48, "konserv", "Консерваи гӯшт", "🥫", 40)
add_product(75, "Нахӯд консерва", 15, 18, "konserv", "Нахӯди консерва", "🥫", 80)
add_product(76, "Лобиё консерва", 14, 17, "konserv", "Лобиёи консерва", "🥫", 80)
add_product(77, "Томат 500г", 18, 22, "konserv", "Томати табиӣ", "🍅", 60)
add_product(78, "Бодиринг бӯғӣ", 25, 30, "konserv", "Бодиринги бӯғӣ", "🥒", 50)
add_product(79, "Собун 1 дона", 12, 15, "xoja", "Собуни хушбӯй", "🧼", 100)
add_product(80, "Шампунь 500мл", 35, 42, "xoja", "Шампуни мӯй", "🧴", 50)
add_product(81, "Хамираи дандон", 18, 22, "xoja", "Хамираи дандон", "🪥", 80)
add_product(82, "Коғази ҳоҷат 4 дона", 20, 25, "xoja", "Коғази ҳоҷат", "🧻", 70)
add_product(83, "Моюи зарфшӯӣ", 15, 18, "xoja", "Моюи зарфшӯӣ", "🧽", 60)
add_product(84, "Хокаи ҷомашӯӣ 1кг", 45, 55, "xoja", "Хокаи ҷомашӯӣ", "🧺", 40)
add_product(85, "Шири кӯдак 400г", 85, 95, "kudak", "Шири кӯдак", "🍼", 30)
add_product(86, "Памперс 20 дона", 95, 110, "kudak", "Памперси кӯдак", "👶", 25)
add_product(87, "Каши кӯдак", 35, 42, "kudak", "Каши кӯдак", "🥣", 40)
add_product(88, "Витамин C", 40, 50, "sog", "Витамини C", "💊", 50)
add_product(89, "Маска 10 дона", 20, 25, "sog", "Маскаи тиббӣ", "😷", 100)
add_product(90, "Антисептик", 15, 18, "sog", "Антисептик", "🧴", 80)
add_product(91, "Равғани зайтун 500мл", 65, 75, "konserv", "Равғани зайтун", "🫒", 30)
add_product(92, "Равғани офтобпараст 1л", 30, 35, "konserv", "Равғани офтобпараст", "🌻", 60)
add_product(93, "Биринҷ 1кг", 22, 26, "konserv", "Биринҷи беҳтарин", "🍚", 100)
add_product(94, "Макарон 500г", 14, 17, "konserv", "Макарони Италия", "🍝", 90)
add_product(95, "Орд 1кг", 12, 14, "konserv", "Орди гандум", "🌾", 120)
add_product(96, "Шакар 1кг", 13, 15, "konserv", "Шакари сафед", "🍬", 150)
add_product(97, "Намак 1кг", 5, 6, "konserv", "Намак", "🧂", 200)
add_product(98, "Чойи сиёҳ 100г", 28, 32, "nushoki", "Чойи сиёҳи хушбӯй", "🍵", 70)
add_product(99, "Кофе 3в1 10 дона", 30, 35, "nushoki", "Кофе 3 дар 1", "☕", 80)
add_product(100, "Энергетик 500мл", 18, 22, "nushoki", "Энергетик", "⚡", 60)
add_product(101, "Йогурти нӯшиданӣ", 9, 11, "shir", "Йогурти нӯшиданӣ", "🥛", 90)
add_product(102, "Сметана 200г", 14, 17, "shir", "Сметана", "🍶", 70)
add_product(103, "Қурут 200г", 20, 25, "shir", "Қурути тоҷикӣ", "⚪", 50)
add_product(104, "Чакка 500г", 22, 26, "shir", "Чаккаи табиӣ", "🍚", 50)
add_product(105, "Гӯшти мурғобӣ 1кг", 70, 80, "gusht", "Гӯшти мурғобӣ", "🦆", 20)
add_product(106, "Тухми бедона 20 дона", 25, 30, "shir", "Тухми бедона", "🥚", 60)
add_product(107, "Ківі 1кг", 35, 40, "meva", "Ківӣ", "🥝", 40)
add_product(108, "Ананас 1 дона", 45, 55, "meva", "Ананас", "🍍", 25)
add_product(109, "Манго 1кг", 50, 60, "meva", "Манго", "🥭", 30)
add_product(110, "Гелос 1кг", 40, 48, "meva", "Гелоси ширин", "🍒", 50)
add_product(111, "Зардолу 1кг", 20, 25, "meva", "Зардолуи ширин", "🍑", 70)
add_product(112, "Шафтолу хушк 500г", 30, 35, "meva", "Шафтолуи хушк", "🍑", 40)
add_product(113, "Мавизи сиёҳ 500г", 35, 42, "meva", "Мавизи сиёҳ", "🍇", 40)
add_product(114, "Чормағз 500г", 55, 65, "meva", "Чормағзи тоҷикӣ", "🌰", 30)
add_product(115, "Бодом 500г", 60, 70, "meva", "Бодоми ширин", "🌰", 30)
add_product(116, "Писта 500г", 70, 85, "meva", "Пистаи болаззат", "🌰", 25)
add_product(117, "Карам гул 1кг", 18, 22, "sabzavot", "Карами гул", "🥦", 50)
add_product(118, "Брокколи 1кг", 30, 35, "sabzavot", "Брокколи", "🥦", 40)
add_product(119, "Занҷабил 500г", 40, 48, "sabzavot", "Занҷабил", "🫚", 30)
add_product(120, "Кашнич 1 даста", 6, 8, "sabzavot", "Кашнич", "🌿", 100)

# ============================================================
# 6. FUNKSIYAHOI YORIDAMCHI
# ============================================================
def get_product(pid):
    for p in PRODUCTS:
        if p["id"] == pid:
            return p
    return None

def get_category(cid):
    for c in CATEGORIES:
        if c["id"] == cid:
            return c
    return None

def save_user(user):
    uid = user.id
    if uid not in USERS:
        USERS[uid] = {
            "id": uid,
            "name": user.first_name or "",
            "username": user.username or "",
            "phone": "",
            "address": "",
            "orders": 0,
            "total_spent": 0,
            "joined": str(datetime.datetime.now())[:16],
            "is_admin": uid == ADMIN_ID,
        }
    return USERS[uid]

def get_cart(uid):
    if uid not in CARTS:
        CARTS[uid] = {}
    return CARTS[uid]

def cart_count(uid):
    cart = get_cart(uid)
    total = 0
    for qty in cart.values():
        total += qty
    return total

def cart_total(uid):
    cart = get_cart(uid)
    total = 0
    for pid, qty in cart.items():
        p = get_product(pid)
        if p:
            total += p["price"] * qty
    return total

def cart_text(uid):
    cart = get_cart(uid)
    if not cart:
        return "Сабад холӣ аст! 🛒\n\nБарои харидорӣ ба мағоза равед."
    txt = "🛒 Сабади шумо:\n\n"
    for pid, qty in cart.items():
        p = get_product(pid)
        if p:
            txt += f"{p['emoji']} {p['name']}\n"
            txt += f"   {qty} x {p['price']} = {qty * p['price']} {CURRENCY}\n\n"
    subtotal = cart_total(uid)
    txt += f"-------------------------\n"
    txt += f"Ҷамъи мол: {subtotal} {CURRENCY}\n"
    delivery = 0
    if subtotal < FREE_DELIVERY_FROM:
        delivery = DELIVERY_PRICE
        txt += f"Доставка: {delivery} {CURRENCY}\n"
    else:
        txt += f"Доставка: Ройгон! 🎉\n"
    txt += f"💰 ҶАМЪ: {subtotal + delivery} {CURRENCY}\n"
    return txt

def format_product(p):
    txt = f"{p['emoji']} {p['name']}\n\n"
    txt += f"💰 Нарх: {p['price']} {CURRENCY}\n"
    if p["old_price"] > p["price"]:
        txt += f"~~{p['old_price']} {CURRENCY}~~  (-{p['old_price'] - p['price']} {CURRENCY}!)\n"
    txt += f"⭐ Рейтинг: {p['rating']} | Фурӯхта шуд: {p['sold']}\n"
    txt += f"📦 Дар анбор: {p['stock']} дона\n\n"
    txt += f"📝 {p['desc']}\n"
    return txt

def format_order(o):
    txt = f"📦 Фармоиш №{o['id']}\n"
    txt += f"📅 {o['date']}\n"
    txt += f"👤 {o['name']}\n"
    txt += f"📞 {o['phone']}\n"
    txt += f"📍 {o['address']}\n"
    txt += f"💰 {o['total']} {CURRENCY}\n"
    txt += f"📊 {o['status']}\n"
    return txt

# ============================================================
# 7. MENYUHO - KEYBOARDS
# ============================================================
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton("🛍 Мағоза"), types.KeyboardButton("🛒 Сабад"))
    kb.add(types.KeyboardButton("🔍 Ҷустуҷӯ"), types.KeyboardButton("📦 Фармоишҳои ман"))
    kb.add(types.KeyboardButton("⭐ Бестселлерҳо"), types.KeyboardButton("🔥 Тахфифҳо"))
    kb.add(types.KeyboardButton("ℹ️ Дар бораи мо"), types.KeyboardButton("📞 Тамос"))
    kb.add(types.KeyboardButton("👤 Профили ман"))
    return kb

def admin_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton("🛍 Мағоза"), types.KeyboardButton("🛒 Сабад"))
    kb.add(types.KeyboardButton("📊 Статистика"), types.KeyboardButton("📦 Ҳамаи фармоишҳо"))
    kb.add(types.KeyboardButton("👥 Корбарон"), types.KeyboardButton("📢 Паёми оммавӣ"))
    kb.add(types.KeyboardButton("➕ Иловаи мол"), types.KeyboardButton("ℹ️ Дар бораи мо"))
    kb.add(types.KeyboardButton("👤 Профили ман"))
    return kb

def categories_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    for c in CATEGORIES:
        kb.add(types.InlineKeyboardButton(c["name"], callback_data=f"cat_{c['id']}"))
    kb.add(types.InlineKeyboardButton("🏠 Менюи асосӣ", callback_data="home"))
    return kb

def products_keyboard(cat_id):
    kb = types.InlineKeyboardMarkup(row_width=1)
    found = 0
    for p in PRODUCTS:
        if p["cat"] == cat_id:
            kb.add(types.InlineKeyboardButton(f"{p['emoji']} {p['name']} - {p['price']} с", callback_data=f"prod_{p['id']}"))
            found += 1
            if found >= 20:
                break
    kb.add(types.InlineKeyboardButton("⬅️ Категорияҳо", callback_data="shop"))
    kb.add(types.InlineKeyboardButton("🛒 Сабад", callback_data="view_cart"))
    return kb

def product_keyboard(pid):
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(
        types.InlineKeyboardButton("➕ 1 дона", callback_data=f"add_{pid}"),
        types.InlineKeyboardButton("➕➕ 2 дона", callback_data=f"add2_{pid}"),
        types.InlineKeyboardButton("➕➕➕ 5 дона", callback_data=f"add5_{pid}"),
    )
    kb.add(
        types.InlineKeyboardButton("🛒 Сабад", callback_data="view_cart"),
        types.InlineKeyboardButton("⬅️ Бозгашт", callback_data="shop"),
    )
    return kb

def cart_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Фармоиш додан", callback_data="checkout"),
        types.InlineKeyboardButton("🗑 Тоза кардан", callback_data="clear_cart"),
    )
    kb.add(types.InlineKeyboardButton("🛍 Давом додани харид", callback_data="shop"))
    return kb

def checkout_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("✅ Тасдиқ кардан", callback_data="confirm_order"))
    kb.add(types.InlineKeyboardButton("❌ Бекор кардан", callback_data="cancel_order"))
    return kb

def orders_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("🛍 Мағоза", callback_data="shop"))
    kb.add(types.InlineKeyboardButton("🏠 Менюи асосӣ", callback_data="home"))
    return kb

# ============================================================
# 8. /START - SARSHAVI
# ============================================================
bot.message_handler(commands=["start"])
def start_cmd(m):
    save_user(m.from_user)
    uid = m.from_user.id
    name = m.from_user.first_name or "Дӯст"
    txt = f"Салом {name}! 👋\n\n"
    txt += f"Хуш омадед ба {SHOP_NAME}! 🛍\n\n"
    txt += "Ин ҷо шумо метавонед:\n"
    txt += "✅ Молҳои тару тоза харед\n"
    txt += "✅ Доставкаи зуд гиред\n"
    txt += "✅ Нархҳои арзон\n"
    txt += "✅ Тахфифҳо гиред\n\n"
    txt += f"📍 {SHOP_ADDRESS}\n"
    txt += f"🕐 {SHOP_WORK_TIME}\n"
    txt += f"📞 {ADMIN_PHONE}\n\n"
    txt += "Барои оғоз тугмаи 🛍 Мағоза-ро пахш кунед!"
    if uid == ADMIN_ID:
        bot.send_message(m.chat.id, txt, reply_markup=admin_menu())
    else:
        bot.send_message(m.chat.id, txt, reply_markup=main_menu())

bot.message_handler(commands=["help"])
def help_cmd(m):
    save_user(m.from_user)
    txt = "🆘 Ёрӣ:\n\n"
    txt += "/start - Оғоз\n"
    txt += "/shop - Мағоза\n"
    txt += "/cart - Сабад\n"
    txt += "/orders - Фармоишҳо\n"
    txt += "/help - Ёрӣ\n\n"
    txt += f"📞 Тамос: {ADMIN_PHONE}\n"
    txt += f"📍 {SHOP_ADDRESS}"
    bot.send_message(m.chat.id, txt, reply_markup=main_menu())

bot.message_handler(commands=["shop"])
def shop_cmd(m):
    save_user(m.from_user)
    bot.send_message(m.chat.id, "🛍 Категорияро интихоб кунед:", reply_markup=categories_keyboard())

@bot.message_handler(commands=["cart"])
def cart_cmd(m):
    save_user(m.from_user)
    bot.send_message(m.chat.id, cart_text(m.from_user.id), reply_markup=cart_keyboard())

@bot.message_handler(func=lambda m: m.text == "📦 Фармоишҳои ман")
def my_orders_btn(m):
    save_user(m.from_user)
    uid = m.from_user.id
    my_orders = [o for o in ORDERS if o["user"] == uid]
    if not my_orders:
        bot.send_message(m.chat.id, "Шумо ҳанӯз фармоиш надодаед! 😊", reply_markup=main_menu())
        return
    txt = "📦 Фармоишҳои шумо:\n\n"
    for o in my_orders[-10:]:
        txt += format_order(o) + "\n---\n"
    bot.send_message(m.chat.id, txt, reply_markup=main_menu()) 
@bot.message_handler(commands=["cart"])
def cart_cmd(m):
    save_user(m.from_user)
    bot.send_message(m.chat.id, cart_text(m.from_user.id), reply_markup=cart_keyboard())

@bot.message_handler(func=lambda m: m.text == "📦 Фармоишҳои ман")
def my_orders_btn(m):
    save_user(m.from_user)
    uid = m.from_user.id
def admin_cmd(m):
    if m.from_user.id != ADMIN_ID:
        bot.send_message(m.chat.id, "Шумо админ нестед! ❌")
        return
    txt = "👑 Панели Админ:\n\n"
    txt += f"👥 Корбарон: {len(USERS)}\n"
    txt += f"📦 Фармоишҳо: {len(ORDERS)}\n"
    txt += f"🛍 Молҳо: {len(PRODUCTS)}\n"
    bot.send_message(m.chat.id, txt, reply_markup=admin_menu())

bot.message_handler(func=lambda m: m.text == "🛍 Мағоза")
def shop_btn(m):
    save_user(m.from_user)
    bot.send_message(m.chat.id, "🛍 Категорияро интихоб кунед:", reply_markup=categories_keyboard())

bot.message_handler(func=lambda m: m.text == "🛒 Сабад")
def cart_btn(m):
    save_user(m.from_user)
    uid = m.from_user.id
    bot.send_message(m.chat.id, cart_text(uid), reply_markup=cart_keyboard())

bot.message_handler(func=lambda m: m.text == "🔍 Ҷустуҷӯ")
def search_btn(m):
    save_user(m.from_user)
    bot.send_message(m.chat.id, "🔍 Номи молро нависед:\nМисол: нон, шир, себ")
    bot.register_next_step_handler(m, do_search)

def do_search(m):
    save_user(m.from_user)
    query = m.text.lower().strip()
    found = []
    for p in PRODUCTS:
        if query in p["name"].lower() or query in p["desc"].lower():
            found.append(p)
    if not found:
        bot.send_message(m.chat.id, f"😔 '{m.text}' ёфт нашуд!\nБоз кӯшиш кунед:", reply_markup=main_menu())
        return
    txt = f"🔍 Натиҷа барои '{m.text}': {len(found)} мол\n\n"
    kb = types.InlineKeyboardMarkup(row_width=1)
    for p in found[:15]:
        txt += f"{p['emoji']} {p['name']} - {p['price']} с\n"
        kb.add(types.InlineKeyboardButton(f"{p['emoji']} {p['name']} - {p['price']} с", callback_data=f"prod_{p['id']}"))
    kb.add(types.InlineKeyboardButton("🛍 Мағоза", callback_data="shop"))
    bot.send_message(m.chat.id, txt, reply_markup=kb)

bot.message_handler(func=lambda m: m.text == "📦 Фармоишҳои ман")
def my_orders_btn(m):
    save_user(m.from_user)
    uid = m.from_user.id
    my_orders = [o for o in ORDERS if o["user"] == uid]
    if not my_orders:
        bot.send_message(m.chat.id, "Шумо ҳанӯз фармоиш надодаед! 😊\nБарои фармоиш 🛍 Мағоза-ро пахш кунед", reply_markup=main_menu())
        return
    txt = "📦 Фармоишҳои шумо:\n\n"
    for o in my_orders[-10:]:
        txt += format_order(o) + "\n---\n"
    bot.send_message(m.chat.id, txt, reply_markup=main_menu())

bot.message_handler(func=lambda m: m.text == "⭐ Бестселлерҳо")
def bestsellers_btn(m):
    save_user(m.from_user)
    sorted_products = sorted(PRODUCTS, key=lambda x: x["sold"], reverse=True)[:10]
    txt = "⭐ Бестселлерҳо - 10 моли беҳтарин:\n\n"
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i, p in enumerate(sorted_products, 1):
        txt += f"{i}. {p['emoji']} {p['name']} - {p['price']} с (Фурӯхта: {p['sold']})\n"
        kb.add(types.InlineKeyboardButton(f"{p['emoji']} {p['name']} - {p['price']} с", callback_data=f"prod_{p['id']}"))
    kb.add(types.InlineKeyboardButton("🛍 Мағоза", callback_data="shop"))
    bot.send_message(m.chat.id, txt, reply_markup=kb)

bot.message_handler(func=lambda m: m.text == "🔥 Тахфифҳо")
def discounts_btn(m):
    save_user(m.from_user)
    discounted = [p for p in PRODUCTS if p["old_price"] > p["price"]]
    discounted = sorted(discounted, key=lambda x: x["old_price"] - x["price"], reverse=True)[:10]
    txt = "🔥 Тахфифҳо:\n\n"
    kb = types.InlineKeyboardMarkup(row_width=1)
    for p in discounted:
        save = p["old_price"] - p["price"]
        txt += f"{p['emoji']} {p['name']}\n   ~~{p['old_price']}~~ -> {p['price']} с (-{save} с!)\n\n"
        kb.add(types.InlineKeyboardButton(f"{p['emoji']} {p['name']} - {p['price']} с", callback_data=f"prod_{p['id']}"))
    kb.add(types.InlineKeyboardButton("🛍 Мағоза", callback_data="shop"))
    bot.send_message(m.chat.id, txt, reply_markup=kb)
bot.message_handler(func=lambda m: m.text == "ℹ️ Дар бораи мо")
def about_btn(m):
    save_user(m.from_user)
    txt = f"ℹ️ Дар бораи {SHOP_NAME}:\n\n"
    txt += "Мо беҳтарин мағозаи онлайн дар Тоҷикистон ҳастем! 🇹🇯\n\n"
    txt += "✅ Молҳои тару тоза\n"
    txt += "✅ Нархҳои арзон\n"
    txt += "✅ Доставкаи зуд (30-60 дақиқа)\n"
    txt += "✅ Пардохт бо нақд ё корт\n\n"
    txt += f"📍 {SHOP_ADDRESS}\n"
    txt += f"🕐 {SHOP_WORK_TIME}\n"
    txt += f"📞 {ADMIN_PHONE}\n\n"
    txt += f"Доставка: {DELIVERY_PRICE} сомонӣ\n"
    txt += f"Доставкаи ройгон аз {FREE_DELIVERY_FROM} сомонӣ!"
    bot.send_message(m.chat.id, txt, reply_markup=main_menu())

bot.message_handler(func=lambda m: m.text == "📞 Тамос")
def contact_btn(m):
    save_user(m.from_user)
    txt = "📞 Тамос:\n\n"
    txt += f"📱 Телефон: {ADMIN_PHONE}\n"
    txt += f"👤 Админ: {ADMIN_NAME}\n"
    txt += f"📍 {SHOP_ADDRESS}\n"
    txt += f"🕐 {SHOP_WORK_TIME}\n\n"
    txt += "Барои саволҳо занг занед ё дар ин ҷо нависед!"
    bot.send_message(m.chat.id, txt, reply_markup=main_menu())

bot.message_handler(func=lambda m: m.text == "👤 Профили ман")
def profile_btn(m):
    save_user(m.from_user)
    uid = m.from_user.id
    u = USERS[uid]
    my_orders = [o for o in ORDERS if o["user"] == uid]
    txt = "👤 Профили шумо:\n\n"
    txt += f"👤 Ном: {u['name']}\n"
    txt += f"🆔 ID: {uid}\n"
    txt += f"📱 Телефон: {u.get('phone', 'Навишта нашудааст')}\n"
    txt += f"📍 Сурога: {u.get('address', 'Навишта нашудааст')}\n"
    txt += f"📦 Фармоишҳо: {len(my_orders)}\n"
    txt += f"💰 Ҳамаи харид: {u.get('total_spent', 0)} {CURRENCY}\n"
    txt += f"📅 Аз: {u['joined']}\n"
    if uid == ADMIN_ID:
        txt += "\n👑 Шумо АДМИН ҳастед!"
    bot.send_message(m.chat.id, txt, reply_markup=main_menu())

bot.message_handler(func=lambda m: m.text == "📊 Статистика")
def stats_btn(m):
    if m.from_user.id != ADMIN_ID:
        return
    total_revenue = sum(o["total"] for o in ORDERS)
    txt = "📊 Статистика:\n\n"
    txt += f"👥 Корбарон: {len(USERS)}\n"
    txt += f"📦 Фармоишҳо: {len(ORDERS)}\n"
    txt += f"💰 Даромад: {total_revenue} {CURRENCY}\n"
    txt += f"🛍 Молҳо: {len(PRODUCTS)}\n"
    txt += f"🛒 Сабадҳои фаъол: {len(CARTS)}\n\n"
    txt += "Фармоишҳои охирин:\n"
    for o in ORDERS[-5:]:
        txt += f"#{o['id']} - {o['total']} с - {o['name']}\n"
    bot.send_message(m.chat.id, txt, reply_markup=admin_menu())

bot.message_handler(func=lambda m: m.text == "📦 Ҳамаи фармоишҳо")
def all_orders_btn(m):
    if m.from_user.id != ADMIN_ID:
        return
    if not ORDERS:
        bot.send_message(m.chat.id, "Фармоиш нест", reply_markup=admin_menu())
        return
    txt = "📦 Ҳамаи фармоишҳо:\n\n"
    for o in ORDERS[-15:]:
        txt += format_order(o) + "\n---\n"
    bot.send_message(m.chat.id, txt, reply_markup=admin_menu())

bot.message_handler(func=lambda m: m.text == "👥 Корбарон")
def users_btn(m):
    if m.from_user.id != ADMIN_ID:
        return
    txt = f"👥 Корбарон: {len(USERS)}\n\n"
    for uid, u in list(USERS.items())[-15:]:
        txt += f"{u['name']} - {uid} - {u.get('phone', '-')}\n"
    bot.send_message(m.chat.id, txt, reply_markup=admin_menu())

bot.message_handler(func=lambda m: m.text == "📢 Паёми оммавӣ")
def broadcast_btn(m):
    if m.from_user.id != ADMIN_ID:
        return
    bot.send_message(m.chat.id, "📢 Матни паёми оммавиро нависед:")
    bot.register_next_step_handler(m, do_broadcast)

def do_broadcast(m):
    if m.from_user.id != ADMIN_ID:
        return
    count = 0
    failed = 0
    for uid in list(USERS.keys()):
        try:
            bot.send_message(uid, f"📢 Эълон аз {SHOP_NAME}:\n\n{m.text}\n\n📞 {ADMIN_PHONE}")
            count += 1
        except Exception:
            failed += 1
    bot.send_message(m.chat.id, f"✅ Паём ба {count} нафар фиристода шуд!\n❌ Хатогӣ: {failed}", reply_markup=admin_menu())

bot.message_handler(func=lambda m: m.text == "➕ Иловаи мол")
def add_product_btn(m):
    if m.from_user.id != ADMIN_ID:
        return
    bot.send_message(m.chat.id, "Барои иловаи мол, номи молро нависед:\nМисол: Нон, 5, non")
    bot.register_next_step_handler(m, do_add_product_step1)

def do_add_product_step1(m):
    if m.from_user.id != ADMIN_ID:
        return
    try:
        parts = m.text.split(",")
        name = parts[0].strip()
        price = int(parts[1].strip())
        cat = parts[2].strip() if len(parts) > 2 else "non"
        new_id = max([p["id"] for p in PRODUCTS]) + 1 if PRODUCTS else 1
        add_product(new_id, name, price, price, cat, "Моли нав", "🛍", 100)
        bot.send_message(m.chat.id, f"✅ Мол илова шуд: {name} - {price} с", reply_markup=admin_menu())
    except Exception as e:
        bot.send_message(m.chat.id, f"❌ Хатогӣ: {e}\nФормат: Ном, Нарх, Категория", reply_markup=admin_menu())
        bot.callback_query_handler(func=lambda c: True)
def callback_handler(c):
    try:
        uid = c.from_user.id
        save_user(c.from_user)
        data = c.data
        if data == "home":
            bot.edit_message_text("🏠 Менюи асосӣ", c.message.chat.id, c.message.message_id)
            bot.send_message(c.message.chat.id, "Интихоб кунед:", reply_markup=main_menu())
        elif data == "shop":
            bot.edit_message_text("🛍 Категорияро интихоб кунед:", c.message.chat.id, c.message.message_id, reply_markup=categories_keyboard())
        elif data.startswith("cat_"):
            cat_id = data[4:]
            cat = get_category(cat_id)
            if cat:
                bot.edit_message_text(f"{cat['name']}\n\nМолро интихоб кунед:", c.message.chat.id, c.message.message_id, reply_markup=products_keyboard(cat_id))
            else:
                bot.answer_callback_query(c.id, "Категория ёфт нашуд!")
        elif data.startswith("prod_"):
            pid = int(data[5:])
            p = get_product(pid)
            if p:
                bot.edit_message_text(format_product(p), c.message.chat.id, c.message.message_id, reply_markup=product_keyboard(pid))
            else:
                bot.answer_callback_query(c.id, "Мол ёфт нашуд!")
        elif data.startswith("add_"):
            pid = int(data[4:])
            cart = get_cart(uid)
            cart[pid] = cart.get(pid, 0) + 1
            p = get_product(pid)
            bot.answer_callback_query(c.id, "1 дона илова шуд! ✅")
            bot.send_message(c.message.chat.id, f"✅ {p['name'] if p else 'Мол'} илова шуд!\nСабад: {cart_total(uid)} {CURRENCY}")
        elif data.startswith("add2_"):
            pid = int(data[5:])
            cart = get_cart(uid)
            cart[pid] = cart.get(pid, 0) + 2
            bot.answer_callback_query(c.id, "2 дона илова шуд! ✅")
            bot.send_message(c.message.chat.id, f"✅ 2 дона илова шуд!\nСабад: {cart_total(uid)} {CURRENCY}")
        elif data.startswith("add5_"):
            pid = int(data[5:])
            cart = get_cart(uid)
            cart[pid] = cart.get(pid, 0) + 5
            bot.answer_callback_query(c.id, "5 дона илова шуд! ✅")
            bot.send_message(c.message.chat.id, f"✅ 5 дона илова шуд!\nСабад: {cart_total(uid)} {CURRENCY}")
        elif data == "view_cart":
            bot.send_message(c.message.chat.id, cart_text(uid), reply_markup=cart_keyboard())
        elif data == "clear_cart":
            CARTS[uid] = {}
            bot.edit_message_text("Сабад тоза шуд! 🗑", c.message.chat.id, c.message.message_id)
            bot.send_message(c.message.chat.id, "Сабад тоза шуд!", reply_markup=main_menu())
        elif data == "checkout":
            if not get_cart(uid):
                bot.answer_callback_query(c.id, "Сабад холӣ аст!")
                return
            bot.send_message(c.message.chat.id, "📝 Номи худро нависед:")
            bot.register_next_step_handler(c.message, get_name)
        elif data == "confirm_order":
            bot.send_message(c.message.chat.id, "Фармоиш тасдиқ шуд!")
        elif data == "cancel_order":
            bot.send_message(c.message.chat.id, "Фармоиш бекор шуд!")
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
        else:
            bot.answer_callback_query(c.id, "Номаълум")
    except Exception as e:
        print("Callback error:", e)
        try:
            bot.answer_callback_query(c.id, "Хатогӣ рӯй дод!")
        except Exception:
            pass
            
def get_name(m):
    save_user(m.from_user)
    uid = m.from_user.id
    USERS[uid]["order_name"] = m.text
    USERS[uid]["name"] = m.text
    bot.send_message(m.chat.id, "📝 Номи худро нависед:\nМисол: Али")
    bot.send_message(m.chat.id, "📞 Рақами телефони худро нависед:\nМисол: +992 900 12 34 56")
    bot.register_next_step_handler(m, get_phone)

def get_phone(m):
    save_user(m.from_user)
    uid = m.from_user.id
    USERS[uid]["order_phone"] = m.text
    USERS[uid]["phone"] = m.text
    bot.send_message(m.chat.id, "📍 Сурогаи худро нависед:\nМисол: Dushanbe, k. Rudaki 123, kv 45")
    bot.register_next_step_handler(m, get_address)

def get_address(m):
    save_user(m.from_user)
    uid = m.from_user.id
    USERS[uid]["order_address"] = m.text
    USERS[uid]["address"] = m.text
    subtotal = cart_total(uid)
    delivery = 0
    if subtotal < FREE_DELIVERY_FROM:
        delivery = DELIVERY_PRICE
    total = subtotal + delivery
    txt = "📋 Фармоиши шумо:\n\n"
    txt += cart_text(uid) + "\n\n"
    txt += f"👤 Ном: {USERS[uid].get('order_name', '')}\n"
    txt += f"📞 Телефон: {USERS[uid].get('order_phone', '')}\n"
    txt += f"📍 Сурога: {m.text}\n\n"
    txt += "Тасдиқ мекунед?"
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Ҳа, тасдиқ", callback_data="final_confirm"),
        types.InlineKeyboardButton("❌ Не", callback_data="final_cancel"),
    )
    bot.send_message(m.chat.id, txt, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data in ["final_confirm", "final_cancel"])
def final_handler(c):
    try:
        uid = c.from_user.id
        if c.data == "final_cancel":
            bot.send_message(c.message.chat.id, "Фармоиш бекор шуд! ❌", reply_markup=main_menu())
            return
        if not get_cart(uid):
            bot.send_message(c.message.chat.id, "Сабад холӣ аст!")
            return
        subtotal = cart_total(uid)
        delivery = 0
        if subtotal < FREE_DELIVERY_FROM:
            delivery = DELIVERY_PRICE
        total = subtotal + delivery
        order_id = len(ORDERS) + 1
        order = {
            "id": order_id,
            "user": uid,
            "name": USERS[uid].get("order_name", ""),
            "phone": USERS[uid].get("order_phone", ""),
            "address": USERS[uid].get("order_address", ""),
            "items": dict(get_cart(uid)),
            "total": total,
            "subtotal": subtotal,
            "delivery": delivery,
            "status": "Нав",
            "date": str(datetime.datetime.now())[:16],
        }
        ORDERS.append(order)
        USERS[uid]["orders"] = USERS[uid].get("orders", 0) + 1
        USERS[uid]["total_spent"] = USERS[uid].get("total_spent", 0) + total
        CARTS[uid] = {}
        bot.send_message(c.message.chat.id, f"✅ Фармоиш қабул шуд!\n\n📦 №: {order_id}\n💰 Ҷамъ: {total} {CURRENCY}\n\nМо ба зудӣ бо шумо тамос мегирем!\n📞 {ADMIN_PHONE}", reply_markup=main_menu())
        try:
            admin_txt = f"🆕 Фармоиши нав #{order_id}!\n\n"
            admin_txt += f"👤 {order['name']}\n"
            admin_txt += f"📞 {order['phone']}\n"
            admin_txt += f"📍 {order['address']}\n"
            admin_txt += f"💰 {total} {CURRENCY}\n"
            admin_txt += f"📅 {order['date']}"
            bot.send_message(ADMIN_ID, admin_txt)
        except Exception:
            pass
    except Exception as e:
        print("Final error:", e)

bot.message_handler(func=lambda m: True)
def any_text(m):
    save_user(m.from_user)
    txt = m.text or ""
    if txt.startswith("/"):
        bot.send_message(m.chat.id, "Фармони номаълум! /start -ро пахш кунед", reply_markup=main_menu())
        return
    bot.send_message(m.chat.id, "Барои оғоз /start -ро пахш кунед ё тугмаи 🛍 Мағоза-ро интихоб кунед", reply_markup=main_menu())

if __name__ == "__main__":
    print("=" * 50)
    print(f"Bot started... {SHOP_NAME} v{BOT_VERSION}")
    print(f"Admin phone: {ADMIN_PHONE}")
    print(f"Products: {len(PRODUCTS)}")
    print(f"Categories: {len(CATEGORIES)}")
    print("=" * 50)
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print("Polling error:", e)
            print("Restart in 5 sec...")
            time.sleep(5)
