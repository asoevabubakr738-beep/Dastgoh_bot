# ============================================================
# БОТИ ГУАНЧЖОУ
# ============================================================
# Версия: 4.0 - ДУРУСТ
# Сатр: 700+
# Ҳар як сатр алоҳида - барои ҳамин зиёд аст
# ============================================================

import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

SHOP_NAME = "ГУАНЧЖОУ"
SHOP_PHONE = "+992 783829009"
SHOP_USERNAME = "@guangzhou_tj"
SHOP_ADDRESS = "Душанбе, Гуанчжоу Маркет"
SHOP_TIME = "9:00 - 21:00"

# ============================================================
# PRODUCTS - ҲАР ЯК МАҲСУЛОТ 6 САТР
# ============================================================

PRODUCTS = {}

# ------------------------------------------------------------
# 1.1 APPLE
# ------------------------------------------------------------

PRODUCTS["iphone13"] = {
    "name": "📱 iPhone 13",
    "price": "750$ / 8,100с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-13-01.jpg",
    "desc": "💾 128GB\n📦 5 дона",
}

PRODUCTS["iphone14"] = {
    "name": "📱 iPhone 14",
    "price": "850$ / 9,200с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-01.jpg",
    "desc": "💾 128GB\n📦 4 дона",
}

PRODUCTS["iphone14pro"] = {
    "name": "📱 iPhone 14 Pro",
    "price": "950$ / 10,300с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-pro-01.jpg",
    "desc": "💾 256GB\n📦 3 дона",
}

PRODUCTS["iphone15"] = {
    "name": "📱 iPhone 15",
    "price": "950$ / 10,300с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-01.jpg",
    "desc": "💾 128GB\n📦 3 дона",
}

PRODUCTS["iphone15pro"] = {
    "name": "📱 iPhone 15 Pro",
    "price": "1150$ / 12,400с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-pro-01.jpg",
    "desc": "💾 256GB\n📦 2 дона",
}

PRODUCTS["iphone16"] = {
    "name": "📱 iPhone 16",
    "price": "1050$ / 11,300с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-16-01.jpg",
    "desc": "💾 128GB\n📦 4 дона",
}

PRODUCTS["iphone16pro"] = {
    "name": "📱 iPhone 16 Pro",
    "price": "1250$ / 13,500с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-16-pro-01.jpg",
    "desc": "💾 256GB\n📦 2 дона",
}

# ------------------------------------------------------------
# 1.1 SAMSUNG
# ------------------------------------------------------------

PRODUCTS["samsung_a15"] = {
    "name": "📱 Samsung A15",
    "price": "180$ / 1,950с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a15-01.jpg",
    "desc": "💾 128GB\n📦 12 дона",
}

PRODUCTS["samsung_a35"] = {
    "name": "📱 Samsung A35",
    "price": "350$ / 3,800с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a35-01.jpg",
    "desc": "💾 128GB\n📦 8 дона",
}

PRODUCTS["samsung_a55"] = {
    "name": "📱 Samsung A55",
    "price": "450$ / 4,900с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-a55-01.jpg",
    "desc": "💾 128GB\n📦 10 дона",
}

PRODUCTS["samsung_s23"] = {
    "name": "📱 Samsung S23",
    "price": "700$ / 7,600с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s23-5g-01.jpg",
    "desc": "💾 256GB\n📦 3 дона",
}

PRODUCTS["samsung_s24"] = {
    "name": "📱 Samsung S24",
    "price": "850$ / 9,200с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24-5g-01.jpg",
    "desc": "💾 256GB\n📦 4 дона",
}

PRODUCTS["samsung_s24u"] = {
    "name": "📱 Samsung S24 Ultra",
    "price": "1150$ / 12,400с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24-ultra-5g-01.jpg",
    "desc": "💾 512GB\n📦 2 дона",
}

# ------------------------------------------------------------
# 1.1 XIAOMI
# ------------------------------------------------------------

PRODUCTS["redmi_13c"] = {
    "name": "📱 Redmi 13C",
    "price": "140$ / 1,500с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-13c-01.jpg",
    "desc": "💾 128GB\n📦 20 дона",
}

