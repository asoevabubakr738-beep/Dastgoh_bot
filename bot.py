import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Салом хуш омадед ба интернет магазини мо! Пеш аз ҳама хотиррасон мекунем борҳои як қисм дар Тоҷикистон ҳаст ва як қисм дар давлати чин!\n\nЯке аз ин борҳои ки харид мекунед интихоб намоед"
    keyboard = [
        [InlineKeyboardButton("1. Техникаҳо барои хона", callback_data="cat1")],
        [InlineKeyboardButton("2. Телефонҳо ва камераҳо", callback_data="cat2")],
        [InlineKeyboardButton("3. Компитерҳо, ноутбукҳо ва таҷҳизоти онҳо", callback_data="cat3")],
        [InlineKeyboardButton("4. Худам заказ мекунам", callback_data="cat4")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "cat1":
        text = "Категорияи 1 - Техникаҳо барои хона:\n\nИнтихоб кунед:"
        keyboard = [
            [InlineKeyboardButton("1. Телефонҳои мобилӣ", callback_data="sub1_1")],
            [InlineKeyboardButton("2. Телефонҳои симдор", callback_data="sub1_2")],
            [InlineKeyboardButton("3. Камераҳои назорати", callback_data="sub1_3")],
            [InlineKeyboardButton("4. Камера барои блогерон ва таҷҳизоти иловагӣ", callback_data="sub1_4")],
            [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "back":
        text = "Салом хуш омадед ба интернет магазини мо! Пеш аз ҳама хотиррасон мекунем борҳои як қисм дар Тоҷикистон ҳаст ва як қисм дар давлати чин!\n\nЯке аз ин борҳои ки харид мекунед интихоб намоед"
        keyboard = [
            [InlineKeyboardButton("1. Техникаҳо барои хона", callback_data="cat1")],
            [InlineKeyboardButton("2. Телефонҳо ва камераҳо", callback_data="cat2")],
            [InlineKeyboardButton("3. Компитерҳо, ноутбукҳо ва таҷҳизоти онҳо", callback_data="cat3")],
            [InlineKeyboardButton("4. Худам заказ мекунам", callback_data="cat4")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data in ["cat2", "cat3", "cat4"]:
        await query.edit_message_text("Ин категория ҳоло дар кор аст, ба зудӣ илова мешавад. ⏳\n\nБарои бозгашт /start-ро пахш кунед.")

    elif data.startswith("sub1_"):
        await query.edit_message_text("Шумо инро интихоб кардед. Ба зудӣ молҳои ин қисм илова мешаванд. 📦\n\nБарои бозгашт /start-ро пахш кунед.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
