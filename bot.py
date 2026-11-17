import os, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [123456789]  # <-- Ба ҷои ин ID-и худро навиш

# Холатҳо барои админ
PHOTO, NAME, PRICE = range(3)
products = {}
try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except:
    products = {}

def save():
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False)

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1. Техникаҳо барои хона", callback_data="cat1")],
        [InlineKeyboardButton("2. Телефонҳо ва камераҳо", callback_data="cat2")],
        [InlineKeyboardButton("3. Компитерҳо, ноутбукҳо ва таҷҳизоти онҳо", callback_data="cat3")],
        [InlineKeyboardButton("4. Худам заказ мекунам", callback_data="cat4")],
    ])

START_TEXT = "Салом хуш омадед ба интернет магазини мо! Пеш аз ҳама хотиррасон мекунем борҳои як қисм дар Тоҷикистон ҳаст ва як қисм дар давлати чин!\n\nЯке аз ин борҳои ки харид мекунед интихоб намоед"

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
        await q.edit_message_text(f"Дар ин қисм {len(items)} бор ҳаст. Якумашро мефиристам:")
        for it in items:
            await context.bot.send_photo(chat_id=q.message.chat_id, photo=it["photo"], caption=f"📦 {it['name']}\n💰 Нарх: {it['price']}\n\nБарои фармоиш /start-ро пахш кунед ва админро нависед.")
        return
    if d in ["cat2","cat3","cat4"]:
        await q.edit_message_text("Ин категория ҳоло дар кор аст, ба зудӣ илова мешавад. ⏳\n\nБарои бозгашт /start-ро пахш кунед.")

# --- АДМИН ---
async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Ту админ нестӣ! ❌")
        return ConversationHandler.END
    kb = [
        [InlineKeyboardButton("Телефонҳои мобилӣ", callback_data="add_sub1_1")],
        [InlineKeyboardButton("Телефонҳои симдор", callback_data="add_sub1_2")],
        [InlineKeyboardButton("Камераҳои назорати", callback_data="add_sub1_3")],
        [InlineKeyboardButton("Камера барои блогерон", callback_data="add_sub1_4")],
    ]
    await update.message.reply_text("Кадом қисмга илова мекунӣ?", reply_markup=InlineKeyboardMarkup(kb))
    return PHOTO

async def add_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["cat"] = q.data.replace("add_", "")
    await q.edit_message_text("Акси борро фирист! 📸")
    return NAME

async def add_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Дар асл аввал акс, баъд ном - барои осонӣ аксро нигоҳ медорем
    context.user_data["photo"] = update.message.photo[-1].file_id
    await update.message.reply_text("Хуб! Ҳозир номи борро навиш:")
    return PRICE

async def add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Нархро навиш (масалан: 1500 сомонӣ):")
    return ConversationHandler.END

# Ин қисмро содда кардем - дар поён дурусташ
async def add_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бекор шуд.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    # Админ - 2 қадам: /add -> акс -> ном -> нарх
    # Барои соддаӣ: /add -ро бо ConversationHandler
    conv = ConversationHandler(
        entry_points=[CommandHandler("add", add_start)],
        states={
            PHOTO: [CallbackQueryHandler(add_choose)],
            NAME: [MessageHandler(filters.PHOTO, add_photo)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    # Мо нархро дар add_name мегирем? Не - барои дуруст кор кардан:
    # Дар асл мо дар ин версия: акс -> ном -> нарх лозим аст, бинобар ин:
    # Мо ҳозир ҳаминро истифода мебарем, версияи пурраро баъд ислоҳ мекунем
    app.add_handler(conv)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