PRODUCTS["redmi_note13"] = {
    "name": "📱 Redmi Note 13",
    "price": "220$ / 2,400с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-13-01.jpg",
    "desc": "💾 256GB\n📦 15 дона",
}

PRODUCTS["redmi_note13pro"] = {
    "name": "📱 Redmi Note 13 Pro",
    "price": "300$ / 3,250с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-13-pro-01.jpg",
    "desc": "💾 256GB\n📦 8 дона",
}

PRODUCTS["redmi_note14"] = {
    "name": "📱 Redmi Note 14",
    "price": "280$ / 3,000с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-14-01.jpg",
    "desc": "💾 256GB\n📦 8 дона",
}

PRODUCTS["poco_x6"] = {
    "name": "📱 Poco X6",
    "price": "320$ / 3,500с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-poco-x6-01.jpg",
    "desc": "💾 256GB\n📦 6 дона",
}

PRODUCTS["xiaomi14"] = {
    "name": "📱 Xiaomi 14",
    "price": "700$ / 7,600с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-14-01.jpg",
    "desc": "💾 512GB\n📦 3 дона",
}

# ------------------------------------------------------------
# 1.1 HONOR / HUAWEI / VIVO / OPPO
# ------------------------------------------------------------

PRODUCTS["honor_x8b"] = {
    "name": "📱 Honor X8b",
    "price": "250$ / 2,700с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-x8b-01.jpg",
    "desc": "💾 256GB\n📦 7 дона",
}

PRODUCTS["honor_x9b"] = {
    "name": "📱 Honor X9b",
    "price": "320$ / 3,500с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-x9b-01.jpg",
    "desc": "💾 256GB\n📦 6 дона",
}

PRODUCTS["honor_90"] = {
    "name": "📱 Honor 90",
    "price": "450$ / 4,900с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-90-01.jpg",
    "desc": "💾 512GB\n📦 4 дона",
}

PRODUCTS["honor_magic6"] = {
    "name": "📱 Honor Magic 6",
    "price": "800$ / 8,600с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/honor/honor-magic6-01.jpg",
    "desc": "💾 512GB\n📦 2 дона",
}

PRODUCTS["huawei_nova12"] = {
    "name": "📱 Huawei Nova 12",
    "price": "400$ / 4,300с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-nova-12-01.jpg",
    "desc": "💾 256GB\n📦 5 дона",
}

PRODUCTS["huawei_pura70"] = {
    "name": "📱 Huawei Pura 70",
    "price": "650$ / 7,000с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-pura-70-01.jpg",
    "desc": "💾 256GB\n📦 3 дона",
}

PRODUCTS["vivo_y100"] = {
    "name": "📱 Vivo Y100",
    "price": "280$ / 3,000с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/vivo/vivo-y100-01.jpg",
    "desc": "💾 256GB\n📦 6 дона",
}

PRODUCTS["oppo_a78"] = {
    "name": "📱 Oppo A78",
    "price": "260$ / 2,800с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/oppo/oppo-a78-01.jpg",
    "desc": "💾 256GB\n📦 7 дона",
}

PRODUCTS["oppo_reno11"] = {
    "name": "📱 Oppo Reno 11",
    "price": "450$ / 4,900с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/oppo/oppo-reno11-01.jpg",
    "desc": "💾 256GB\n📦 4 дона",
}

# ------------------------------------------------------------
# 1.2 НАУШНИК
# ------------------------------------------------------------

PRODUCTS["airpods_pro2"] = {
    "name": "🎧 AirPods Pro 2",
    "price": "180$ / 1,950с",
    "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=1140&hei=1140&fmt=jpeg",
    "desc": "🔋 30 соат\n📦 20 дона",
}

PRODUCTS["airpods2"] = {
    "name": "🎧 AirPods 2",
    "price": "95$ / 1,030с",
    "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MV7N2?wid=1140&hei=1140&fmt=jpeg",
    "desc": "🔋 24 соат\n📦 15 дона",
}

PRODUCTS["airpods3"] = {
    "name": "🎧 AirPods 3",
    "price": "130$ / 1,400с",
    "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MME73?wid=1140&hei=1140&fmt=jpeg",
    "desc": "🔋 30 соат\n📦 10 дона",
}

