import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "9282246667"))  
WHATSAPP = "992783829009" 
# Молҳо: ном, сомонӣ, юан, доллар
PRODUCTS = {
    "apple_case": [
        ("Чехол iPhone 15", 120, 85, 11),
        ("Чехол iPhone 16", 140, 100, 13),
        ("Чехол iPhone 14", 100, 70, 9),
    ],
    "samsung_case": [
        ("Чехол Samsung S24", 110, 78, 10),
        ("Чехол Samsung A55", 90, 64, 8),
    ],
    "xiaomi_case": [
        ("Чехол Xiaomi 14", 95, 67, 9),
        ("Чехол Redmi Note 13", 80, 57, 7),
    ],
    "laptop": [
        ("Ноутбук Lenovo IdeaPad", 5500, 3900, 500),
        ("Ноутбук HP Pavilion", 6200, 4400, 565),
    ],
    "kitchen": [
        ("Блендер Xiaomi", 350, 250, 32),
        ("Чойник электрикӣ", 280, 200, 25),
    ],
    "car": [
        ("Видеорегистратор 4K", 650, 460, 59),
        ("Зарядник мошин 65W", 180, 128, 16),
    ],
}

BRANDS = {
    "apple": "🍎 Apple",
    "samsung": "📱 Samsung",
    "xiaomi": "📱 Xiaomi",
    "huawei": "📱 Huawei",
    "honor": "📱 Honor",
}

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 Телефон ва лавозимоти он", callback_data="cat_phone")],
        [InlineKeyboardButton("💻 Компютер, ноутбук ва таҷҳизоти он", callback_data="cat_comp")],
        [InlineKeyboardButton("🏠 Барои хона ва ошхона", callback_data="cat_home")],
        [InlineKeyboardButton("🚗 Маҳсулот барои мошин", callback_data="cat_car")],
        [InlineKeyboardButton("✍️ Заказ аз админ", callback_data="cat_admin")],
        [InlineKeyboardButton("🛒 Сабади ман", callback_data="cart")],
    ])

