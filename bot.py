import telebot
from telebot import types
import sqlite3
import uuid
import logging
import random
from datetime import datetime

# --- КОНФИГУРАЦИЯ ---
API_TOKEN = '8756114797:AAEXhGfTLMihmEaBUZspuFgYPH2kWOIP-_4'
ADMIN_ID = 8512977613
SHOP_NAME = "Shop Magnet"
MANAGER_USERNAME = "Magnet004"
INFO_CHANNEL = "https://t.me/Magnet04"

# Ваше изображение
MAIN_IMG = "https://ru.files.fm/u/wupw7uda33"

# Банки
BANKS = {
    'Россия': ['Сбербанк', 'Т-Банк', 'Озон Банк', 'ВТБ', 'Альфа-Банк', 'Райффайзен'],
    'Украина': ['Monobank', 'PrivatBank', 'А-Банк', 'Ощадбанк', 'ПУМБ'],
    'Казахстан': ['Kaspi.kz', 'Halyk Bank', 'ForteBank', 'Jusan Bank'],
    'Беларусь': ['Беларусбанк', 'Приорбанк', 'МТБанк', 'Белгазпромбанк']
}

ALL_PRODUCT_NAMES = [
    "Гашиш Euro (Classic)", "Гашиш Ice-o-Lator (Top Tier)", "Гашиш Marocco Gold", "Гашиш Afghan Premium", 
    "Гашиш Nepal Stick", "Гашиш Fresh Frozen", "Гашиш Dry Sift",
    "Кокаин VHQ (92% Pure)", "Кокаин Fishscale (Bolivia)", "Кокаин Colombia High Quality", "Кокаин Royal White",
    "Кокаин Peru Premium", "Кокаин Crack (Rocks)",
    "Мефедрон Кристалл (Big Crystal)", "Мефедрон Мука (Classic)", "Мефедрон VHQ (Needle)", "Мефедрон Power Crystal",
    "Мефедрон Кристалл (Emerald)", "Мефедрон Мелкий Кристалл (Sugar)",
    "Амфетамин Sulphate (High Speed)", "Амфетамин Pink Panther", "Амфетамин Euro Speed", 
    "Амфетамин VHQ White", "Амфетамин Фосфат",
    "Шишки AK-47 (Indoor)", "Шишки Amnesia Haze (Extra)", "Шишки Gorilla Glue #4", 
    "Шишки White Widow (Classic)", "Шишки OG Kush (Strong)", "Шишки Lemon Haze (Citrus)", 
    "Шишки Girl Scout Cookies", "Шишки Jack Herer", "Шишки Northern Lights", "Шишки Pineapple Express",
    "Альфа-ПВП Blue Sky", "Альфа-ПВП Crystal Clear", "Альфа-ПВП Flour White", 
    "Альфа-ПВП Red Bull", "Альфа-ПВП Apple Green",
    "МДМА Кристаллы (Pure)", "МДМА Champagne (Gold)", "МДМА Cola Crystal",
    "Экстази Punisher (300mg)", "Экстази Tesla (Orange)", "Экстази Skype (Blue)", 
    "Экстази Burger King", "Экстази Red Bull (Pink)", "Экстази Philipp Plein", "Экстази WhatsApp",
    "ЛСД-25 250мкг (Aztec)", "ЛСД-25 California Sunshine", "ЛСД-25 Hoffman (200мкг)",
    "Грибы Golden Teacher (Dried)", "Грибы McKennaii", "DMT Crystal (Spirit)", 
    "2C-B Nexus (Pink)", "Кетамин S-isomer (Crystal)", "Кетамин Рацемат",
    "Метадон VHQ (Stone)", "Героин Classic (H-1)", "Ксанакс 2мг (Pfizer Style)", 
    "Лирика 300мг", "Трамадол 200мг"
]

