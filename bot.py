import os, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [8975989959]
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
        "cat4_naush_pc": {"name": "🎧 Наушник компютер", "brands": ["Беспроводное", "Проводное"]},
    }},
}

START_TEXT = "Салом хуш омадед! 👋\nИн мағозаи таҷҳизот аз Гуанчжоу аст.\nҲамаи молҳо аслӣ, бо кафолат.\n\nКатегорияро интихоб кунед:"

def main_menu():
    kb = []
    for cid, c in CATEGORIES.items():
        kb.append([InlineKeyboardButton(c["name"], callback_data=cid)])
    kb.append([InlineKeyboardButton("🛒 Сабади ман", callback_data="cart")])
    kb.append([InlineKeyboardButton("📞 Тамос", callback_data="contact")])
    return InlineKeyboardMarkup(kb)

def back_btn(cb):
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Бозгашт", callback_data=cb)]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.setdefault("cart", [])
    await update.message.reply_text(START_TEXT, reply_markup=main_menu())

async def show_products(q, context, key, back_cb, title=""):
    items = products.get(key, [])
    if not items:
        await q.edit_message_text(f"{title}\n\nДар ин бахш ҳоло мол нест 😔", reply_markup=back_btn(back_cb))
        return
    await q.edit_message_text(f"{title}\nДар ин бахш {len(items)} мол ҳаст:")
    for i, it in enumerate(items):
        caption = f"📦 {it['name']}\n\n💰 Нарх:\n- {it['som']} сомонӣ\n- {it['dol']} $ доллар\n- {it['yuan']} юан"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🛒 Ба сабад илова кун", callback_data=f"buy_{key}_{i}")]])
        try:
            await context.bot.send_photo(chat_id=q.message.chat_id, photo=it["photo"], caption=caption, reply_markup=kb)
        except:
            await context.bot.send_message(chat_id=q.message.chat_id, text=caption, reply_markup=kb)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    context.user_data.setdefault("cart", [])

    if d == "back":
        await q.edit_message_text(START_TEXT, reply_markup=main_menu())
        return
    if d == "contact":
        await q.edit_message_text("📞 Тамос:\n\nTelegram: @username\nТел: +992 ...\nМанзил: Душанбе", reply_markup=back_btn("back"))
        return
    if d == "cart":
        cart = context.user_data["cart"]
        if not cart:
            await q.edit_message_text("Сабад холӣ аст 😔", reply_markup=back_btn("back"))
            return
        txt = "🛒 Сабади шумо:\n\n"
        ts = td = ty = 0
        for it in cart:
            txt += f"- {it['name']} - {it['som']} с.\n"
            try: ts += int(it['som'])
            except: pass
        txt += f"\n💰 Ҷамъ: {ts} сомонӣ"
        kb = [[InlineKeyboardButton("✅ Фармоиш додан", callback_data="order")], [InlineKeyboardButton("🗑️ Сабадро тоза кун", callback_data="clear")], [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]]
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))
        return
    if d == "clear":
        context.user_data["cart"] = []
        await q.edit_message_text("Сабад тоза шуд ✅", reply_markup=back_btn("back"))
        return
    if d == "order":
        cart = context.user_data["cart"]
        if not cart:
            await q.edit_message_text("Сабад холӣ аст", reply_markup=back_btn("back"))
            return
        txt = f"🆕 Фармоиши нав!\n\nАз: @{q.from_user.username} (ID: {q.from_user.id})\nНом: {q.from_user.first_name}\n\n"
        for it in cart:
            txt += f"- {it['name']} - {it['som']} с. / {it['dol']} $ / {it['yuan']} юан\n"
        for aid in ADMIN_IDS:
            try: await context.bot.send_message(chat_id=aid, text=txt)
            except: pass
        context.user_data["cart"] = []
        await q.edit_message_text("Фармоишатон қабул шуд! ✅\nМо ба зудӣ бо шумо тамос мегирем 🙏", reply_markup=back_btn("back"))
        return
    if d in CATEGORIES:
        kb = []
        for sid, s in CATEGORIES[d]["subs"].items():
            kb.append([InlineKeyboardButton(s["name"], callback_data=sid)])
        kb.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")])
        await q.edit_message_text(f"Категория: {CATEGORIES[d]['name']}\nЯке ро интихоб кунед:", reply_markup=InlineKeyboardMarkup(kb))
        return
    # Зергурӯҳ
    for cid, c in CATEGORIES.items():
        if d in c["subs"]:
            sub = c["subs"][d]
            kb = []
            for b in sub["brands"]:
                kb.append([InlineKeyboardButton(b, callback_data=f"brand|{d}|{b}")])
            kb.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data=cid)])
            await q.edit_message_text(f"{sub['name']}\nМаркаро интихоб кунед:", reply_markup=InlineKeyboardMarkup(kb))
            return
    if d.startswith("brand|"):
        _, sub_id, brand = d.split("|", 2)
        key = f"{sub_id}|{brand}"
        await show_products(q, context, key, sub_id, title=f"📦 {brand}")
        return
    if d.startswith("buy_"):
        # buy_<key>_<index> - key метавонад | дошта бошад
        rest = d[4:]
        # охирин _ index аст
        idx_str = rest.rsplit("_", 1)[-1]
        key = rest.rsplit("_", 1)[0]
        try:
            idx = int(idx_str)
            items = products.get(key, [])
            if idx < len(items):
                context.user_data["cart"].append(items[idx])
                await q.answer("Ба сабад илова шуд! ✅", show_alert=True)
        except:
            pass
        return

# ===== ADMIN =====
async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Шумо админ нестед ⛔")
        return ConversationHandler.END
    kb = []
    for cid, c in CATEGORIES.items():
        for sid, s in c["subs"].items():
            for b in s["brands"]:
                kb.append([InlineKeyboardButton(f"{s['name']} > {b}", callback_data=f"{sid}|{b}")])
    await update.message.reply_text("Кадом шохаро интихоб мекунӣ? 👇", reply_markup=InlineKeyboardMarkup(kb))
    return CHOOSE

async def add_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["cat"] = q.data
    await q.edit_message_text("Расми молро равон кун 📸")
    return PHOTO
async def add_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["photo"] = update.message.photo[-1].file_id
    await update.message.reply_text("Номи молро нависед ✍️")
    return NAME
async def add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Нарх бо сомонӣ 💰 (масалан: 6500)")
    return PRICE_SOM
async def add_price_som(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["som"] = update.message.text
    await update.message.reply_text("Нарх бо доллар $ 💵 (масалан: 600)")
    return PRICE_DOL
async def add_price_dol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["dol"] = update.message.text
    await update.message.reply_text("Нарх бо юан 🇨🇳 (масалан: 4300)")
    return PRICE_YUAN
async def add_price_yuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat = context.user_data["cat"]
    item = {"photo": context.user_data["photo"], "name": context.user_data["name"], "som": context.user_data["som"], "dol": context.user_data["dol"], "yuan": update.message.text}
    if cat not in products:
        products[cat] = []
    products[cat].append(item)
    save()
    await update.message.reply_text("Мол илова шуд! ✅\nБоз /add - ро пахш кун")
    return ConversationHandler.END
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бекор шуд.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    conv = ConversationHandler(
        entry_points=[CommandHandler("add", add_start)],
        states={CHOOSE: [CallbackQueryHandler(add_choose)], PHOTO: [MessageHandler(filters.PHOTO, add_photo)], NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)], PRICE_SOM: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_price_som)], PRICE_DOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_price_dol)], PRICE_YUAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_price_yuan)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    print("Bot started...")
    app.run_polling()
if __name__ == "__main__":
    main()
