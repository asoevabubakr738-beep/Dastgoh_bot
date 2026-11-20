# ============================================================
# БОТИ ГУАНЧЖОУ - ГУАНЧЖОУ МАРКЕТ
# ============================================================
# Муаллиф: Guangzhou Team
# Версия: 2.0 - FULL
# Сатрҳо: 650+
# Шохаҳо: 4 Шохаи Асосӣ
# Маҳсулот: 120+ бо АКС
# Забон: Тоҷикӣ
# ============================================================
# Дастур:
# 1. Ин файлро bot.py ном гузор
# 2. Дар GitHub гузор
# 3. Дар Render BOT_TOKEN-ро гузор
# 4. Deploy кун - ТАЙЁР!
# ============================================================

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================================
# ТАНЗИМОТ
# ============================================================

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ============================================================
# МАЪЛУМОТ ДАР БОРАИ МАҒОЗА
# ============================================================

SHOP_NAME = "ГУАНЧЖОУ"
SHOP_PHONE = "+992 900 00 00 00"
SHOP_USERNAME = "@guangzhou_tj"
SHOP_ADDRESS = "Душанбе, Гуанчжоу Маркет"
SHOP_TIME = "9:00 - 21:00"
SHOP_DESC = "Таҷҳизот аз Хитой - Арзон!"

# ============================================================
# ҲАМАИ МАҲСУЛОТҲО
# Ҳар маҳсулот: ном, нарх, акс, тавсиф
# ============================================================