COUNTRIES_DATA = {
    'Россия': [
        'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань', 'Нижний Новгород', 'Челябинск', 'Самара', 'Омск', 'Ростов-на-Дону',
        'Уфа', 'Красноярск', 'Воронеж', 'Пермь', 'Волгоград', 'Краснодар', 'Саратов', 'Тюмень', 'Тольятти', 'Ижевск',
        'Барнаул', 'Ульяновск', 'Иркутск', 'Хабаровск', 'Махачкала', 'Владивосток', 'Ярославль', 'Оренбург', 'Томск', 'Кемерово',
        'Новокузнецк', 'Рязань', 'Набережные Челны', 'Астрахань', 'Пенза', 'Киров', 'Липецк', 'Чебоксары', 'Балашиха', 'Калининград', 'Сочи'
    ],
    'Украина': [
        'Киев', 'Харьков', 'Одесса', 'Днепр', 'Донецк', 'Запорожье', 'Львов', 'Кривой Рог', 'Николаев', 'Мариуполь',
        'Луганск', 'Винница', 'Макеевка', 'Севастополь', 'Симферополь', 'Херсон', 'Полтава', 'Чернигов', 'Черкассы', 'Хмельницкий',
        'Житомир', 'Черновцы', 'Сумы', 'Ровно', 'Ивано-Франковск', 'Каменское', 'Кропивницкий', 'Тернополь', 'Кременчуг', 'Луцк',
        'Белая Церковь', 'Краматорск', 'Мелитополь', 'Керчь', 'Ужгород', 'Бердянск', 'Никополь', 'Славянск', 'Алчевск', 'Павлоград', 'Северодонецк'
    ],
    'Казахстан': [
        'Алматы', 'Астана', 'Шымкент', 'Актобе', 'Караганда', 'Тараз', 'Усть-Каменогорск', 'Павлодар', 'Атырау', 'Семей',
        'Кызылорда', 'Костанай', 'Актау', 'Уральск', 'Петропавловск', 'Туркестан', 'Темиртау', 'Талдыкорган', 'Кокшетау', 'Жанаозен',
        'Экибастуз', 'Рудный', 'Кентау', 'Балхаш', 'Сатпаев', 'Кульсары', 'Жезказган', 'Талгар', 'Каскелен', 'Степногорск',
        'Щучинск', 'Риддер', 'Приозерск', 'Аральск', 'Аягоз', 'Сарань', 'Лисаковск', 'Житикара', 'Шу', 'Аркалык', 'Байконур'
    ],
    'Беларусь': [
        'Минск', 'Гомель', 'Могилев', 'Витебск', 'Гродно', 'Брест', 'Бобруйск', 'Барановичи', 'Борисов', 'Пинск',
        'Орша', 'Мозырь', 'Солигорск', 'Лида', 'Новополоцк', 'Молодечно', 'Полоцк', 'Жлобин', 'Светлогорск', 'Речица',
        'Слуцк', 'Жодино', 'Слоним', 'Кобрин', 'Волковыск', 'Калинковичи', 'Сморгонь', 'Рогачев', 'Горки', 'Осиповичи',
        'Новогрудок', 'Береза', 'Кричев', 'Дзержинск', 'Лунинец', 'Ивацевичи', 'Марьина Горка', 'Поставы', 'Пружаны', 'Глубокое', 'Добруш'
    ]
}

EXCHANGE_RATES = {'KZT': 450.0, 'RUB': 92.0, 'BYN': 3.3, 'UAH': 38.0, 'USD': 1.0}
CURRENCY_MAP = {'Казахстан': 'KZT', 'Россия': 'RUB', 'Беларусь': 'BYN', 'Украина': 'UAH'}

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(API_TOKEN)