def back_btn():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cart"] = []
    await update.message.reply_text(
        "Салом! 👋\nМағозаи техника ва таҷҳизоти электронӣ аз Чин 🇨🇳\nНархҳо аз худи завод, бе восита.\n\nКатегорияро интихоб кун:",
        reply_markup=main_menu()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "back":
        await q.edit_message_text("Категорияро интихоб кун:", reply_markup=main_menu())
        return

    if data == "cat_phone":
        kb = [[InlineKeyboardButton(v, callback_data=f"brand_{k}")] for k, v in BRANDS.items()]
        kb.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")])
        await q.edit_message_text("Маркаро интихоб кун:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("brand_"):
        brand = data.replace("brand_", "")
        key = f"{brand}_case" if f"{brand}_case" in PRODUCTS else "apple_case"
        kb = []
        for i, (name, s, y, d) in enumerate(PRODUCTS.get(key, [])):
            kb.append([InlineKeyboardButton(f"{name} - {s} с.", callback_data=f"prod_{key}_{i}")])
        kb.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="cat_phone")])
        await q.edit_message_text(f"{BRANDS.get(brand,'')} - Чехолҳо:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "cat_comp":
        kb = [[InlineKeyboardButton("💻 Ноутбукҳо", callback_data="show_laptop")],
              [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]]
        await q.edit_message_text("Компютер, ноутбук - интихоб кун:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "cat_home":
        kb = [[InlineKeyboardButton("🍳 Техникаи ошхона", callback_data="show_kitchen")],
              [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]]
        await q.edit_message_text("Барои хона ва ошхона:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "cat_car":
        kb = [[InlineKeyboardButton("🚗 Барои мошин", callback_data="show_car")],
              [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]]
        await q.edit_message_text("Маҳсулот барои мошин:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data in ["show_laptop", "show_kitchen", "show_car"]:
        key = {"show_laptop":"laptop","show_kitchen":"kitchen","show_car":"car"}[data]
        kb = []
        for i, (name, s, y, d) in enumerate(PRODUCTS[key]):
            kb.append([InlineKeyboardButton(f"{name} - {s} с.", callback_data=f"prod_{key}_{i}")])
        kb.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")])
        await q.edit_message_text("Молро интихоб кун:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("prod_"):
        _, key, idx = data.split("_")
        name, s, y, d = PRODUCTS[key][int(idx)]
        context.user_data["last_prod"] = (name, s)
        kb = [[InlineKeyboardButton("🛒 Ба сабад илова кун", callback_data=f"add_{key}_{idx}")],
              [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]]
        await q.edit_message_text(
            f"📦 {name}\n\n💰 Нарх:\n🇹🇯 {s} сомонӣ\n🇨🇳 {y} юан\n🇺🇸 {d} доллар",
            reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("add_"):
        _, key, idx = data.split("_")
        name, s, y, d = PRODUCTS[key][int(idx)]
        cart = context.user_data.get("cart", [])
        cart.append((name, s))
        context.user_data["cart"] = cart
        await q.edit_message_text(f"✅ {name} ба сабад илова шуд!\n\nКатегорияро интихоб кун:", reply_markup=main_menu())
        return

    if data == "cart":
        cart = context.user_data.get("cart", [])
        if not cart:
            await q.edit_message_text("🛒 Сабади шумо холӣ аст.", reply_markup=back_btn())
            return
        total = sum(x[1] for x in cart)
        text = "🛒 Сабади шумо:\n\n" + "\n".join([f"- {n} - {p} с." for n, p in cart]) + f"\n\n💰 Ҷамъ: {total} сомонӣ\n\nНом ва рақами телефонатонро нависед:"
        context.user_data["await_order"] = True
        await q.edit_message_text(text, reply_markup=back_btn())
        return

    if data == "cat_admin":
        await q.edit_message_text(
            "✍️ Заказ аз админ\n\nАгар моле, ки мехоҳӣ дар мағоза нест, акс ё силкаи онро аз Taobao / Pinduoduo ҳамин ҷо равон кун, админ нархашро мегӯяд.\n\nАкс ё силкаро равон кун:",
            reply_markup=back_btn())
        context.user_data["await_custom"] = True
        return

    if data.startswith("accept_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(user_id, "✅ Фармоиши шумо қабул шуд!\nМо ба зудӣ бо шумо тамос мегирем. Раҳмат! 🙏")
        await q.edit_message_text("✅ Қабул шуд, ба муштарӣ хабар рафт.")
        return
    if data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(user_id, "❌ Мутаассифона фармоиши шумо рад шуд. Барои маълумоти бештар ба админ нависед.")
        await q.edit_message_text("❌ Рад шуд.")
        return

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or "[Акс равон шуд]"
    if context.user_data.get("await_custom"):
        context.user_data["await_custom"] = False
        if ADMIN_ID:
            await context.bot.send_message(ADMIN_ID, f"✍️ ЗАКАЗИ НАВ АЗ АДМИН!\n\n👤 {user.first_name} (@{user.username})\n📝 {text}\n\nБарои ҷавоб, ба муштарӣ нависед.")
        await update.message.reply_text("✅ Дархости шумо ба админ равон шуд! Админ ба зудӣ ҷавоб медиҳад.")
        return
    if context.user_data.get("await_order"):
        context.user_data["await_order"] = False
        cart = context.user_data.get("cart", [])
        total = sum(x[1] for x in cart)
        items = "\n".join([f"- {n} - {p} с." for n, p in cart])
        if ADMIN_ID:
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Қабул кардан", callback_data=f"accept_{user.id}"),
                 InlineKeyboardButton("❌ Рад кардан", callback_data=f"reject_{user.id}")],
                [InlineKeyboardButton(f"💬 WhatsApp-и муштарӣ", url=f"https://wa.me/{WHATSAPP}")]
            ])
            await context.bot.send_message(ADMIN_ID, f"🆕 ЗАЯВКАИ НАВ!\n\n👤 {user.first_name} (@{user.username})\n📞 {text}\n\n{items}\n\n💰 Ҷамъ: {total} сомонӣ", reply_markup=kb)
        await update.message.reply_text("✅ Заявкаи шумо қабул шуд! Админ ба зудӣ тамос мегирад.")
        context.user_data["cart"] = []
        return
    await update.message.reply_text("Барои оғоз /start -ро пахш кунед.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_msg))
    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
