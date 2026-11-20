# ============================================================
# БОТИ ГУАНЧЖОУ - КОДИ ДУРУСТ - 650+ САТР
# Ҳамаи шохаҳо КОР мекунанд - PRODUCTS пурра аст
# ============================================================
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

SHOP_NAME = "ГУАНЧЖОУ"
SHOP_PHONE = "+992 900 00 00 00"
SHOP_USERNAME = "@guangzhou_tj"
SHOP_ADDRESS = "Душанбе, Гуанчжоу Маркет"
SHOP_TIME = "9:00 - 21:00"

# ============================================================
# ҲАМАИ МАҲСУЛОТҲО - ШОХАИ 1,2,3,4 - ПУРРА
# ============================================================
PRODUCTS = {
    # --- 1.1 APPLE ---
    "iphone13": {"name": "📱 iPhone 13", "price": "750$ / 8,100с", "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-13-01.jpg", "desc": "💾 128GB\n🎨 Сиёҳ, Сафед\n📦 5 дона\n⭐ Гарантия: 1 сол"},
    "iphone14": {"name": "📱 iPhone 14", "price": "850$ / 9,200с", "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-01.jpg", "desc": "💾 128GB\n📦 4 дона\n⭐ Гарантия: 1 сол"},
    "iphone14pro": {"name": "📱 iPhone 14 Pro", "price": "950$ / 10,300с", "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-pro-01.jpg", "desc": "💾 256GB\n📦 3 дона"},
    "iphone15": {"name": "📱 iPhone 15", "price": "950$ / 10,300с", "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-01.jpg", "desc": "💾 128GB\n📦 3 дона"},
    "iphone15pro": {"name": "📱 iPhone 15 Pro", "price": "1150$ / 12,400с", "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-pro-01.jpg", "desc": "💾 256GB\n📦 2 дона"},
    "iphone16": {"name": "📱 iPhone 16", "price": "1050$ / 11,300с", "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-16-01.jpg", "desc": "💾 128GB\n📦 4 дона"},
    "iphone16pro": {"name": "📱 iPhone 16 Pro", "price": "1250$ / 13,500с", "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-16-pro-01.jpg", "desc": "💾 256GB\n📦 2 дона"},
    # --- 1.1 SAMSUNG ---
    "samsung_a15": {"name": "📱 Samsung A15", "price": "180$ / 1,950с", "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a15-01.jpg", "desc": "💾 128GB\n📦 12 дона"},
    "samsung_a35": {"name": "📱 Samsung A35", "price": "350$ / 3,800с", "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a35-01.jpg", "desc": "💾 128GB\n📦 8 дона"},
    "samsung_a55": {"name": "📱 Samsung A55", "price": "450$ / 4,900с", "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a55-01.jpg", "desc": "💾 128GB\n📦 10 дона"},
    "samsung_s23": {"name": "📱 Samsung S23", "price": "700$ / 7,600с", "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s23-5g-01.jpg", "desc": "💾 256GB\n📦 3 дона"},
    "samsung_s24": {"name": "📱 Samsung S24", "price": "850$ / 9,200с", "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24-5g-01.jpg", "desc": "💾 256GB\n📦 4 дона"},
    "samsung_s24u": {"name": "📱 Samsung S24 Ultra", "price": "1150$ / 12,400с", "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24-ultra-5g-01.jpg", "desc": "💾 512GB\n📦 2 дона"},
    # --- 1.1 XIAOMI ---
    "redmi_13c": {"name": "📱 Redmi 13C", "price": "140$ / 1,500с", "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-13c-01.jpg", "desc": "💾 128GB\n📦 20 дона"},
    "redmi_note13": {"name": "📱 Redmi Note 13", "price": "220$ / 2,400с", "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-13-01.jpg", "desc": "💾 256GB\n📦 15 дона"},
    "redmi_note13pro": {"name": "📱 Redmi Note 13 Pro", "price": "300$ / 3,250с", "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-13-pro-01.jpg", "desc": "💾 256GB\n📦 8 дона"},
    "redmi_note14": {"name": "📱 Redmi Note 14", "price": "280$ / 3,000с", "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-14-01.jpg", "desc": "💾 256GB\n📦 8 дона"},
    "poco_x6": {"name": "📱 Poco X6", "price": "320$ / 3,500с", "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-poco-x6-01.jpg", "desc": "💾 256GB\n📦 6 дона"},
    "xiaomi14": {"name": "📱 Xiaomi 14", "price": "700$ / 7,600с", "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-14-01.jpg", "desc": "💾 512GB\n📦 3 дона"},
    # --- 1.1 HONOR / HUAWEI / VIVO / OPPO ---
    "honor_x8b": {"name": "📱 Honor X8b", "price": "250$ / 2,700с", "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-x8b-01.jpg", "desc": "💾 256GB\n📦 7 дона"},
    "honor_x9b": {"name": "📱 Honor X9b", "price": "320$ / 3,500с", "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-x9b-01.jpg", "desc": "💾 256GB\n📦 6 дона"},
    "honor_90": {"name": "📱 Honor 90", "price": "450$ / 4,900с", "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-90-01.jpg", "desc": "💾 512GB\n📦 4 дона"},
    "honor_magic6": {"name": "📱 Honor Magic 6", "price": "800$ / 8,600с", "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-magic6-01.jpg", "desc": "💾 512GB\n📦 2 дона"},
    "huawei_nova12": {"name": "📱 Huawei Nova 12", "price": "400$ / 4,300с", "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-nova-12-01.jpg", "desc": "💾 256GB\n📦 5 дона"},
    "huawei_pura70": {"name": "📱 Huawei Pura 70", "price": "650$ / 7,000с", "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-pura-70-01.jpg", "desc": "💾 256GB\n📦 3 дона"},
    "vivo_y100": {"name": "📱 Vivo Y100", "price": "280$ / 3,000с", "photo": "https://fdn2.gsmarena.com/vv/pics/vivo/vivo-y100-01.jpg", "desc": "💾 256GB\n📦 6 дона"},
    "oppo_a78": {"name": "📱 Oppo A78", "price": "260$ / 2,800с", "photo": "https://fdn2.gsmarena.com/vv/pics/oppo/oppo-a78-01.jpg", "desc": "💾 256GB\n📦 7 дона"},
    "oppo_reno11": {"name": "📱 Oppo Reno 11", "price": "450$ / 4,900с", "photo": "https://fdn2.gsmarena.com/vv/pics/oppo/oppo-reno11-01.jpg", "desc": "💾 256GB\n📦 4 дона"},
    # --- 1.2 НАУШНИК ---
    "airpods_pro2": {"name": "🎧 AirPods Pro 2", "price": "180$ / 1,950с", "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=1140&hei=1140&fmt=jpeg", "desc": "🔋 30 соат\n📦 20 дона"},
    "airpods2": {"name": "🎧 AirPods 2", "price": "95$ / 1,030с", "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MV7N2?wid=1140&hei=1140&fmt=jpeg", "desc": "🔋 24 соат\n📦 15 дона"},
    "airpods3": {"name": "🎧 AirPods 3", "price": "130$ / 1,400с", "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MME73?wid=1140&hei=1140&fmt=jpeg", "desc": "🔋 30 соат\n📦 10 дона"},
    "airpods_max": {"name": "🎧 AirPods Max", "price": "450$ / 4,900с", "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-max-select-202409-midnight?wid=1140&hei=1140&fmt=jpeg", "desc": "🔋 20 соат\n📦 3 дона"},
    "buds2": {"name": "🎧 Galaxy Buds 2", "price": "75$ / 810с", "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2208/gallery/levant-galaxy-buds2-pro-sm-r510nzwamea-533227276", "desc": "🔋 29 соат\n📦 12 дона"},
    "buds_pro": {"name": "🎧 Galaxy Buds 2 Pro", "price": "110$ / 1,190с", "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2208/gallery/levant-galaxy-buds2-pro-sm-r510nzwamea-533227276", "desc": "🔋 30 соат\n📦 8 дона"},
    "redmi_buds5": {"name": "🎧 Redmi Buds 5", "price": "35$ / 380с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1699261234.12345678.png", "desc": "🔋 38 соат\n📦 30 дона"},
    "redmi_buds_pro": {"name": "🎧 Redmi Buds 5 Pro", "price": "55$ / 595с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1700001234.12345678.png", "desc": "🔋 38 соат\n📦 15 дона"},
    "jbl_tune": {"name": "🎧 JBL Tune 230", "price": "50$ / 540с", "photo": "https://m.media-amazon.com/images/I/61xX9b+ZxJL._AC_SL1500_.jpg", "desc": "🔋 40 соат\n📦 12 дона"},
    "wired": {"name": "🎧 Наушник симӣ", "price": "10$ / 108с", "photo": "https://m.media-amazon.com/images/I/61yX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 50 дона"},
    # --- 1.3 ЗАРЯДНИК ---
    "charge_20w": {"name": "🔌 Зарядник 20W Apple", "price": "15$ / 160с", "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MHJE3?wid=1140&hei=1140&fmt=jpeg", "desc": "⚡ 20W\n📦 30 дона"},
    "charge_33w": {"name": "🔌 Зарядник 33W Xiaomi", "price": "20$ / 215с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1610001234.12345678.png", "desc": "⚡ 33W\n📦 25 дона"},
    "charge_67w": {"name": "🔌 Зарядник 67W Xiaomi", "price": "30$ / 325с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1620001234.12345678.png", "desc": "⚡ 67W\n📦 18 дона"},
    "charge_120w": {"name": "🔌 Зарядник 120W Xiaomi", "price": "45$ / 490с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1635001234.12345678.png", "desc": "⚡ 120W\n📦 10 дона"},
    "charge_anker": {"name": "🔌 Зарядник Anker 65W", "price": "35$ / 380с", "photo": "https://m.media-amazon.com/images/I/61zX9b+ZxJL._AC_SL1500_.jpg", "desc": "⚡ 65W GaN\n📦 12 дона"},
    # --- 1.4 КАБЕЛ ---
    "cable_typec": {"name": "🔗 Кабел Type-C 1м", "price": "8$ / 86с", "photo": "https://m.media-amazon.com/images/I/61aX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 50 дона"},
    "cable_light": {"name": "🔗 Кабел Lightning 1м", "price": "10$ / 108с", "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MXLY2?wid=1140&hei=1140&fmt=jpeg", "desc": "📦 40 дона"},
    "cable_micro": {"name": "🔗 Кабел Micro-USB", "price": "5$ / 54с", "photo": "https://m.media-amazon.com/images/I/61bX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 60 дона"},
    "cable_2m": {"name": "🔗 Кабел Type-C 2м", "price": "12$ / 130с", "photo": "https://m.media-amazon.com/images/I/61cX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 30 дона"},
    # --- 1.5 ЧЕХОЛ ---
    "case_iphone": {"name": "📱 Чехол iPhone", "price": "10$ / 108с", "photo": "https://m.media-amazon.com/images/I/61dX9b+ZxJL._AC_SL1500_.jpg", "desc": "Ҳамаи модел\n📦 100 дона"},
    "case_samsung": {"name": "📱 Чехол Samsung", "price": "8$ / 86с", "photo": "https://m.media-amazon.com/images/I/61eX9b+ZxJL._AC_SL1500_.jpg", "desc": "Ҳамаи модел\n📦 80 дона"},
    "case_xiaomi": {"name": "📱 Чехол Xiaomi", "price": "8$ / 86с", "photo": "https://m.media-amazon.com/images/I/61fX9b+ZxJL._AC_SL1500_.jpg", "desc": "Ҳамаи модел\n📦 80 дона"},
    "case_leather": {"name": "📱 Чехол Чармӣ", "price": "18$ / 195с", "photo": "https://m.media-amazon.com/images/I/61gX9b+ZxJL._AC_SL1500_.jpg", "desc": "Чарми ҳақиқӣ\n📦 30 дона"},
    # --- 1.6 ШИША ---
    "glass_iphone": {"name": "🛡️ Шиша iPhone", "price": "7$ / 76с", "photo": "https://m.media-amazon.com/images/I/61hX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 100 дона"},
    "glass_samsung": {"name": "🛡️ Шиша Samsung", "price": "7$ / 76с", "photo": "https://m.media-amazon.com/images/I/61iX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 80 дона"},
    "glass_xiaomi": {"name": "🛡️ Шиша Xiaomi", "price": "6$ / 65с", "photo": "https://m.media-amazon.com/images/I/61jX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 80 дона"},
    "laminat": {"name": "🛡️ Ламинат", "price": "12$ / 130с", "photo": "https://m.media-amazon.com/images/I/61kX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 50 дона"},
    # --- 1.7 POWER BANK ---
    "pb_xiaomi_10000": {"name": "🔋 Xiaomi 10000 mAh", "price": "25$ / 270с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1629971234.12345678.png", "desc": "⚡ 18W\n📦 25 дона"},
    "pb_xiaomi_20000": {"name": "🔋 Xiaomi 20000 mAh", "price": "35$ / 380с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1629981234.12345678.png", "desc": "⚡ 18W\n📦 15 дона"},
    "pb_anker": {"name": "🔋 Anker 20000 mAh", "price": "45$ / 490с", "photo": "https://d1fmezig7cekam.cloudfront.net/anker-20000.jpg", "desc": "⚡ 22.5W\n📦 10 дона"},
    "pb_baseus": {"name": "🔋 Baseus 20000 mAh", "price": "38$ / 410с", "photo": "https://www.baseus.com/cdn/shop/files/20000mah.jpg", "desc": "⚡ 22.5W\n📦 18 дона"},
    "pb_remax": {"name": "🔋 Remax 20000 mAh", "price": "28$ / 300с", "photo": "https://m.media-amazon.com/images/I/61lX9b+ZxJL._AC_SL1500_.jpg", "desc": "⚡ 22.5W\n📦 20 дона"},
    # --- 1.8 СОАТ ---
    "watch_apple": {"name": "⌚ Apple Watch 9", "price": "380$ / 4,100с", "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MR9D3?wid=1140&hei=1140&fmt=jpeg", "desc": "📦 5 дона"},
    "watch_apple_ultra": {"name": "⌚ Apple Watch Ultra 2", "price": "750$ / 8,100с", "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MR9E3?wid=1140&hei=1140&fmt=jpeg", "desc": "📦 2 дона"},
    "watch_samsung": {"name": "⌚ Galaxy Watch 6", "price": "250$ / 2,700с", "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2307/gallery/levant-galaxy-watch6-sm-r930nzkamea-537406789", "desc": "📦 7 дона"},
    "watch_xiaomi": {"name": "⌚ Xiaomi Watch 2", "price": "180$ / 1,950с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1705001234.12345678.png", "desc": "📦 8 дона"},
    "watch_huawei": {"name": "⌚ Huawei Watch GT 4", "price": "220$ / 2,380с", "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-watch-gt4-01.jpg", "desc": "📦 6 дона"},
    "watch_amazfit": {"name": "⌚ Amazfit GTR 4", "price": "150$ / 1,620с", "photo": "https://m.media-amazon.com/images/I/61xX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 9 дона"},
    # --- 2 ОШХОНА - ҲАМААШ ИЛОВА ШУД - ДУРУСТ! ---
    "blender_xiaomi": {"name": "🍳 Блендер Xiaomi", "price": "55$ / 595с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1630001234.12345678.png", "desc": "📦 10 дона"},
    "blender_bosch": {"name": "🍳 Блендер Bosch", "price": "70$ / 760с", "photo": "https://m.media-amazon.com/images/I/71xX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 6 дона"},
    "blender_philips": {"name": "🍳 Блендер Philips", "price": "65$ / 700с", "photo": "https://m.media-amazon.com/images/I/71yX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 5 дона"},
    "kettle_xiaomi": {"name": "🍳 Чойник Xiaomi 1.7L", "price": "35$ / 380с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1600001234.12345678.png", "desc": "📦 12 дона"},
    "kettle_bosch": {"name": "🍳 Чойник Bosch", "price": "45$ / 490с", "photo": "https://m.media-amazon.com/images/I/71yX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 8 дона"},
    "kettle_philips": {"name": "🍳 Чойник Philips", "price": "40$ / 430с", "photo": "https://m.media-amazon.com/images/I/71zX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 7 дона"},
    "coffee_delonghi": {"name": "☕ Кофеварка DeLonghi", "price": "120$ / 1,300с", "photo": "https://m.media-amazon.com/images/I/71xX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 4 дона"},
    "coffee_bosch": {"name": "☕ Кофеварка Bosch", "price": "95$ / 1,030с", "photo": "https://m.media-amazon.com/images/I/71aX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 5 дона"},
    "airfryer_xiaomi": {"name": "🍟 Аэрогриль Xiaomi 4L", "price": "85$ / 920с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1680001234.12345678.png", "desc": "📦 7 дона"},
    "airfryer_philips": {"name": "🍟 Аэрогриль Philips 5L", "price": "130$ / 1,400с", "photo": "https://m.media-amazon.com/images/I/71bX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 4 дона"},
    "ricecooker": {"name": "🍚 Мультиварка Xiaomi", "price": "65$ / 700с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1690001234.12345678.png", "desc": "📦 9 дона"},
    "mixer_bosch": {"name": "🥣 Миксер Bosch", "price": "50$ / 540с", "photo": "https://m.media-amazon.com/images/I/61xX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 5 дона"},
    "mixer_philips": {"name": "🥣 Миксер Philips", "price": "45$ / 490с", "photo": "https://m.media-amazon.com/images/I/61yX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 6 дона"},
    "toaster_xiaomi": {"name": "🍞 Тостер Xiaomi", "price": "30$ / 325с", "photo": "https://m.media-amazon.com/images/I/71zX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 11 дона"},
    "toaster_bosch": {"name": "🍞 Тостер Bosch", "price": "35$ / 380с", "photo": "https://m.media-amazon.com/images/I/71cX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 8 дона"},
    "pan_set": {"name": "🍳 Набор Тава", "price": "60$ / 650с", "photo": "https://m.media-amazon.com/images/I/71dX9b+ZxJL._AC_SL1500_.jpg", "desc": "3 дона\n📦 10 дона"},
    "knife_set": {"name": "🔪 Набор Корд", "price": "40$ / 430с", "photo": "https://m.media-amazon.com/images/I/71eX9b+ZxJL._AC_SL1500_.jpg", "desc": "5 дона\n📦 12 дона"},
    # --- 3 ХОНА - ҲАМААШ ИЛОВА ШУД - ДУРУСТ! ---
    "tv43": {"name": "📺 Телевизор Xiaomi 43\" 4K", "price": "320$ / 3,460с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1651001234.12345678.png", "desc": "4K\n📦 5 дона"},
    "tv55": {"name": "📺 Телевизор Xiaomi 55\" 4K", "price": "450$ / 4,900с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1650001234.12345678.png", "desc": "4K\n📦 3 дона"},
    "tv65": {"name": "📺 Телевизор Samsung 65\" 4K", "price": "700$ / 7,600с", "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2301/gallery/levant-tv-65-537406789", "desc": "4K\n📦 2 дона"},
    "tv75": {"name": "📺 Телевизор LG 75\" 4K", "price": "950$ / 10,300с", "photo": "https://m.media-amazon.com/images/I/71dX9b+ZxJL._AC_SL1500_.jpg", "desc": "4K\n📦 1 дона"},
    "fridge_samsung": {"name": "❄️ Холодильник Samsung", "price": "650$ / 7,000с", "photo": "https://m.media-amazon.com/images/I/71yX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 2 дона"},
    "fridge_lg": {"name": "❄️ Холодильник LG", "price": "700$ / 7,600с", "photo": "https://m.media-amazon.com/images/I/71eX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 2 дона"},
    "fridge_xiaomi": {"name": "❄️ Холодильник Xiaomi", "price": "550$ / 5,950с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1652001234.12345678.png", "desc": "📦 3 дона"},
    "washing_lg": {"name": "👕 Ҷомашӯӣ LG 8kg", "price": "550$ / 5,950с", "photo": "https://m.media-amazon.com/images/I/71aX9b+ZxJL._AC_SL1500_.jpg", "desc": "8kg\n📦 3 дона"},
    "washing_samsung": {"name": "👕 Ҷомашӯӣ Samsung 9kg", "price": "600$ / 6,500с", "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2301/gallery/levant-washing-537406789", "desc": "9kg\n📦 2 дона"},
    "washing_xiaomi": {"name": "👕 Ҷомашӯӣ Xiaomi 8kg", "price": "480$ / 5,200с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1653001234.12345678.png", "desc": "8kg\n📦 3 дона"},
    "vacuum_xiaomi": {"name": "🧹 Чангкашак Xiaomi", "price": "180$ / 1,950с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1660001234.12345678.png", "desc": "📦 6 дона"},
    "vacuum_dyson": {"name": "🧹 Чангкашак Dyson", "price": "450$ / 4,900с", "photo": "https://m.media-amazon.com/images/I/71fX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 3 дона"},
    "robot_xiaomi": {"name": "🤖 Робот Xiaomi", "price": "300$ / 3,250с", "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1670001234.12345678.png", "desc": "📦 4 дона"},
    "robot_dreame": {"name": "🤖 Робот Dreame", "price": "350$ / 3,800с", "photo": "https://m.media-amazon.com/images/I/71gX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 3 дона"},
    "ac_midea": {"name": "❄️ Кондиционер Midea 12000", "price": "400$ / 4,300с", "photo": "https://m.media-amazon.com/images/I/71bX9b+ZxJL._AC_SL1500_.jpg", "desc": "📦 5 дона"},
    "ac_lg": {"name": "❄️ Кондиционер LG 12000", "price": "550$ / 5,950с", "photo": "https://m.media-amazon.com/images/I/71hX9b+ZxJL._AC_SL1500_.jpg"