# --- БАЗА ДАННЫХ ---
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('shop_v5.db', check_same_thread=False)
        self.create_tables()
        self.init_data()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (uid INTEGER PRIMARY KEY, city TEXT, country TEXT, joined TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)')
        cursor.execute('CREATE TABLE IF NOT EXISTS stock (city TEXT, product_id INTEGER, PRIMARY KEY(city, product_id))')
        cursor.execute('CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, prod TEXT)')
        self.conn.commit()

    def init_data(self):
        cursor = self.conn.cursor()
        if cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            for name in ALL_PRODUCT_NAMES:
                cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, random.randint(40, 110)))
        
        if cursor.execute("SELECT COUNT(*) FROM reviews").fetchone()[0] == 0:
            review_texts = [
    "Забрал в касание", "Курьер молодец", "Место надежное", "Качество на высоте", "Все прошло ровно",
    "Снял очень быстро", "Вес соответствует", "Лучший магазин в городе", "Описание точное", "Клад в тихом месте",
    "Без лишних глаз снял", "Эффект отличный", "Беру не первый раз", "Все как всегда четко", "Наход моментальный",
    "Магазину респект за сервис", "Квест выполнен успешно", "Посылка на месте", "Забежал и ушел", "Стафф свежий",
    "Работают профессионалы", "Доволен покупкой", "Все отлично", "Рекомендую данный шоп", "Клад на магните",
    "Снял в одно касание", "Вес ровный", "Качество радует", "Место подобрано идеально", "Все по описанию",
    "Забрал легко", "Стафф огонь", "Лучший курьер", "Сервис на уровне", "Без нареканий", "Все супер",
    "Нашел быстро", "Подъем легкий", "Клад в лесу но место хорошее", "Все на базе", "Работают ровно",
    "Магазин отличный", "Все понравилось", "Клад надежный", "Описание понятное", "Забрал в лесу",
    "Место очень спокойное", "Снял без проблем", "Качество пушка", "Все на высоте", "Буду брать еще",
    "Стафф улет", "Куре премию", "Вес отличный", "Все ровно как в аптеке", "Лучший стафф здесь",
    "Сервис пушка", "Квест легкий", "Снял за секунду", "Все по красоте", "Магазин топовый",
    "Наход за секунду", "Место тихое", "Все на месте", "Клад качественный", "Стафф лютый",
    "Поднял без проблем", "Все очень круто", "Забрал в касашку", "Место супер", "Все отлично работает",
    "Лучшее предложение в городе", "Все ровно пацаны", "Снял быстро и ушел", "Вес в норме", "Все ок",
    "Качество вышка", "Магаз не подвел", "Все четко сделано", "Наход сто процентов", "Квест изи",
    "Все по делу", "Забрал без лишнего шума", "Место грамотное", "Все на уровне", "Стафф супер гуд",
    "Подъем моментальный", "Все прошло успешно", "Клад надежно спрятан", "Описание огонь", "Забрал быстро",
    "Все супер гуд", "Магазин держит марку", "Качество просто класс", "Нашел место сразу", "Все ровно здесь",
    "Касание 10 из 10", "Кура профи своего дела", "Место беспалевное", "Стафф просто бомба", "Все ровненько",
    "Снял в касание без проблем", "Вес четкий", "Шоп лучший на районе", "Описание четкое", "Клад спрятан надежно",
    "Снял в одно касание и ушел", "Качество лютое", "Постоянно здесь беру", "Все четко как всегда", "Нашел в секунду",
    "Магазу процветания", "Квест изи катка", "Посылочка дома", "Залетел и забрал", "Стафф пушка",
    "Профи работают", "Покупкой доволен на все сто", "Все ровно", "Рекомендую магазин", "Магнит четкий",
    "В касание забрал", "Вес в ажуре", "Качество пушка страшная", "Место идеальное", "Все по красоте сделано",
    "Забрал без проблем", "Стафф вышка", "Курьер лучший", "Сервис топ", "Нареканий нет", "Все огонь",
    "Быстрый наход", "Легкий подъем", "Место тихое и спокойное", "Все на месте пацаны", "Работают четко",
    "Отличный магазин", "Все понравилось", "Надежный клад", "Понятное описание", "Забрал в лесу без проблем",
    "Очень спокойное место", "Проблем со съемом нет", "Пушка стафф", "Все на уровне", "Буду обращаться еще",
    "Улетный стафф", "Курьеру респект", "Вес ровный", "Ровно как в аптеке", "Стафф лучший",
    "Пушка сервис", "Легкий квест", "Снял за миг", "Красиво сделано", "Топовый магаз",
    "Нашел моментально", "Тихое место", "На месте все", "Качественный клад", "Лютый стафф",
    "Поднял легко", "Круто все", "Забрал в касание", "Супер место", "Работает отлично все",
    "Лучшее в городе", "Пацаны все ровно", "Быстро снял и ушел", "Норм вес", "Ок все",
    "Вышка качество", "Не подвел магаз", "Четко сделано все", "Сто процентов наход", "Изи квест",
    "По делу все", "Без шума забрал", "Грамотное место", "Уровень во всем", "Супер гуд стафф",
    "Моментальный подъем", "Успешно все прошло", "Надежно спрятано", "Огонь описание", "Быстро забрал",
    "Супер гуд все", "Марку держат", "Класс качество", "Место сразу нашел", "Здесь все ровно"
          ]
            for i in range(100):
                txt = review_texts[i % len(review_texts)]
                cursor.execute("INSERT INTO reviews (text, prod) VALUES (?,?)", (txt, random.choice(ALL_PRODUCT_NAMES)))
        
        if cursor.execute("SELECT COUNT(*) FROM stock").fetchone()[0] == 0:
            self.shuffle_stock()
        self.conn.commit()

    def shuffle_stock(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM stock")
        p_ids = [r[0] for r in cursor.execute("SELECT id FROM products").fetchall()]
        for country, cities in COUNTRIES_DATA.items():
            for city in cities:
                for pid in random.sample(p_ids, random.randint(7, 10)):
                    cursor.execute("INSERT INTO stock (city, product_id) VALUES (?,?)", (city, pid))
        self.conn.commit()

    def execute(self, query, params=()):
        c = self.conn.cursor(); c.execute(query, params); self.conn.commit()

    def fetchall(self, query, params=()):
        return self.conn.cursor().execute(query, params).fetchall()

    def fetchone(self, query, params=()):
        return self.conn.cursor().execute(query, params).fetchone()

db = Database()

# --- ЛОГИКА ---
def get_main_kb(uid):
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("🌐 Геолокация", callback_data="loc"), types.InlineKeyboardButton("🛒 Shop", callback_data="shop"))
    m.add(types.InlineKeyboardButton("🗨️ Отзывы", callback_data="rev_list_0"), types.InlineKeyboardButton("💼 Работа", callback_data="job"))
    m.add(types.InlineKeyboardButton("📞 Поддержка", url=f"https://t.me/{MANAGER_USERNAME}"), types.InlineKeyboardButton("ℹ️ Информация", url=INFO_CHANNEL))
    if uid == ADMIN_ID:
        m.add(types.InlineKeyboardButton("⚙️ АДМИН ПАНЕЛЬ", callback_data="admin_main"))
    return m