PRODUCTS["airpods_max"] = {
    "name": "🎧 AirPods Max",
    "price": "450$ / 4,900с",
    "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-max-select-202409-midnight?wid=1140&hei=1140&fmt=jpeg",
    "desc": "🔋 20 соат\n📦 3 дона",
}

PRODUCTS["buds2"] = {
    "name": "🎧 Galaxy Buds 2",
    "price": "75$ / 810с",
    "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2208/gallery/levant-galaxy-buds2-pro-sm-r510nzwamea-533227276",
    "desc": "🔋 29 соат\n📦 12 дона",
}

PRODUCTS["buds_pro"] = {
    "name": "🎧 Galaxy Buds 2 Pro",
    "price": "110$ / 1,190с",
    "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2208/gallery/levant-galaxy-buds2-pro-sm-r510nzwamea-533227276",
    "desc": "🔋 30 соат\n📦 8 дона",
}

PRODUCTS["redmi_buds5"] = {
    "name": "🎧 Redmi Buds 5",
    "price": "35$ / 380с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1699261234.12345678.png",
    "desc": "🔋 38 соат\n📦 30 дона",
}

PRODUCTS["redmi_buds_pro"] = {
    "name": "🎧 Redmi Buds 5 Pro",
    "price": "55$ / 595с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1700001234.12345678.png",
    "desc": "🔋 38 соат\n📦 15 дона",
}

PRODUCTS["jbl_tune"] = {
    "name": "🎧 JBL Tune 230",
    "price": "50$ / 540с",
    "photo": "https://m.media-amazon.com/images/I/61xX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "🔋 40 соат\n📦 12 дона",
}

PRODUCTS["wired"] = {
    "name": "🎧 Наушник симӣ",
    "price": "10$ / 108с",
    "photo": "https://m.media-amazon.com/images/I/61yX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 50 дона",
}

# ------------------------------------------------------------
# 1.3 ЗАРЯДНИК
# ------------------------------------------------------------

PRODUCTS["charge_20w"] = {
    "name": "🔌 Зарядник 20W Apple",
    "price": "15$ / 160с",
    "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MHJE3?wid=1140&hei=1140&fmt=jpeg",
    "desc": "⚡ 20W\n📦 30 дона",
}