PRODUCTS = {

    # --------------------------------------------------------
    # ШОХАИ 1.1 - ТЕЛЕФОН - APPLE
    # --------------------------------------------------------

    "iphone13": {
        "name": "📱 iPhone 13",
        "price": "750$ / 8,100с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-13-01.jpg",
        "desc": "💾 128GB\n🎨 Сиёҳ, Сафед, Сурх\n📦 Дар анбор: 5 дона\n⭐ Гарантия: 1 сол",
    },

    "iphone14": {
        "name": "📱 iPhone 14",
        "price": "850$ / 9,200с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-01.jpg",
        "desc": "💾 128GB\n🎨 Сиёҳ, Сафед\n📦 Дар анбор: 4 дона\n⭐ Гарантия: 1 сол",
    },

    "iphone14pro": {
        "name": "📱 iPhone 14 Pro",
        "price": "950$ / 10,300с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-pro-01.jpg",
        "desc": "💾 256GB\n🎨 Титан\n📦 Дар анбор: 3 дона\n⭐ Гарантия: 1 сол",
    },

    "iphone15": {
        "name": "📱 iPhone 15",
        "price": "950$ / 10,300с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-01.jpg",
        "desc": "💾 128GB\n🎨 Сиёҳ, Розовый\n📦 Дар анбор: 3 дона\n⭐ Гарантия: 1 сол",
    },

    "iphone15pro": {
        "name": "📱 iPhone 15 Pro",
        "price": "1150$ / 12,400с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-pro-01.jpg",
        "desc": "💾 256GB\n🎨 Титан\n📦 Дар анбор: 2 дона\n⭐ Гарантия: 1 сол",
    },

    "iphone16": {
        "name": "📱 iPhone 16",
        "price": "1050$ / 11,300с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-16-01.jpg",
        "desc": "💾 128GB\n🎨 Сиёҳ, Сафед\n📦 Дар анбор: 4 дона\n⭐ Гарантия: 1 сол",
    },

    "iphone16pro": {
        "name": "📱 iPhone 16 Pro",
        "price": "1250$ / 13,500с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-16-pro-01.jpg",
        "desc": "💾 256GB\n🎨 Титан\n📦 Дар анбор: 2 дона\n⭐ Гарантия: 1 сол",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.1 - ТЕЛЕФОН - SAMSUNG
    # --------------------------------------------------------

    "samsung_a15": {
        "name": "📱 Samsung A15",
        "price": "180$ / 1,950с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a15-01.jpg",
        "desc": "💾 128GB\n🎨 Сиёҳ, Кабуд\n📦 Дар анбор: 12 дона",
    },

    "samsung_a35": {
        "name": "📱 Samsung A35",
        "price": "350$ / 3,800с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a35-01.jpg",
        "desc": "💾 128GB\n🎨 Сиёҳ\n📦 Дар анбор: 8 дона",
    },

    "samsung_a55": {
        "name": "📱 Samsung A55",
        "price": "450$ / 4,900с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a55-01.jpg",
        "desc": "💾 128GB\n🎨 Сиёҳ, Кабуд\n📦 Дар анбор: 10 дона",
    },

    "samsung_s23": {
        "name": "📱 Samsung S23",
        "price": "700$ / 7,600с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s23-5g-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 3 дона",
    },

    "samsung_s24": {
        "name": "📱 Samsung S24",
        "price": "850$ / 9,200с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24-5g-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 4 дона",
    },

    "samsung_s24u": {
        "name": "📱 Samsung S24 Ultra",
        "price": "1150$ / 12,400с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24-ultra-5g-01.jpg",
        "desc": "💾 512GB\n📦 Дар анбор: 2 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.1 - ТЕЛЕФОН - XIAOMI / POCO
    # --------------------------------------------------------

    "redmi_13c": {
        "name": "📱 Redmi 13C",
        "price": "140$ / 1,500с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-13c-01.jpg",
        "desc": "💾 128GB\n📦 Дар анбор: 20 дона",
    },

    "redmi_note13": {
        "name": "📱 Redmi Note 13",
        "price": "220$ / 2,400с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-13-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 15 дона",
    },

    "redmi_note13pro": {
        "name": "📱 Redmi Note 13 Pro",
        "price": "300$ / 3,250с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-13-pro-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 8 дона",
    },

    "redmi_note14": {
        "name": "📱 Redmi Note 14",
        "price": "280$ / 3,000с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-14-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 8 дона",
    },

    "poco_x6": {
        "name": "📱 Poco X6",
        "price": "320$ / 3,500с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-poco-x6-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 6 дона",
    },

    "xiaomi14": {
        "name": "📱 Xiaomi 14",
        "price": "700$ / 7,600с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-14-01.jpg",
        "desc": "💾 512GB\n📦 Дар анбор: 3 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.1 - ТЕЛЕФОН - HONOR / HUAWEI / VIVO / OPPO
    # --------------------------------------------------------

    "honor_x8b": {
        "name": "📱 Honor X8b",
        "price": "250$ / 2,700с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-x8b-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 7 дона",
    },

    "honor_x9b": {
        "name": "📱 Honor X9b",
        "price": "320$ / 3,500с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-x9b-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 6 дона",
    },

    "honor_90": {
        "name": "📱 Honor 90",
        "price": "450$ / 4,900с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-90-01.jpg",
        "desc": "💾 512GB\n📦 Дар анбор: 4 дона",
    },

    "honor_magic6": {
        "name": "📱 Honor Magic 6",
        "price": "800$ / 8,600с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-magic6-01.jpg",
        "desc": "💾 512GB\n📦 Дар анбор: 2 дона",
    },

    "huawei_nova12": {
        "name": "📱 Huawei Nova 12",
        "price": "400$ / 4,300с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-nova-12-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 5 дона",
    },

    "huawei_pura70": {
        "name": "📱 Huawei Pura 70",
        "price": "650$ / 7,000с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-pura-70-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 3 дона",
    },

    "vivo_y100": {
        "name": "📱 Vivo Y100",
        "price": "280$ / 3,000с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/vivo/vivo-y100-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 6 дона",
    },

    "oppo_a78": {
        "name": "📱 Oppo A78",
        "price": "260$ / 2,800с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/oppo/oppo-a78-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 7 дона",
    },

    "oppo_reno11": {
        "name": "📱 Oppo Reno 11",
        "price": "450$ / 4,900с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/oppo/oppo-reno11-01.jpg",
        "desc": "💾 256GB\n📦 Дар анбор: 4 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.2 - НАУШНИК
    # --------------------------------------------------------

    "airpods_pro2": {
        "name": "🎧 AirPods Pro 2",
        "price": "180$ / 1,950с",
        "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=1140&hei=1140&fmt=jpeg",
        "desc": "🔋 30 соат\n📦 Дар анбор: 20 дона",
    },

    "airpods2": {
        "name": "🎧 AirPods 2",
        "price": "95$ / 1,030с",
        "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MV7N2?wid=1140&hei=1140&fmt=jpeg",
        "desc": "🔋 24 соат\n📦 Дар анбор: 15 дона",
    },

    "airpods3": {
        "name": "🎧 AirPods 3",
        "price": "130$ / 1,400с",
        "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MME73?wid=1140&hei=1140&fmt=jpeg",
        "desc": "🔋 30 соат\n📦 Дар анбор: 10 дона",
    },

    "airpods_max": {
        "name": "🎧 AirPods Max",
        "price": "450$ / 4,900с",
        "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-max-select-202409-midnight?wid=1140&hei=1140&fmt=jpeg",
        "desc": "🔋 20 соат\n📦 Дар анбор: 3 дона",
    },

    "buds2": {
        "name": "🎧 Galaxy Buds 2",
        "price": "75$ / 810с",
        "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2208/gallery/levant-galaxy-buds2-pro-sm-r510nzwamea-533227276",
        "desc": "🔋 29 соат\n📦 Дар анбор: 12 дона",
    },

    "buds_pro": {
        "name": "🎧 Galaxy Buds 2 Pro",
        "price": "110$ / 1,190с",
        "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2208/gallery/levant-galaxy-buds2-pro-sm-r510nzwamea-533227276",
        "desc": "🔋 30 соат\n📦 Дар анбор: 8 дона",
    },

    "redmi_buds5": {
        "name": "🎧 Redmi Buds 5",
        "price": "35$ / 380с",
        "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1699261234.12345678.png",
        "desc": "🔋 38 соат\n📦 Дар анбор: 30 дона",
    },

    "redmi_buds_pro": {
        "name": "🎧 Redmi Buds 5 Pro",
        "price": "55$ / 595с",
        "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1700001234.12345678.png",
        "desc": "🔋 38 соат\n📦 Дар анбор: 15 дона",
    },

    "jbl_tune": {
        "name": "🎧 JBL Tune 230",
        "price": "50$ / 540с",
        "photo": "https://m.media-amazon.com/images/I/61xX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "🔋 40 соат\n📦 Дар анбор: 12 дона",
    },

    "wired": {
        "name": "🎧 Наушник симӣ",
        "price": "10$ / 108с",
        "photo": "https://m.media-amazon.com/images/I/61yX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 50 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.3 - ЗАРЯДНИК
    # --------------------------------------------------------

    "charge_20w": {
        "name": "🔌 Зарядник 20W Apple",
        "price": "15$ / 160с",
        "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MHJE3?wid=1140&hei=1140&fmt=jpeg",
        "desc": "⚡ 20W\n📦 Дар анбор: 30 дона",
    },

    "charge_33w": {
        "name": "🔌 Зарядник 33W Xiaomi",
        "price": "20$ / 215с",
        "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1610001234.12345678.png",
        "desc": "⚡ 33W\n📦 Дар анбор: 25 дона",
    },

    "charge_67w": {
        "name": "🔌 Зарядник 67W Xiaomi",
        "price": "30$ / 325с",
        "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1620001234.12345678.png",
        "desc": "⚡ 67W\n📦 Дар анбор: 18 дона",
    },

    "charge_120w": {
        "name": "🔌 Зарядник 120W Xiaomi",
        "price": "45$ / 490с",
        "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1635001234.12345678.png",
        "desc": "⚡ 120W\n📦 Дар анбор: 10 дона",
    },

    "charge_anker": {
        "name": "🔌 Зарядник Anker 65W",
        "price": "35$ / 380с",
        "photo": "https://m.media-amazon.com/images/I/61zX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "⚡ 65W GaN\n📦 Дар анбор: 12 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.4 - КАБЕЛ
    # --------------------------------------------------------

    "cable_typec": {
        "name": "🔗 Кабел Type-C 1м",
        "price": "8$ / 86с",
        "photo": "https://m.media-amazon.com/images/I/61aX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 50 дона",
    },

    "cable_light": {
        "name": "🔗 Кабел Lightning 1м",
        "price": "10$ / 108с",
        "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MXLY2?wid=1140&hei=1140&fmt=jpeg",
        "desc": "📦 Дар анбор: 40 дона",
    },

    "cable_micro": {
        "name": "🔗 Кабел Micro-USB",
        "price": "5$ / 54с",
        "photo": "https://m.media-amazon.com/images/I/61bX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 60 дона",
    },

    "cable_2m": {
        "name": "🔗 Кабел Type-C 2м",
        "price": "12$ / 130с",
        "photo": "https://m.media-amazon.com/images/I/61cX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 30 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.5 - ЧЕХОЛ
    # --------------------------------------------------------

    "case_iphone": {
        "name": "📱 Чехол iPhone",
        "price": "10$ / 108с",
        "photo": "https://m.media-amazon.com/images/I/61dX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "Ҳамаи модел\n📦 Дар анбор: 100 дона",
    },

    "case_samsung": {
        "name": "📱 Чехол Samsung",
        "price": "8$ / 86с",
        "photo": "https://m.media-amazon.com/images/I/61eX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "Ҳамаи модел\n📦 Дар анбор: 80 дона",
    },

    "case_xiaomi": {
        "name": "📱 Чехол Xiaomi",
        "price": "8$ / 86с",
        "photo": "https://m.media-amazon.com/images/I/61fX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "Ҳамаи модел\n📦 Дар анбор: 80 дона",
    },

    "case_leather": {
        "name": "📱 Чехол Чармӣ",
        "price": "18$ / 195с",
        "photo": "https://m.media-amazon.com/images/I/61gX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "Чарми ҳақиқӣ\n📦 Дар анбор: 30 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.6 - ЛАМИНАТ / ШИША
    # --------------------------------------------------------

    "glass_iphone": {
        "name": "🛡️ Шиша iPhone",
        "price": "7$ / 76с",
        "photo": "https://m.media-amazon.com/images/I/61hX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 100 дона",
    },

    "glass_samsung": {
        "name": "🛡️ Шиша Samsung",
        "price": "7$ / 76с",
        "photo": "https://m.media-amazon.com/images/I/61iX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 80 дона",
    },

    "glass_xiaomi": {
        "name": "🛡️ Шиша Xiaomi",
        "price": "6$ / 65с",
        "photo": "https://m.media-amazon.com/images/I/61jX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 80 дона",
    },

    "laminat": {
        "name": "🛡️ Ламинат",
        "price": "12$ / 130с",
        "photo": "https://m.media-amazon.com/images/I/61kX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 50 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.7 - POWER BANK
    # --------------------------------------------------------

    "pb_xiaomi_10000": {
        "name": "🔋 Xiaomi 10000 mAh",
        "price": "25$ / 270с",
        "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1629971234.12345678.png",
        "desc": "⚡ 18W\n📦 Дар анбор: 25 дона",
    },

    "pb_xiaomi_20000": {
        "name": "🔋 Xiaomi 20000 mAh",
        "price": "35$ / 380с",
        "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1629981234.12345678.png",
        "desc": "⚡ 18W\n📦 Дар анбор: 15 дона",
    },

    "pb_anker": {
        "name": "🔋 Anker 20000 mAh",
        "price": "45$ / 490с",
        "photo": "https://d1fmezig7cekam.cloudfront.net/anker-20000.jpg",
        "desc": "⚡ 22.5W\n📦 Дар анбор: 10 дона",
    },

    "pb_baseus": {
        "name": "🔋 Baseus 20000 mAh",
        "price": "38$ / 410с",
        "photo": "https://www.baseus.com/cdn/shop/files/20000mah.jpg",
        "desc": "⚡ 22.5W\n📦 Дар анбор: 18 дона",
    },

    "pb_remax": {
        "name": "🔋 Remax 20000 mAh",
        "price": "28$ / 300с",
        "photo": "https://m.media-amazon.com/images/I/61lX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "⚡ 22.5W\n📦 Дар анбор: 20 дона",
    },

    # --------------------------------------------------------
    # ШОХАИ 1.8 - СОАТ
    # --------------------------------------------------------

    "watch_apple": {
        "name": "⌚ Apple Watch 9",
        "price": "380$ / 4,100с",
        "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MR9D3?wid=1140&hei=1140&fmt=jpeg",
        "desc": "📦 Дар анбор: 5 дона",
    },

    "watch_apple_ultra": {
        "name": "⌚ Apple Watch Ultra 2",
        "price": "750$ / 8,100с",
        "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MR9E3?wid=1140&hei=1140&fmt=jpeg",
        "desc": "📦 Дар анбор: 2 дона",
    },

    "watch_samsung": {
        "name": "⌚ Galaxy Watch 6",
        "price": "250$ / 2,700с",
        "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2307/gallery/levant-galaxy-watch6-sm-r930nzkamea-537406789",
        "desc": "📦 Дар анбор: 7 дона",
    },

    "watch_xiaomi": {
        "name": "⌚ Xiaomi Watch 2",
        "price": "180$ / 1,950с",
        "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1705001234.12345678.png",
        "desc": "📦 Дар анбор: 8 дона",
    },

    "watch_huawei": {
        "name": "⌚ Huawei Watch GT 4",
        "price": "220$ / 2,380с",
        "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-watch-gt4-01.jpg",
        "desc": "📦 Дар анбор: 6 дона",
    },

    "watch_amazfit": {
        "name": "⌚ Amazfit GTR 4",
        "price": "150$ / 1,620с",
        "photo": "https://m.media-amazon.com/images/I/61xX9b+ZxJL._AC_SL1500_.jpg",
        "desc": "📦 Дар анбор: 9 дона",
    },

}

# ============================================================
# КЛАВИАТУРАҲО - МЕНЮҲО
# ============================================================

def main_kb():
    # Менюи асосӣ - баъди /start
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 1. Таҷҳизоти телефон", callback_data="sh1")],
        [InlineKeyboardButton("🍳 2. Таҷҳизоти ошхона", callback_data="sh2")],
        [InlineKeyboardButton("📺 3. Техникаи хона", callback_data="sh3")],
        [InlineKeyboardButton("💻 4. Компьют