@bot.message_handler(commands=['start'])
def handle_start(m):
    db.execute("INSERT OR IGNORE INTO users (uid, joined) VALUES (?,?)", (m.from_user.id, datetime.now().strftime("%Y-%m-%d")))
    bot.send_photo(m.chat.id, MAIN_IMG, caption=f"👋 Добро пожаловать! <b>{SHOP_NAME}</b>!", reply_markup=get_main_kb(m.from_user.id), parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: True)
def handle_cb(c):
    uid, cid, mid, data = c.from_user.id, c.message.chat.id, c.message.message_id, c.data

    if data == "to_main":
        bot.edit_message_media(types.InputMediaPhoto(MAIN_IMG, caption=f"🏠 Главное меню <b>{SHOP_NAME}</b>", parse_mode="HTML"), cid, mid, reply_markup=get_main_kb(uid))

    elif data == "job":
        job_text = (f"🤝 <b>Стань частью команды {SHOP_NAME}</b>\n\n"
                    f"Хочешь расти вместе с нами? В Magnet всегда рады ответственным коллегам. Твое идеальное место ждет тебя здесь:\n"
                    f"📦 <b>Курьер</b> (высокая оплата, свободный график)\n"
                    f"🏢 <b>Склад</b> (прием и фасовка товара)\n"
                    f"📣 <b>Пиар-менеджер</b> (продвижение бренда)\n"
                    f"🚚 <b>Доставщик</b> (транспортировка между городами)\n\n"
                    f"Твой путь к прибыли начинается здесь. Напиши оператору за деталями!\n\n"
                    f"👉 Связаться с нами: @{MANAGER_USERNAME}")
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📩 Откликнуться", url=f"https://t.me/{MANAGER_USERNAME}"), types.InlineKeyboardButton("🏠 Back", callback_data="to_main"))
        bot.edit_message_media(types.InputMediaPhoto(MAIN_IMG, caption=job_text, parse_mode="HTML"), cid, mid, reply_markup=m)

    elif data.startswith("rev_list_"):
        idx = int(data.split("_")[2])
        revs = db.fetchall("SELECT text, prod FROM reviews")
        idx = idx % len(revs)
        r = revs[idx]
        txt = (f"⭐️ <b>ОТЗЫВЫ (12986 шт.)</b>\n"
               f"📊 Средняя оценка: <b>4.9/5.0</b>\n\n"
               f"👤 Автор: <b>Аноним</b>\n"
               f"📦 Товар: {r[1]}\n"
               f"💬 <i>{r[0]}</i>")
        m = types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton("⬅️ Back", callback_data=f"rev_list_{idx-1}"),
            types.InlineKeyboardButton("Next ➡️", callback_data=f"rev_list_{idx+1}")
        ).add(types.InlineKeyboardButton("🏠 Главная", callback_data="to_main"))
        bot.edit_message_media(types.InputMediaPhoto(MAIN_IMG, caption=txt, parse_mode="HTML"), cid, mid, reply_markup=m)

    elif data == "loc":
        m = types.InlineKeyboardMarkup(row_width=2)
        for country in COUNTRIES_DATA.keys(): m.add(types.InlineKeyboardButton(country, callback_data=f"cnt_{country}_0"))
        m.add(types.InlineKeyboardButton("🏠 Back", callback_data="to_main"))
        bot.edit_message_media(types.InputMediaPhoto(MAIN_IMG, caption="🌍 <b>Выберите страну:</b>", parse_mode="HTML"), cid, mid, reply_markup=m)

    elif data.startswith("cnt_"):
        p = data.split("_")
        cnt = p[1]
        page = int(p[2])
        cities = COUNTRIES_DATA[cnt]
        
        start = page * 10
        end = start + 10
        m = types.InlineKeyboardMarkup(row_width=2)
        for city in cities[start:end]:
            m.add(types.InlineKeyboardButton(city, callback_data=f"set_{city}_{cnt}"))
        
        nav = []
        if page > 0: nav.append(types.InlineKeyboardButton("⬅️ Back", callback_data=f"cnt_{cnt}_{page-1}"))
        if end < len(cities): nav.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"cnt_{cnt}_{page+1}"))
        if nav: m.row(*nav)
        
        m.add(types.InlineKeyboardButton("⬅️ К списку стран", callback_data="loc"))
        bot.edit_message_caption(f"🏙️ <b>Сменить город: {cnt} (стр. {page+1})</b>", cid, mid, reply_markup=m, parse_mode="HTML")

    elif data.startswith("set_"):
        _, city, cnt = data.split("_")
        db.execute("UPDATE users SET city=?, country=? WHERE uid=?", (city, cnt, uid))
        bot.answer_callback_query(c.id, f"📍 Выбран город: {city}")
        bot.edit_message_media(types.InputMediaPhoto(MAIN_IMG, caption=f"📍 Ваш город: <b>{city}</b>", parse_mode="HTML"), cid, mid, reply_markup=get_main_kb(uid))

    elif data == "shop":
        u = db.fetchone("SELECT city, country FROM users WHERE uid=?", (uid,))
        if not u or not u[0]: return bot.answer_callback_query(c.id, "‼️Для начала работы выберите локацию", show_alert=True)
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        prods = db.fetchall("SELECT p.id, p.name, p.price FROM products p JOIN stock s ON p.id = s.product_id WHERE s.city = ?", (u[0],))
        m = types.InlineKeyboardMarkup(row_width=1)
        for pid, name, price in prods:
            m.add(types.InlineKeyboardButton(f"{name} — от {round(price*rate, 1)} {curr}", callback_data=f"buy_{pid}"))
        m.add(types.InlineKeyboardButton("🏠 Back", callback_data="to_main"))
        bot.edit_message_media(types.InputMediaPhoto(MAIN_IMG, caption=f"🛒 <b>Каталог: {u[0]}</b>\nВ наличии {len(prods)} товаров:", parse_mode="HTML"), cid, mid, reply_markup=m)

    elif data.startswith("buy_"):
        pid = data.split("_")[1]
        p = db.fetchone("SELECT name, price FROM products WHERE id=?", (pid,))
        u = db.fetchone("SELECT city, country FROM users WHERE uid=?", (uid,))
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        m = types.InlineKeyboardMarkup(row_width=2)
        for w, mult in [("1г", 1), ("2г", 1.9), ("3г", 2.8), ("5г", 4.2)]:
            p_val = round(p[1]*mult*rate, 1)
            m.add(types.InlineKeyboardButton(f"{w} - {p_val} {curr}", callback_data=f"bank_{pid}_{w}_{p_val}"))
        m.add(types.InlineKeyboardButton("⬅️ К каталогу", callback_data="shop"))
        bot.edit_message_caption(f"💎 <b>{p[0]}</b>\nВыберите количество:", cid, mid, reply_markup=m, parse_mode="HTML")

    elif data.startswith("bank_"):
        _, pid, w, price = data.split("_")
        u = db.fetchone("SELECT country FROM users WHERE uid=?", (uid,))
        m = types.InlineKeyboardMarkup(row_width=2)
        country_banks = BANKS.get(u[0], ['Крипта', 'Карта'])
        for b_name in country_banks:
            m.add(types.InlineKeyboardButton(b_name, callback_data=f"pay_{pid}_{w}_{price}_{b_name}"))
        m.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"buy_{pid}"))
        bot.edit_message_caption(f"🏦 <b>Выбор способа оплаты({u[0]}):</b>", cid, mid, reply_markup=m, parse_mode="HTML")

    elif data.startswith("pay_"):
        _, pid, w, price, bank = data.split("_")
        p = db.fetchone("SELECT name FROM products WHERE id=?", (pid,))
        u = db.fetchone("SELECT city, country FROM users WHERE uid=?", (uid,))
        curr = CURRENCY_MAP.get(u[1], 'USD')
        order_id = str(uuid.uuid4())[:8].upper()
        
        check = (f"🧾 <b>ВАШ ЗАКАЗ #{order_id}</b>\n"
                 f"━━━━━━━━━━━━━━\n"
                 f"📍 Город: <b>{u[0]}</b>\n"
                 f"📦 Товар: <b>{p[0]}</b>\n"
                 f"⚖️ Вес: <b>{w}</b>\n"
                 f"🏦 Тип оплаты: <b>{bank}</b>\n"
                 f"💰 Сумма: <b>{price} {curr}</b>\n"
                 f"━━━━━━━━━━━━━━\n"
                 f"⚠️ <b>ИНСТРУКЦИЯ:</b>\n"
                 f"Чтобы получить реквизиты, перешлите данный чек в чат с оператором.\n\n"
                 f"👉 Оператор: @{MANAGER_USERNAME}")
        
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏠 На главную", callback_data="to_main"))
        bot.edit_message_caption(check, cid, mid, reply_markup=m, parse_mode="HTML")

    # --- АДМИНКА ---
    elif data == "admin_main" and uid == ADMIN_ID:
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(types.InlineKeyboardButton("📝 РЕДАКТИРОВАТЬ ТОВАРЫ", callback_data="adm_list_0"),
              types.InlineKeyboardButton("🔄 ОБНОВИТЬ ВСЕ ВИТРИНЫ (RANDOM)", callback_data="adm_shuffle"),
              types.InlineKeyboardButton("🏠 Выйти", callback_data="to_main"))
        bot.edit_message_caption("⚙️ <b>ПАНЕЛЬ УПРАВЛЕНИЯ</b>\nЗдесь вы можете управлять ассортиментом и глобальными настройками.", cid, mid, reply_markup=m, parse_mode="HTML")

    elif data == "adm_shuffle" and uid == ADMIN_ID:
        db.shuffle_stock()
        bot.answer_callback_query(c.id, "✅ Витрины во всех городах успешно обновлены!", show_alert=True)

    elif data.startswith("adm_list_"):
        page = int(data.split("_")[2])
        prods = db.fetchall("SELECT id, name, price FROM products")
        start = page * 10
        end = start + 10
        m = types.InlineKeyboardMarkup(row_width=2)
        for pid, name, price in prods[start:end]:
            m.add(types.InlineKeyboardButton(f"{name}", callback_data=f"adm_edit_{pid}"))
        
        nav = []
        if page > 0: nav.append(types.InlineKeyboardButton("⬅️", callback_data=f"adm_list_{page-1}"))
        if end < len(prods): nav.append(types.InlineKeyboardButton("➡️", callback_data=f"adm_list_{page+1}"))
        if nav: m.row(*nav)
        m.add(types.InlineKeyboardButton("🏠 Back", callback_data="admin_main"))
        bot.edit_message_caption(f"Выберите товар для редактирования (стр. {page+1}):", cid, mid, reply_markup=m)

    elif data.startswith("adm_edit_"):
        pid = data.split("_")[2]
        p = db.fetchone("SELECT name, price FROM products WHERE id=?", (pid,))
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(types.InlineKeyboardButton("✏️ Сменить название", callback_data=f"edt_name_{pid}"),
              types.InlineKeyboardButton("💰 Сменить цену", callback_data=f"edt_prc_{pid}"),
              types.InlineKeyboardButton("⬅️ К списку", callback_data="adm_list_0"))
        bot.edit_message_caption(f"<b>Редактирование товара</b>\n\nID: {pid}\nНазвание: <b>{p[0]}</b>\nБазовая цена: <b>{p[1]}$</b>", cid, mid, reply_markup=m, parse_mode="HTML")

    elif data.startswith("edt_name_"):
        pid = data.split("_")[2]
        msg = bot.send_message(cid, "Введите НОВОЕ НАЗВАНИЕ для товара:")
        bot.register_next_step_handler(msg, update_name_step, pid)

    elif data.startswith("edt_prc_"):
        pid = data.split("_")[2]
        msg = bot.send_message(cid, "Введите НОВУЮ ЦЕНУ ($) за 1г:")
        bot.register_next_step_handler(msg, update_price_step, pid)

def update_name_step(m, pid):
    if not m.text: return
    db.execute("UPDATE products SET name=? WHERE id=?", (m.text, pid))
    bot.send_message(m.chat.id, f"✅ Название товара #{pid} изменено на: {m.text}")

def update_price_step(m, pid):
    try:
        new_p = float(m.text)
        db.execute("UPDATE products SET price=? WHERE id=?", (new_p, pid))
        bot.send_message(m.chat.id, f"✅ Цена товара #{pid} обновлена: {new_p}$")
    except:
        bot.send_message(m.chat.id, "❌ Ошибка. Введите числовое значение.")

if __name__ == "__main__":
    bot.polling(none_stop=True)