PRODUCTS["charge_33w"] = {
    "name": "🔌 Зарядник 33W Xiaomi",
    "price": "20$ / 215с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1610001234.12345678.png",
    "desc": "⚡ 33W\n📦 25 дона",
}
PRODUCTS["coffee_bosch"] = {
PRODUCTS["charge_67w"] = {
    "name": "🔌 Зарядник 67W Xiaomi",
    "price": "30$ / 325с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1620001234.12345678.png",
    "desc": "⚡ 67W\n📦 18 дона",
}

PRODUCTS["charge_120w"] = {
    "name": "🔌 Зарядник 120W Xiaomi",
    "price": "45$ / 490с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1635001234.12345678.png",
    "desc": "⚡ 120W\n📦 10 дона",
}

PRODUCTS["charge_anker"] = {
    "name": "🔌 Зарядник Anker 65W",
    "price": "35$ / 380с",
    "photo": "https://m.media-amazon.com/images/I/61zX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "⚡ 65W GaN\n📦 12 дона",
}

# ------------------------------------------------------------
# 1.4 КАБЕЛ
# ------------------------------------------------------------

PRODUCTS["cable_typec"] = {
    "name": "🔗 Кабел Type-C 1м",
    "price": "8$ / 86с",
    "photo": "https://m.media-amazon.com/images/I/61aX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 50 дона",
}

PRODUCTS["cable_light"] = {
    "name": "🔗 Кабел Lightning 1м",
    "price": "10$ / 108с",
    "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MXLY2?wid=1140&hei=1140&fmt=jpeg",
    "desc": "📦 40 дона",
}

PRODUCTS["cable_micro"] = {
    "name": "🔗 Кабел Micro-USB",
    "price": "5$ / 54с",
    "photo": "https://m.media-amazon.com/images/I/61bX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 60 дона",
}

PRODUCTS["cable_2m"] = {
    "name": "🔗 Кабел Type-C 2м",
    "price": "12$ / 130с",
    "photo": "https://m.media-amazon.com/images/I/61cX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 30 дона",
}

# ------------------------------------------------------------
# 1.5 ЧЕХОЛ
# ------------------------------------------------------------

PRODUCTS["case_iphone"] = {
    "name": "📱 Чехол iPhone",
    "price": "10$ / 108с",
    "photo": "https://m.media-amazon.com/images/I/61dX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "Ҳамаи модел\n📦 100 дона",
}

PRODUCTS["case_samsung"] = {
    "name": "📱 Чехол Samsung",
    "price": "8$ / 86с",
    "photo": "https://m.media-amazon.com/images/I/61eX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "Ҳамаи модел\n📦 80 дона",
}

PRODUCTS["case_xiaomi"] = {
    "name": "📱 Чехол Xiaomi",
    "price": "8$ / 86с",
    "photo": "https://m.media-amazon.com/images/I/61fX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "Ҳамаи модел\n📦 80 дона",
}

PRODUCTS["case_leather"] = {
    "name": "📱 Чехол Чармӣ",
    "price": "18$ / 195с",
    "photo": "https://m.media-amazon.com/images/I/61gX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "Чарми ҳақиқӣ\n📦 30 дона",
}

# ------------------------------------------------------------
# 1.6 ШИША
# ------------------------------------------------------------

PRODUCTS["glass_iphone"] = {
    "name": "🛡️ Шиша iPhone",
    "price": "7$ / 76с",
    "photo": "https://m.media-amazon.com/images/I/61hX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 100 дона",
}

PRODUCTS["glass_samsung"] = {
    "name": "🛡️ Шиша Samsung",
    "price": "7$ / 76с",
    "photo": "https://m.media-amazon.com/images/I/61iX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 80 дона",
}

PRODUCTS["glass_xiaomi"] = {
    "name": "🛡️ Шиша Xiaomi",
    "price": "6$ / 65с",
    "photo": "https://m.media-amazon.com/images/I/61jX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 80 дона",
}

PRODUCTS["laminat"] = {
    "name": "🛡️ Ламинат",
    "price": "12$ / 130с",
    "photo": "https://m.media-amazon.com/images/I/61kX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 50 дона",
}

# ------------------------------------------------------------
# 1.7 POWER BANK
# ------------------------------------------------------------

PRODUCTS["pb_xiaomi_10000"] = {
    "name": "🔋 Xiaomi 10000 mAh",
    "price": "25$ / 270с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1629971234.12345678.png",
    "desc": "⚡ 18W\n📦 25 дона",
}

PRODUCTS["pb_xiaomi_20000"] = {
    "name": "🔋 Xiaomi 20000 mAh",
    "price": "35$ / 380с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1629981234.12345678.png",
    "desc": "⚡ 18W\n📦 15 дона",
}

PRODUCTS["pb_anker"] = {
    "name": "🔋 Anker 20000 mAh",
    "price": "45$ / 490с",
    "photo": "https://d1fmezig7cekam.cloudfront.net/anker-20000.jpg",
    "desc": "⚡ 22.5W\n📦 10 дона",
}

PRODUCTS["pb_baseus"] = {
    "name": "🔋 Baseus 20000 mAh",
    "price": "38$ / 410с",
    "photo": "https://www.baseus.com/cdn/shop/files/20000mah.jpg",
    "desc": "⚡ 22.5W\n📦 18 дона",
}

PRODUCTS["pb_remax"] = {
    "name": "🔋 Remax 20000 mAh",
    "price": "28$ / 300с",
    "photo": "https://m.media-amazon.com/images/I/61lX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "⚡ 22.5W\n📦 20 дона",
}

# ------------------------------------------------------------
# 1.8 СОАТ
# ------------------------------------------------------------

PRODUCTS["watch_apple"] = {
    "name": "⌚ Apple Watch 9",
    "price": "380$ / 4,100с",
    "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MR9D3?wid=1140&hei=1140&fmt=jpeg",
    "desc": "📦 5 дона",
}

PRODUCTS["watch_apple_ultra"] = {
    "name": "⌚ Apple Watch Ultra 2",
    "price": "750$ / 8,100с",
    "photo": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MR9E3?wid=1140&hei=1140&fmt=jpeg",
    "desc": "📦 2 дона",
}

PRODUCTS["watch_samsung"] = {
    "name": "⌚ Galaxy Watch 6",
    "price": "250$ / 2,700с",
    "photo": "https://images.samsung.com/is/image/samsung/p6pim/levant/2307/gallery/levant-galaxy-watch6-sm-r930nzkamea-537406789",
    "desc": "📦 7 дона",
}

PRODUCTS["watch_xiaomi"] = {
    "name": "⌚ Xiaomi Watch 2",
    "price": "180$ / 1,950с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1705001234.12345678.png",
    "desc": "📦 8 дона",
}

PRODUCTS["watch_huawei"] = {
    "name": "⌚ Huawei Watch GT 4",
    "price": "220$ / 2,380с",
    "photo": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-watch-gt4-01.jpg",
    "desc": "📦 6 дона",
}

PRODUCTS["watch_amazfit"] = {
    "name": "⌚ Amazfit GTR 4",
    "price": "150$ / 1,620с",
    "photo": "https://m.media-amazon.com/images/I/61xX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 9 дона",
}

# ------------------------------------------------------------
# 2 ОШХОНА
# ------------------------------------------------------------

PRODUCTS["blender_xiaomi"] = {
    "name": "🍳 Блендер Xiaomi",
    "price": "55$ / 595с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1630001234.12345678.png",
    "desc": "📦 10 дона",
}

PRODUCTS["blender_bosch"] = {
    "name": "🍳 Блендер Bosch",
    "price": "70$ / 760с",
    "photo": "https://m.media-amazon.com/images/I/71xX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 6 дона",
}

PRODUCTS["blender_philips"] = {
    "name": "🍳 Блендер Philips",
    "price": "65$ / 700с",
    "photo": "https://m.media-amazon.com/images/I/71yX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 5 дона",
}

PRODUCTS["kettle_xiaomi"] = {
    "name": "🍳 Чойник Xiaomi 1.7L",
    "price": "35$ / 380с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1600001234.12345678.png",
    "desc": "📦 12 дона",
}

PRODUCTS["kettle_bosch"] = {
    "name": "🍳 Чойник Bosch",
    "price": "45$ / 490с",
    "photo": "https://m.media-amazon.com/images/I/71yX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 8 дона",
}

PRODUCTS["kettle_philips"] = {
    "name": "🍳 Чойник Philips",
    "price": "40$ / 430с",
    "photo": "https://m.media-amazon.com/images/I/71zX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 7 дона",
}

PRODUCTS["coffee_delonghi"] = {
    "name": "☕ Кофеварка DeLonghi",
    "price": "120$ / 1,300с",
    "photo": "https://m.media-amazon.com/images/I/71xX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 4 дона",
}

PRODUCTS["coffee_bosch"]
PRODUCTS["coffee_bosch"] = {
    "name": "☕ Кофеварка Bosch",
    "price": "95$ / 1,030с",
    "photo": "https://m.media-amazon.com/images/I/71aX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 5 дона",
}

PRODUCTS["coffee_philips"] = {
    "name": "☕ Кофеварка Philips",
    "price": "85$ / 920с",
    "photo": "https://m.media-amazon.com/images/I/71bX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 6 дона",
}

PRODUCTS["iron_philips"] = {
    "name": "👕 Утюг Philips",
    "price": "45$ / 490с",
    "photo": "https://m.media-amazon.com/images/I/71cX9b+ZxJL._AC_SL1500_.jpg",
    "desc": "📦 10 дона",
}

PRODUCTS["vacuum_xiaomi"] = {
    "name": "🧹 Пылесос Xiaomi",
    "price": "180$ / 1,950с",
    "photo": "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E08F55F/pms_1640001234.12345678.png",
    "desc": "📦 4 дона",
}

CATEGORIES = {
    "phones": ["iphone13", "iphone14", "iphone14pro", "iphone15", "iphone15pro", "iphone16", "iphone16pro", "samsung_a15", "samsung_a35", "samsung_a55", "samsung_s23", "samsung_s24", "samsung_s24u", "redmi_13c", "redmi_note13", "redmi_note13pro", "redmi_note14", "poco_x6", "xiaomi14", "honor_x8b", "honor_x9b", "honor_90", "honor_magic6", "huawei_nova12", "huawei_pura70", "vivo_y100", "oppo_a78", "oppo_reno11"],
    "audio": ["airpods_pro2", "airpods2", "airpods3", "airpods_max", "buds2", "buds_pro", "redmi_buds5", "redmi_buds_pro", "jbl_tune", "wired"],
    "charge": ["charge_20w", "charge_33w", "charge_67w", "charge_120w", "charge_anker", "cable_typec", "cable_light", "cable_micro", "cable_2m"],
    "case": ["case_iphone", "case_samsung", "case_xiaomi", "case_leather", "glass_iphone", "glass_samsung", "glass_xiaomi", "laminat"],
    "power": ["pb_xiaomi_10000", "pb_xiaomi_20000", "pb_anker", "pb_baseus", "pb_remax"],
    "watch": ["watch_apple", "watch_apple_ultra", "watch_samsung", "watch_xiaomi", "watch_huawei", "watch_amazfit"],
    "kitchen": ["blender_xiaomi", "blender_bosch", "blender_philips", "kettle_xiaomi", "kettle_bosch", "kettle_philips", "coffee_delonghi", "coffee_bosch", "coffee_philips", "iron_philips", "vacuum_xiaomi"],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 Телефонҳо", callback_data="cat_phones")],
        [InlineKeyboardButton("🎧 Наушник", callback_data="cat_audio")],
        [InlineKeyboardButton("🔌 Зарядник ва Кабел", callback_data="cat_charge")],
        [InlineKeyboardButton("📱 Чехол ва Шиша", callback_data="cat_case")],
        [InlineKeyboardButton("🔋 Power Bank", callback_data="cat_power")],
        [InlineKeyboardButton("⌚ Соат", callback_data="cat_watch")],
        [InlineKeyboardButton("🍳 Ошхона", callback_data="cat_kitchen")],
        [InlineKeyboardButton("📞 Алоқа", callback_data="contact")],
    ]
    text = f"🏪 {SHOP_NAME}\n\n📍 {SHOP_ADDRESS}\n🕐 {SHOP_TIME}\n📞 {SHOP_PHONE}\n\nКатегорияро интихоб кун:"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat = query.data.replace("cat_", "")
    keyboard = []
    for key in CATEGORIES.get(cat, []):
        p = PRODUCTS[key]
        keyboard.append([InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"prod_{key}")])
    keyboard.append([InlineKeyboardButton("⬅️ Бозгашт", callback_data="back_start")])
    await query.edit_message_text("Маҳсулотро интихоб кун:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data.replace("prod_", "")
    p = PRODUCTS[key]
    keyboard = [
        [InlineKeyboardButton("🛒 Фармоиш додан", callback_data=f"order_{key}")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="back_start")],
    ]
    caption = f"{p['name']}\n\n💰 Нарх: {p['price']}\n\n{p['desc']}\n\n📍 {SHOP_ADDRESS}"
    try:
        await query.message.reply_photo(photo=p['photo'], caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await query.message.reply_text(caption, reply_markup=InlineKeyboardMarkup(keyboard))

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data.replace("order_", "")
    p = PRODUCTS[key]
    user = query.from_user
    await query.message.reply_text(f"✅ Фармоиши ту қабул шуд!\n\n{p['name']}\n💰 {p['price']}\n\n👤 {user.first_name} (@{user.username})\n\nМо ба зудӣ бо ту алоқа мекунем!\n📞 {SHOP_PHONE}")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"📞 Алоқа:\n\n🏪 {SHOP_NAME}\n📍 {SHOP_ADDRESS}\n🕐 {SHOP_TIME}\n📞 {SHOP_PHONE}\n✈️ {SHOP_USERNAME}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Бозгашт", callback_data="back_start")]]))

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

def main():
    if not TOKEN:
        logger.error("BOT_TOKEN нест!")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_category, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(show_product, pattern="^prod_"))
    app.add_handler(CallbackQueryHandler(order, pattern="^order_"))
    app.add_handler(CallbackQueryHandler(contact, pattern="^contact$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back_start$"))
    logger.info("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
