import os, json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [9228348493]

CHOOSE, PHOTO, NAME, PRICE = range(4)

# Барои Render Web Service
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
    await q.edit_message_text(
        "📞 Барои фармоиш: @asoevabubakr\n\n⬅️ Барои бозгашт /start -ро пахш кун",
        reply_markup=main_kb(q.from_user.id in ADMIN_IDS)
    )

# ---------- КАТАЛОГ ----------

async def catalog(update, context):
    q = update.callback_query
    await q.answer()
    if not products:
        await q.edit_message_text(
            "Ҳоло маҳсулот нест. 😔",
            reply_markup=main_kb(q.from_user.id in ADMIN_IDS)
        )
        return
    kb = []
    for pid, p in products.items():
        kb.append([InlineKeyboardButton(f"{p['name']} - {p['price']} с.", callback_data=f"view_{pid}")])
    kb.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="back")])
    await q.edit_message_text("🛍 Каталог:", reply_markup=InlineKeyboardMarkup(kb))
# ---------- ДИДАНИ МАҲСУЛОТ ----------

async def view_product(update, context):
    q = update.callback_query
    await q.answer()
    pid = q.data.replace("view_", "")
    p = products.get(pid)
    if not p:
        await q.edit_message_text(
            "Маҳсулот ёфт нашуд.",
            reply_markup=main_kb(q.from_user.id in ADMIN_IDS)
        )
        return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Фармоиш додан", callback_data=f"order_{pid}")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="catalog")]
    ])
    caption = f"📦 {p['name']}\n💰 Нарх: {p['price']} с.\n📂 Категория: {p.get('category','-')}"
    if p.get("photo"):
        try:
            await q.message.reply_photo(photo=p["photo"], caption=caption, reply_markup=kb)
            await q.message.delete()
            return
        except:
            pass
    await q.edit_message_text(caption, reply_markup=kb)

async def order(update, context):
    q = update.callback_query
    await q.answer()
    pid = q.data.replace("order_", "")
    p = products.get(pid)
    if not p:
        return
    await q.edit_message_text(
        f"✅ Шумо '{p['name']}' -ро интихоб кардед.\n\nБарои фармоиш ба @asoevabubakr нависед.",
        reply_markup=main_kb(q.from_user.id in ADMIN_IDS)
    )

# ---------- АДМИН ----------

async def admin_panel(update, context):
    q = update.callback_query
    await q.answer()
    if q.from_user.id not in ADMIN_IDS:
        await q.edit_message_text("Ту админ нестӣ. ⛔")
        return
    await q.edit_message_text("⚙️ Панели админ:", reply_markup=admin_kb())

async def delete_list(update, context):
    q = update.callback_query
    await q.answer()
    if not products:
        await q.edit_message_text("Маҳсулот нест.", reply_markup=admin_kb())
        return
    kb = []
    for pid, p in products.items():
        kb.append([InlineKeyboardButton(f"🗑 {p['name']}", callback_data=f"del_{pid}")])
    kb.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="admin")])
    await q.edit_message_text("Кадомро нест кунем?", reply_markup=InlineKeyboardMarkup(kb))

async def delete_product(update, context):
    q = update.callback_query
    await q.answer()
    pid = q.data.replace("del_", "")
    if pid in products:
        del products[pid]
        save()
    await q.edit_message_text("✅ Нест карда шуд.", reply_markup=admin_kb())

async def back(update, context):
    q = update.callback_query
    await q.answer()
    await start(update, context)

# ---------- ИЛОВАИ МАҲСУЛОТ ----------

async def add_start(update, context):
    q = update.callback_query
    await q.answer()
    if q.from_user.id not in ADMIN_IDS:
        return
    await q.edit_message_text("Категорияро интихоб кун:", reply_markup=categories_kb())
    return CHOOSE

async def choose_cat(update, context):
    q = update.callback_query
    await q.answer()
    context.user_data["category"] = q.data.replace("cat_", "")
    await q.edit_message_text("📸 Акси маҳсулотро равон кун:")
    return PHOTO

async def get_photo(update, context):
    if not update.message.photo:
        await update.message.reply_text("Лутфан акс равон кун.")
        return PHOTO
    context.user_data["photo"] = update.message.photo[-1].file_id
    await update.message.reply_text("✏️ Номи маҳсулотро нависед:")
    return NAME

async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("💰 Нархро нависед (фақат рақам, масалан: 150):")
    return PRICE

async def get_price(update, context):
    price = update.message.text.strip()
    if not price.isdigit():
        await update.message.reply_text("Лутфан фақат рақам нависед:")
        return PRICE
    pid = str(len(products) + 1)
    while pid in products:
        pid = str(int(pid) + 1)
    products[pid] = {
        "name": context.user_data["name"],
        "price": price,
        "photo": context.user_data.get("photo"),
        "category": context.user_data.get("category", "Дигар")
    }
    save()
    context.user_data.clear()
    await update.message.reply_text("✅ Маҳсулот илова шуд!", reply_markup=main_kb(True))
    return ConversationHandler.END

async def cancel(update, context):
    q = update.callback_query
    if q:
        await q.answer()
        await q.edit_message_text("❌ Бекор карда шуд.", reply_markup=main_kb(q.from_user.id in ADMIN_IDS))
    else:
        await update.message.reply_text("❌ Бекор карда шуд.")
    context.user_data.clear()
    return ConversationHandler.END

# ---------- MAIN ----------

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_start, pattern="^add$")],
        states={
            CHOOSE: [CallbackQueryHandler(choose_cat, pattern="^cat_")],
            PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern="^cancel$"), CommandHandler("cancel", cancel)],
        allow_reentry=True
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(catalog, pattern="^catalog$"))
    app.add_handler(CallbackQueryHandler(view_product, pattern="^view_"))
    app.add_handler(CallbackQueryHandler(order, pattern="^order_"))
    app.add_handler(CallbackQueryHandler(contact, pattern="^contact$"))
    app.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin$"))
    app.add_handler(CallbackQueryHandler(delete_list, pattern="^delete_list$"))
    app.add_handler(CallbackQueryHandler(delete_product, pattern="^del_"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
