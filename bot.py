import os, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes

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
        json.dump(products, f, ensure_ascii=False, indent=2)

START_TEXT = "Салом хуш омадед ба интернет-мағозаи мо! 👇 Категорияро интихоб кунед:"

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1. Техника 📺", callback_data="cat1")],
        [InlineKeyboardButton("2. Телефон 📱", callback_data="cat2")],
        [InlineKeyboardButton("3. Компьютер 💻", callback_data="cat3")],
        [InlineKeyboardButton("4. Худ 😊", callback_data="cat4")],
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
            [InlineKeyboardButton("1. Телевизор", callback_data="sub1_1")],
            [InlineKeyboardButton("2. Холодильник", callback_data="sub1_2")],
            [InlineKeyboardButton("3. Кондиционер", callback_data="sub1_3")],
            [InlineKeyboardButton("4. Мошинаи ҷомашӯӣ", callback_data="sub1_4")],
            [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")],
        ]
        await q.edit_message_text("Категория: Техника. Яке аз зергурӯҳҳоро интихоб кунед:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if d.startswith("sub1_"):
        items = products.get(d, [])
        if not items:
            await q.edit_message_text("Дар ин бахш ҳоло мол нест 😔", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]]))
            return
        await q.edit_message_text(f"Дар ин бахш {len(items)} мол ҳаст:")
        for it in items:
            try:
                await context.bot.send_photo(chat_id=q.message.chat_id, photo=it["photo"], caption=f"{it['name']}\nНарх: {it['price']} сомонӣ")
            except:
                await context.bot.send_message(chat_id=q.message.chat_id, text=f"{it['name']}\nНарх: {it['price']}")
        return

    if d in ["cat2", "cat3", "cat4"]:
        await q.edit_message_text("Ин бахш ҳоло дар кор аст, ба зудӣ мол илова мешавад 🙏", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")]]))
        return

async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Шумо админ нестед ⛔")
        return ConversationHandler.END
    kb = [
        [InlineKeyboardButton("Телевизор", callback_data="sub1_1")],
        [InlineKeyboardButton("Холодильник", callback_data="sub1_2")],
        [InlineKeyboardButton("Кондиционер", callback_data="sub1_3")],
        [InlineKeyboardButton("Мошинаи ҷомашӯӣ", callback_data="sub1_4")],
    ]
    await update.message.reply_text("Категорияро интихоб кунед:", reply_markup=InlineKeyboardMarkup(kb))
    return CHOOSE

async def add_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["cat"] = q.data
    await q.edit_message_text("Расми молро равон кунед 📸")
    return PHOTO

async def add_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1].file_id
    context.user_data["photo"] = photo
    await update.message.reply_text("Номи молро нависед ✍️")
    return NAME

async def add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Нархро нависед 💰 (масалан: 2500)")
    return PRICE

async def add_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat = context.user_data["cat"]
    item = {"photo": context.user_data["photo"], "name": context.user_data["name"], "price": update.message.text}
    if cat not in products:
        products[cat] = []
    products[cat].append(item)
    save()
    await update.message.reply_text("Мол илова шуд! ✅")
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
        states={
            CHOOSE: [CallbackQueryHandler(add_choose)],
            PHOTO: [MessageHandler(filters.PHOTO, add_photo)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_price)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
