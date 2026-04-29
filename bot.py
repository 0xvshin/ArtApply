import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, CallbackQueryHandler, ConversationHandler
)

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 7720697188

# ==================== مراحل فرم ====================
(
    F_NAME, F_TELEGRAM, F_EMAIL, F_BIRTH, F_DEGREE, F_FIELD,
    F_UNIVERSITY, F_STATUS, F_GRAD_YEAR, F_REMAINING, F_GPA,
    F_TARGET_DEGREE, F_TARGET_FIELD, F_COUNTRIES, F_PAPERS,
    F_EXHIBITIONS, F_LANG_STATUS, F_LANG_SCORE, F_APPLY_KNOW,
    F_PORTFOLIO_LEVEL, F_OTHER, F_FILES, F_CONFIRM
) = range(23)

# ==================== منوها ====================

main_menu = ReplyKeyboardMarkup([
    ["📦 بسته‌های اپلای", "✅ ارزیابی رایگان"],
    ["📋 تهیه مدارک اپلای", "🧳 مشاوره اپلای"],
    ["📞 ارتباط با پشتیبانی", "🏆 پرونده‌های موفق"]
], resize_keyboard=True)

packages_menu = ReplyKeyboardMarkup([
    ["🎓 بسته کارشناسی", "🎓 بسته کارشناسی ارشد"],
    ["🎓 بسته دکتری", "🧑‍🏫 بسته منتورینگ"],
    ["↩️ بازگشت به منوی اصلی"]
], resize_keyboard=True)

cancel_menu = ReplyKeyboardMarkup([["❌ انصراف از فرم"]], resize_keyboard=True)

# ==================== سوالات متداول ====================

def faq_karshenas_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("این بسته شامل چه مواردی است؟", callback_data="k_1")],
        [InlineKeyboardButton("برای چه کشورهایی اقدام می‌شود؟", callback_data="k_2")],
        [InlineKeyboardButton("آیا دریافت پذیرش تضمینی است؟", callback_data="k_3")],
        [InlineKeyboardButton("آیا بدون مدرک زبان امکان اپلای وجود دارد؟", callback_data="k_4")],
        [InlineKeyboardButton("آیا امکان دریافت فاند وجود دارد؟", callback_data="k_5")],
        [InlineKeyboardButton("اپلای را چه کسانی انجام می‌دهند؟", callback_data="k_6")],
        [InlineKeyboardButton("قیمت بسته چقدر است؟", callback_data="k_7")],
        [InlineKeyboardButton("آیا امکان پرداخت اقساطی وجود دارد؟", callback_data="k_8")],
        [InlineKeyboardButton("آیا از پیشرفت پرونده خبردار می‌شویم؟", callback_data="k_9")],
        [InlineKeyboardButton("چگونه می‌توانم شروع کنم؟", callback_data="k_10")],
    ])

def faq_arshad_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("این بسته شامل چه مواردی است؟", callback_data="a_1")],
        [InlineKeyboardButton("برای چه کشورهایی اقدام می‌شود؟", callback_data="a_2")],
        [InlineKeyboardButton("آیا دریافت پذیرش تضمینی است؟", callback_data="a_3")],
        [InlineKeyboardButton("آیا بدون مدرک زبان امکان اپلای وجود دارد؟", callback_data="a_4")],
        [InlineKeyboardButton("آیا امکان دریافت فاند وجود دارد؟", callback_data="a_5")],
        [InlineKeyboardButton("اپلای را چه کسانی انجام می‌دهند؟", callback_data="a_6")],
        [InlineKeyboardButton("قیمت بسته چقدر است؟", callback_data="a_7")],
        [InlineKeyboardButton("آیا امکان پرداخت اقساطی وجود دارد؟", callback_data="a_8")],
        [InlineKeyboardButton("آیا از پیشرفت پرونده خبردار می‌شویم؟", callback_data="a_9")],
        [InlineKeyboardButton("چگونه می‌توانم شروع کنم؟", callback_data="a_10")],
    ])

def faq_doktori_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("برای چه کشورهایی اقدام می‌شود؟", callback_data="d_1")],
        [InlineKeyboardButton("این بسته شامل چه مواردی است؟", callback_data="d_2")],
        [InlineKeyboardButton("آیا دریافت پذیرش تضمینی است؟", callback_data="d_3")],
        [InlineKeyboardButton("آیا امکان دریافت فاند وجود دارد؟", callback_data="d_4")],
        [InlineKeyboardButton("اپلای را چه کسانی انجام می‌دهند؟", callback_data="d_5")],
        [InlineKeyboardButton("قیمت بسته چقدر است؟", callback_data="d_6")],
        [InlineKeyboardButton("آیا امکان پرداخت اقساطی وجود دارد؟", callback_data="d_7")],
        [InlineKeyboardButton("آیا از پیشرفت پرونده خبردار می‌شویم؟", callback_data="d_8")],
        [InlineKeyboardButton("چگونه می‌توانم شروع کنم؟", callback_data="d_9")],
    ])

def faq_mentoring_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بسته منتورینگ اپلای چیست؟", callback_data="m_1")],
        [InlineKeyboardButton("آیا دریافت پذیرش و فاند تضمینی است؟", callback_data="m_2")],
        [InlineKeyboardButton("خدمات منتورینگ شامل چه جزئیاتی است؟", callback_data="m_3")],
        [InlineKeyboardButton("هزینه بسته منتورینگ چقدر است؟", callback_data="m_4")],
        [InlineKeyboardButton("نحوه پرداخت هزینه به چه صورت است؟", callback_data="m_5")],
        [InlineKeyboardButton("چگونه ثبت سفارش کنم؟", callback_data="m_6")],
    ])

def faq_madarek_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("برای ثبت سفارش چه کار باید انجام دهیم؟", callback_data="md_1")],
        [InlineKeyboardButton("مدت زمان آماده‌سازی مدارک چقدر است؟", callback_data="md_2")],
        [InlineKeyboardButton("نحوه پرداخت به چه صورت است؟", callback_data="md_3")],
        [InlineKeyboardButton("نحوه ارسال مدرک آماده به چه صورت است؟", callback_data="md_4")],
        [InlineKeyboardButton("در صورت عدم رضایت از فایل چه راه حلی وجود دارد؟", callback_data="md_5")],
        [InlineKeyboardButton("مدرک توسط چه کسانی آماده می‌شود؟", callback_data="md_6")],
    ])

def faq_consulting_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("جلسه مشاوره چگونه برگزار می‌شود؟", callback_data="c_1")],
        [InlineKeyboardButton("زمان جلسه چقدر است؟", callback_data="c_2")],
        [InlineKeyboardButton("در جلسه در مورد چه موضوعاتی صحبت می‌شود؟", callback_data="c_3")],
    ])

back_keyboards = {
    "k": faq_karshenas_keyboard, "a": faq_arshad_keyboard,
    "d": faq_doktori_keyboard, "m": faq_mentoring_keyboard,
    "md": faq_madarek_keyboard, "c": faq_consulting_keyboard,
}

# ==================== پاسخ‌ها ====================

answers = {
    "k_1": "این بسته شامل خدمات بسیاری است، از جمله: مشاوره دقیق، پشتیبانی و گزارش لحظه‌ای تمام امور پرونده؛ آماده‌سازی مدارک شامل نگارش رزومه، نگارش انگیزه‌نامه، طراحی پورتفولیو، نگارش متن توصیه‌نامه، مکاتبات، تهیه فهرست کامل دانشگاه‌ها، تکمیل فرم‌های مربوط و سابمیت اپلیکیشن‌ها، اقدام برای بورسیه‌های موجود و غیره.",
    "k_2": "آرت اپلای به صورت حرفه‌ای برای اکثر کشورهای دنیا امکان اقدام دارد. بسته به درخواست متقاضی و نظر کارشناس، اپلای صورت می‌گیرد.",
    "k_3": "در صورت ارائه مدارک کامل توسط متقاضی، امکان دریافت پذیرش بسیار بالاست. آمار پذیرش آرت اپلای از شروع فعالیت مجموعه از سال 2017 تاکنون، صد در صد بوده است.",
    "k_4": "در برخی کشورها بله این امکان وجود دارد، اما به صورت کلی پیشنهاد می‌شود با مدارک کامل اقدام به اپلای کنید. تیم آرت اپلای اکثر مدارک اپلای شما را آماده خواهد کرد.",
    "k_5": "ما تمام تلاش خود را برای دریافت بورسیه‌های تحصیلی انجام می‌دهیم، اما تضمین صد در صدی برای فاند در این مقطع و در برخی از کشورها ممکن نیست.",
    "k_6": "بسته‌های صفر تا صد اپلای توسط فارغ‌التحصیلان رشته هنر در خارج از کشور انجام می‌شود. تمامی کارشناسان ما دارای مدرک دکتری از بهترین دانشگاه‌های دنیا هستند و به روند کامل اپلای تسلط دارند.",
    "k_7": "بسته به کشور یا کشورهای مدنظر متغیر است. پایین‌ترین نرخ برای قبرس رایگان و بالاترین نرخ برای کانادا 2600 یورو است. برای استعلام نرخ دقیق با پشتیبان آرت اپلای در تماس باشید.",
    "k_8": "بله! نه‌تنها امکان پرداخت اقساطی وجود دارد، بلکه نیمی از هزینه قرارداد پس از اخذ پذیرش دریافت می‌شود.",
    "k_9": "بله! به محض شروع کار با آرت اپلای، شما وارد گروهی متشکل از پشتیبان آرت اپلای، کارشناس ارتباط با متقاضی و سوپروایزر اپلای خواهید شد.",
    "k_10": "برای ثبت سفارش کافی است به پشتیبان آرت اپلای پیام دهید:\n👤 @ArtApplyContact",
    "a_1": "این بسته شامل خدمات بسیاری است، از جمله: مشاوره دقیق، پشتیبانی و گزارش لحظه‌ای تمام امور پرونده؛ آماده‌سازی مدارک شامل نگارش رزومه، نگارش انگیزه‌نامه، طراحی پورتفولیو، نگارش متن توصیه‌نامه، مکاتبات، تهیه فهرست کامل دانشگاه‌ها، تکمیل فرم‌های مربوط و سابمیت اپلیکیشن‌ها، اقدام برای بورسیه‌های موجود و غیره.",
    "a_2": "آرت اپلای به صورت حرفه‌ای برای اکثر کشورهای دنیا امکان اقدام دارد. بسته به درخواست متقاضی و نظر کارشناس، اپلای صورت می‌گیرد.",
    "a_3": "در صورت ارائه مدارک کامل توسط متقاضی (نمره زبان مدنظر دانشگاه، پورتفولیوی مناسب و غیره)، امکان دریافت پذیرش بسیار بالاست. آمار پذیرش آرت اپلای از سال 2017 تاکنون نزدیک به صد در صد بوده است.",
    "a_4": "در برخی کشورها بله این امکان وجود دارد، اما به صورت کلی پیشنهاد می‌شود با مدارک کامل اقدام به اپلای کنید.",
    "a_5": "ما تمام تلاش خود را برای دریافت بورسیه‌های تحصیلی انجام می‌دهیم، اما تضمین صد در صدی برای فاند در برخی از کشورها ممکن نیست.",
    "a_6": "بسته‌های صفر تا صد اپلای توسط فارغ‌التحصیلان رشته هنر در خارج از کشور انجام می‌شود. تمامی کارشناسان ما دارای مدرک دکتری از بهترین دانشگاه‌های دنیا هستند.",
    "a_7": "بسته به کشور یا کشورهای مدنظر متغیر است. پایین‌ترین نرخ برای قبرس رایگان و بالاترین نرخ برای کانادا 3600 یورو است.",
    "a_8": "بله! نه‌تنها امکان پرداخت اقساطی وجود دارد، بلکه بیش از دو سوم از هزینه قرارداد پس از اخذ پذیرش و بورسیه دریافت می‌شود.",
    "a_9": "بله! به محض شروع کار با آرت اپلای، شما وارد گروهی متشکل از پشتیبان، کارشناس و سوپروایزر اپلای خواهید شد.",
    "a_10": "برای ثبت سفارش کافی است به پشتیبان آرت اپلای پیام دهید:\n👤 @ArtApplyContact",
    "d_1": "آرت اپلای به صورت حرفه‌ای برای اکثر کشورهای دنیا امکان اقدام دارد. بسته به درخواست متقاضی و نظر کارشناس، اپلای صورت می‌گیرد.",
    "d_2": "این بسته شامل: مشاوره دقیق، پشتیبانی و گزارش لحظه‌ای تمام امور پرونده؛ آماده‌سازی مدارک شامل نگارش رزومه، انگیزه‌نامه، پورتفولیو، توصیه‌نامه، مکاتبات، تهیه فهرست دانشگاه‌ها، تکمیل فرم‌ها، سابمیت اپلیکیشن‌ها و اقدام برای بورسیه‌های موجود.",
    "d_3": "اپلای دکتری بسیار رقابتی است. امکان اخذ پذیرش در صورتی که متقاضی رزومه قوی داشته باشد و پروپزال خوبی ارائه دهد، بسیار بالاست.",
    "d_4": "بله، در بسیاری از موقعیت‌های دکتری فاند وجود دارد و در صورت اخذ پذیرش، امکان و احتمال دریافت فاند بالاست.",
    "d_5": "بسته‌های صفر تا صد اپلای توسط فارغ‌التحصیلان رشته هنر در خارج از کشور انجام می‌شود. تمامی کارشناسان ما دارای مدرک دکتری از بهترین دانشگاه‌های دنیا هستند.",
    "d_6": "این بسته نسبت به شرایط متغیر است. بازه هزینه بین 2400 تا 3600 یورو است. برای استعلام نرخ دقیق با پشتیبان آرت اپلای در تماس باشید.",
    "d_7": "بله! نه‌تنها امکان پرداخت اقساطی وجود دارد، بلکه بیش از یک سوم از هزینه قرارداد پس از اخذ پذیرش و بورسیه دریافت می‌شود.",
    "d_8": "بله! به محض شروع کار با آرت اپلای، شما وارد گروهی متشکل از پشتیبان، کارشناس و سوپروایزر اپلای خواهید شد.",
    "d_9": "برای ثبت سفارش کافی است به پشتیبان آرت اپلای پیام دهید:\n👤 @ArtApplyContact",
    "m_1": "منتورینگ اپلای یعنی همراهی یک فرد باتجربه (موسس و مدیر آرت اپلای) در کل مسیر اپلای، از انتخاب رشته و دانشگاه تا آماده‌سازی مدارک، مکاتبات، ارسال درخواست، پیگیری بورسیه‌های تحصیلی و پروسه ویزا.",
    "m_2": "این بسته آموزشی و پشتیبانی است و تضمین صددرصدی برای پذیرش یا فاند ندارد، اما با ترکیب دانش تخصصی منتور و عملکرد متقاضی، موفقیت شما را تضمین می‌کند. تاکنون بیش از 90 درصد پرونده‌های منتورینگ موفق بوده‌اند.",
    "m_3": "مشاوره اولیه، ارائه نقشه راه، عضویت در کانال اختصاصی منتورینگ، دسترسی به ساعت‌ها ویدیوی آموزشی، ارتباط مستقیم با منتور در تمام پروسه اپلای، جلسات مشاوره، بررسی و آماده‌سازی قدم به قدم مدارک، تهیه لیست کامل دانشگاه‌ها، مکاتبات، فرایند تکمیل اپلیکیشن‌ها، پیگیری نتایج، اپلای برای بورسیه‌ها، امور مرتبط با ویزا و خدمات پس از اخذ ویزا.",
    "m_4": "هزینه این بسته 1200 یورو است. در صورت پرداخت از طریق ارزهای دیجیتال، 10 درصد تخفیف اعمال می‌شود.",
    "m_5": "پرداخت به صورت اقساطی در سه قسط:\n\nقسط اول (600 یورو) هنگام شروع دوره\nقسط دوم (300 یورو) پس از چهل روز\nقسط سوم (300 یورو) پس از اخذ نخستین پذیرش.",
    "m_6": "برای ثبت سفارش کافی است به پشتیبان آرت اپلای پیام دهید:\n👤 @ArtApplyContact",
    "md_1": "کافی است به پشتیبان آرت اپلای پیام داده و مدارک مورد نظرتان را به ما اطلاع دهید:\n👤 @ArtApplyContact",
    "md_2": "بسته به نوع مدرک انتخابی، زمان تحویل بین 3 تا 21 روز کاری است.",
    "md_3": "در برخی مدارک پرداخت یکجا در ابتدا خواهد بود. برای پورتفولیو، پروپزال و وبسایت پرداخت در دو قسط انجام می‌شود.",
    "md_4": "مدارک نهایی به صورت فایل ورد و پی‌دی‌اف از طریق ایمیل یا تلگرام برای شما ارسال خواهند شد.",
    "md_5": "شما می‌توانید از مهلت ویرایش رایگان خود استفاده کرده و تمامی نظرات و درخواست‌های اصلاحی خود را به کارشناس مربوطه ارسال کنید.",
    "md_6": "مدارک شما توسط کارشناسانی تهیه می‌شود که خود تجربه موفق اپلای و تحصیل در بهترین دانشگاه‌های دنیا را دارند.",
    "c_1": "پس از رزرو وقت مشاوره، اطلاعات مربوط به جلسه از طریق ایمیل و پیامک برای شما ارسال خواهد شد.",
    "c_2": "جلسه مشاوره 40 دقیقه است و طی این مدت کارشناس به بررسی شرایط شما و پیشنهاد بهترین مسیر مهاجرتی خواهد پرداخت.",
    "c_3": "در جلسه مشاوره، کارشناس پس از بررسی شرایط شما نقشه راه کاملی از برنامه‌های اپلای ارائه می‌دهد و تمامی سوالات شما پاسخ داده خواهد شد.",
}

question_titles = {
    "k_1": "این بسته شامل چه مواردی است؟", "k_2": "برای چه کشورهایی اقدام می‌شود؟",
    "k_3": "آیا دریافت پذیرش تضمینی است؟", "k_4": "آیا بدون مدرک زبان امکان اپلای وجود دارد؟",
    "k_5": "آیا امکان دریافت فاند وجود دارد؟", "k_6": "اپلای را چه کسانی انجام می‌دهند؟",
    "k_7": "قیمت بسته چقدر است؟", "k_8": "آیا امکان پرداخت اقساطی وجود دارد؟",
    "k_9": "آیا از پیشرفت پرونده خبردار می‌شویم؟", "k_10": "چگونه می‌توانم شروع کنم؟",
    "a_1": "این بسته شامل چه مواردی است؟", "a_2": "برای چه کشورهایی اقدام می‌شود؟",
    "a_3": "آیا دریافت پذیرش تضمینی است؟", "a_4": "آیا بدون مدرک زبان امکان اپلای وجود دارد؟",
    "a_5": "آیا امکان دریافت فاند وجود دارد؟", "a_6": "اپلای را چه کسانی انجام می‌دهند؟",
    "a_7": "قیمت بسته چقدر است؟", "a_8": "آیا امکان پرداخت اقساطی وجود دارد؟",
    "a_9": "آیا از پیشرفت پرونده خبردار می‌شویم؟", "a_10": "چگونه می‌توانم شروع کنم؟",
    "d_1": "برای چه کشورهایی اقدام می‌شود؟", "d_2": "این بسته شامل چه مواردی است؟",
    "d_3": "آیا دریافت پذیرش تضمینی است؟", "d_4": "آیا امکان دریافت فاند وجود دارد؟",
    "d_5": "اپلای را چه کسانی انجام می‌دهند؟", "d_6": "قیمت بسته چقدر است؟",
    "d_7": "آیا امکان پرداخت اقساطی وجود دارد؟", "d_8": "آیا از پیشرفت پرونده خبردار می‌شویم؟",
    "d_9": "چگونه می‌توانم شروع کنم؟",
    "m_1": "بسته منتورینگ اپلای چیست؟", "m_2": "آیا دریافت پذیرش و فاند تضمینی است؟",
    "m_3": "خدمات منتورینگ شامل چه جزئیاتی است؟", "m_4": "هزینه بسته منتورینگ چقدر است؟",
    "m_5": "نحوه پرداخت هزینه به چه صورت است؟", "m_6": "چگونه ثبت سفارش کنم؟",
    "md_1": "برای ثبت سفارش چه کار باید انجام دهیم؟", "md_2": "مدت زمان آماده‌سازی مدارک چقدر است؟",
    "md_3": "نحوه پرداخت به چه صورت است؟", "md_4": "نحوه ارسال مدرک آماده به چه صورت است؟",
    "md_5": "در صورت عدم رضایت از فایل چه راه حلی وجود دارد؟", "md_6": "مدرک توسط چه کسانی آماده می‌شود؟",
    "c_1": "جلسه مشاوره چگونه برگزار می‌شود؟", "c_2": "زمان جلسه چقدر است؟",
    "c_3": "در جلسه در مورد چه موضوعاتی صحبت می‌شود؟",
}

# ==================== فرم ارزیابی ====================

async def form_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data['files'] = []
    await update.message.reply_text(
        "📋 *فرم ارزیابی رایگان آرت اپلای*\n\n"
        "لطفاً به سوالات زیر پاسخ دهید.\n"
        "در هر مرحله می‌توانید ❌ انصراف از فرم را بزنید.\n\n"
        "━━━━━━━━━━━━━━━\n"
        "1️⃣ نام و نام خانوادگی:",
        reply_markup=cancel_menu,
        parse_mode="Markdown"
    )
    return F_NAME

async def f_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['name'] = update.message.text
    await update.message.reply_text("2️⃣ آیدی یا شماره تلگرام:")
    return F_TELEGRAM

async def f_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['telegram'] = update.message.text
    await update.message.reply_text("3️⃣ ایمیل:")
    return F_EMAIL

async def f_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['email'] = update.message.text
    await update.message.reply_text("4️⃣ سال تولد:")
    return F_BIRTH

async def f_birth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['birth'] = update.message.text
    await update.message.reply_text("5️⃣ آخرین مقطع تحصیلی:\n(مثال: کارشناسی، کارشناسی ارشد، دکتری)")
    return F_DEGREE

async def f_degree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['degree'] = update.message.text
    await update.message.reply_text("6️⃣ رشته تحصیلی:")
    return F_FIELD

async def f_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['field'] = update.message.text
    await update.message.reply_text("7️⃣ دانشگاه محل تحصیل:")
    return F_UNIVERSITY

async def f_university(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['university'] = update.message.text
    keyboard = ReplyKeyboardMarkup(
        [["در حال تحصیل", "فارغ التحصیل"], ["❌ انصراف از فرم"]],
        resize_keyboard=True
    )
    await update.message.reply_text("8️⃣ وضعیت تحصیلی:", reply_markup=keyboard)
    return F_STATUS

async def f_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['status'] = update.message.text
    if update.message.text == "فارغ التحصیل":
        await update.message.reply_text("9️⃣ سال اتمام تحصیل:", reply_markup=cancel_menu)
        return F_GRAD_YEAR
    else:
        context.user_data['grad_year'] = "-"
        await update.message.reply_text("9️⃣ چند ترم تا پایان تحصیل باقی مانده؟", reply_markup=cancel_menu)
        return F_REMAINING

async def f_grad_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['grad_year'] = update.message.text
    context.user_data['remaining'] = "-"
    await update.message.reply_text("🔟 معدل آخرین مقطع تحصیلی:")
    return F_GPA

async def f_remaining(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['remaining'] = update.message.text
    await update.message.reply_text("🔟 معدل آخرین مقطع تحصیلی:")
    return F_GPA

async def f_gpa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['gpa'] = update.message.text
    keyboard = ReplyKeyboardMarkup(
        [["کارشناسی", "کارشناسی ارشد", "دکتری"], ["❌ انصراف از فرم"]],
        resize_keyboard=True
    )
    await update.message.reply_text("1️⃣1️⃣ مقطع مدنظر برای اپلای:", reply_markup=keyboard)
    return F_TARGET_DEGREE

async def f_target_degree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['target_degree'] = update.message.text
    await update.message.reply_text("1️⃣2️⃣ رشته مدنظر برای اپلای:", reply_markup=cancel_menu)
    return F_TARGET_FIELD

async def f_target_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['target_field'] = update.message.text
    await update.message.reply_text("1️⃣3️⃣ کشور یا کشورهای مدنظر:")
    return F_COUNTRIES

async def f_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['countries'] = update.message.text
    await update.message.reply_text("1️⃣4️⃣ تعداد مقالات منتشر شده:\n(اگر ندارید عدد 0 بنویسید)")
    return F_PAPERS

async def f_papers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['papers'] = update.message.text
    await update.message.reply_text("1️⃣5️⃣ تعداد نمایشگاه‌ها:\n(اگر ندارید عدد 0 بنویسید)")
    return F_EXHIBITIONS

async def f_exhibitions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['exhibitions'] = update.message.text
    keyboard = ReplyKeyboardMarkup(
        [["دارم", "ندارم"], ["❌ انصراف از فرم"]],
        resize_keyboard=True
    )
    await update.message.reply_text("1️⃣6️⃣ مدرک زبان:", reply_markup=keyboard)
    return F_LANG_STATUS

async def f_lang_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['lang_status'] = update.message.text
    if update.message.text == "دارم":
        await update.message.reply_text("1️⃣7️⃣ نمره یا سطح زبان:", reply_markup=cancel_menu)
    else:
        context.user_data['lang_score'] = "-"
        keyboard = ReplyKeyboardMarkup(
            [["هیچ", "تا حدودی", "خیلی"], ["❌ انصراف از فرم"]],
            resize_keyboard=True
        )
        await update.message.reply_text("1️⃣8️⃣ آشنایی با پروسه اپلای:", reply_markup=keyboard)
        return F_APPLY_KNOW
    return F_LANG_SCORE

async def f_lang_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['lang_score'] = update.message.text
    keyboard = ReplyKeyboardMarkup(
        [["هیچ", "تا حدودی", "خیلی"], ["❌ انصراف از فرم"]],
        resize_keyboard=True
    )
    await update.message.reply_text("1️⃣8️⃣ آشنایی با پروسه اپلای:", reply_markup=keyboard)
    return F_APPLY_KNOW

async def f_apply_know(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['apply_know'] = update.message.text
    keyboard = ReplyKeyboardMarkup(
        [["معمولی", "خوب", "مورد تایید اساتید"], ["❌ انصراف از فرم"]],
        resize_keyboard=True
    )
    await update.message.reply_text("1️⃣9️⃣ سطح نمونه آثار:", reply_markup=keyboard)
    return F_PORTFOLIO_LEVEL

async def f_portfolio_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['portfolio_level'] = update.message.text
    await update.message.reply_text(
        "2️⃣0️⃣ سایر اطلاعات:\n(هر چیز دیگری که فکر می‌کنید مفید است بنویسید، یا بنویسید ندارم)",
        reply_markup=cancel_menu
    )
    return F_OTHER

async def f_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)
    context.user_data['other'] = update.message.text
    keyboard = ReplyKeyboardMarkup(
        [["رد کردن و ارسال فرم ✅"], ["❌ انصراف از فرم"]],
        resize_keyboard=True
    )
    await update.message.reply_text(
        "2️⃣1️⃣ *ارسال فایل (اختیاری)*\n\n"
        "اگر رزومه، پورتفولیو یا هر فایل دیگری دارید همین الان ارسال کنید.\n"
        "می‌توانید چند فایل ارسال کنید.\n\n"
        "وقتی تمام شد روی *رد کردن و ارسال فرم* کلیک کنید.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    return F_FILES

async def f_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "❌ انصراف از فرم":
        return await form_cancel(update, context)

    if update.message.text == "رد کردن و ارسال فرم ✅":
        return await f_confirm(update, context)

    # ذخیره فایل
    file_id = None
    file_type = None
    if update.message.document:
        file_id = update.message.document.file_id
        file_type = "document"
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_type = "photo"

    if file_id:
        context.user_data['files'].append({'id': file_id, 'type': file_type})
        await update.message.reply_text(
            f"✅ فایل دریافت شد! ({len(context.user_data['files'])} فایل)\nفایل دیگری ارسال کنید یا روی دکمه کلیک کنید."
        )
    return F_FILES

async def f_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = context.user_data
    user = update.effective_user

    summary = (
        f"📋 *فرم ارزیابی جدید*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 *نام:* {d.get('name', '-')}\n"
        f"📱 *تلگرام:* {d.get('telegram', '-')}\n"
        f"📧 *ایمیل:* {d.get('email', '-')}\n"
        f"🎂 *سال تولد:* {d.get('birth', '-')}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎓 *آخرین مقطع:* {d.get('degree', '-')}\n"
        f"📚 *رشته:* {d.get('field', '-')}\n"
        f"🏫 *دانشگاه:* {d.get('university', '-')}\n"
        f"📊 *وضعیت:* {d.get('status', '-')}\n"
        f"📅 *سال اتمام:* {d.get('grad_year', '-')}\n"
        f"⏳ *ترم‌های باقیمانده:* {d.get('remaining', '-')}\n"
        f"📈 *معدل:* {d.get('gpa', '-')}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎯 *مقطع مدنظر:* {d.get('target_degree', '-')}\n"
        f"🖌 *رشته مدنظر:* {d.get('target_field', '-')}\n"
        f"🌍 *کشورهای مدنظر:* {d.get('countries', '-')}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📄 *مقالات:* {d.get('papers', '-')}\n"
        f"🖼 *نمایشگاه‌ها:* {d.get('exhibitions', '-')}\n"
        f"🗣 *مدرک زبان:* {d.get('lang_status', '-')}\n"
        f"📝 *نمره زبان:* {d.get('lang_score', '-')}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🧠 *آشنایی با اپلای:* {d.get('apply_know', '-')}\n"
        f"🎨 *سطح نمونه آثار:* {d.get('portfolio_level', '-')}\n"
        f"💬 *سایر اطلاعات:* {d.get('other', '-')}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📎 *تعداد فایل‌های ارسالی:* {len(d.get('files', []))}\n"
        f"🔗 *یوزرنیم تلگرام:* @{user.username if user.username else 'ندارد'}"
    )

    # ارسال فرم به ادمین
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=summary,
        parse_mode="Markdown"
    )

    # ارسال فایل‌ها به ادمین
    for f in d.get('files', []):
        try:
            if f['type'] == "document":
                await context.bot.send_document(chat_id=ADMIN_ID, document=f['id'])
            elif f['type'] == "photo":
                await context.bot.send_photo(chat_id=ADMIN_ID, photo=f['id'])
        except Exception:
            pass

    await update.message.reply_text(
        "✅ *فرم شما با موفقیت ارسال شد!*\n\n"
        "کارشناسان آرت اپلای به زودی با شما تماس خواهند گرفت.\n\n"
        "👤 برای پیگیری: @ArtApplyContact",
        reply_markup=main_menu,
        parse_mode="Markdown"
    )
    context.user_data.clear()
    return ConversationHandler.END

async def form_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "❌ فرم لغو شد. هر وقت خواستید دوباره شروع کنید.",
        reply_markup=main_menu
    )
    return ConversationHandler.END

# ==================== هندلرهای اصلی ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 {name} عزیز، به سرویس خدمات آرت اپلای خوش آمدید!\n\n"
        "👇 از منوی زیر سرویس مورد نظر را انتخاب کنید:",
        reply_markup=main_menu
    )

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👇 خدمات آرت اپلای را انتخاب کنید:", reply_markup=main_menu)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📦 بسته‌های اپلای":
        await update.message.reply_text("لطفاً بسته مورد نظر خود را انتخاب کنید:", reply_markup=packages_menu)

    elif text == "🎓 بسته کارشناسی":
        await update.message.reply_text(
            "🎓 *بسته کارشناسی*\n\nبرای تحصیل در مقطع کارشناسی، تیم آرت اپلای به صورت تخصصی و با ارائه‌ی مشاوره‌ی دقیق، بهترین مقصد را برای شما پیشنهاد و تمامی امور اپلای را انجام می‌دهد.\n\nدر صورتی که سوال بیشتری دارید، می‌توانید از پشتیبان آرت اپلای بپرسید.",
            parse_mode="Markdown"
        )
        await update.message.reply_text("❓ سوالات متداول:", reply_markup=faq_karshenas_keyboard())

    elif text == "🎓 بسته کارشناسی ارشد":
        await update.message.reply_text(
            "🎓 *بسته کارشناسی ارشد*\n\nبرای تحصیل در مقطع کارشناسی‌ارشد، تیم آرت اپلای به صورت تخصصی و با ارائه‌ی مشاوره‌ی دقیق، بهترین مقصد را برای شما پیشنهاد و تمامی امور اپلای را انجام می‌دهد.\n\nدر صورتی که سوال بیشتری دارید، می‌توانید از پشتیبان آرت اپلای بپرسید.",
            parse_mode="Markdown"
        )
        await update.message.reply_text("❓ سوالات متداول:", reply_markup=faq_arshad_keyboard())

    elif text == "🎓 بسته دکتری":
        await update.message.reply_text(
            "🎓 *بسته دکتری*\n\nبرای تحصیل در مقطع دکتری، تیم آرت اپلای به صورت تخصصی و با ارائه‌ی مشاوره‌ی دقیق، بهترین مقصد را برای شما پیشنهاد و تمامی امور اپلای را انجام می‌دهد.\n\nدر صورتی که سوال بیشتری دارید، می‌توانید از پشتیبان آرت اپلای بپرسید.",
            parse_mode="Markdown"
        )
        await update.message.reply_text("❓ سوالات متداول:", reply_markup=faq_doktori_keyboard())

    elif text == "🧑‍🏫 بسته منتورینگ":
        await update.message.reply_text(
            "🧑‍🏫 *بسته منتورینگ*\n\nمنتورینگ یکی از پر طرفدارترین خدمات آرت اپلای است که طی چهار سال گذشته، بیش از 200 اپلیکنت از این خدمت استفاده کرده و مستقیماً با موسس و مدیر آرت اپلای در ارتباط بودند.\n\nبیش از 90 درصد از این افراد موفق به اخذ پذیرش و بورسیه تحصیلی از بهترین دانشگاه‌های دنیا شدند.",
            parse_mode="Markdown"
        )
        await update.message.reply_text("❓ سوالات متداول:", reply_markup=faq_mentoring_keyboard())

    elif text == "📋 تهیه مدارک اپلای":
        await update.message.reply_text(
            "📋 *تهیه مدارک اپلای*\n\n"
            "📝 نگارش و ویرایش متن اولیه ایمیل: 30 یورو\n"
            "📝 انگیزه‌نامه: 70 یورو\n"
            "📝 متن توصیه‌نامه: 20 یورو\n"
            "📝 سی‌وی: 50 یورو\n"
            "🎨 طراحی پورتفولیو: 150 یورو\n"
            "📄 پروپزال: بسته به موضوع بین 200 تا 500 یورو\n"
            "🌐 طراحی وبسایت: شروع قیمت از 200 یورو\n\n"
            "برای ثبت سفارش می‌توانید به پشتیبان آرت اپلای پیام دهید.",
            parse_mode="Markdown"
        )
        await update.message.reply_text("❓ سوالات متداول:", reply_markup=faq_madarek_keyboard())

    elif text == "🧳 مشاوره اپلای":
        await update.message.reply_text(
            "🧳 *مشاوره اپلای*\n\nجهت رزرو وقت مشاوره تحصیلی:\n🔗 Apply.planovin.com",
            parse_mode="Markdown"
        )
        await update.message.reply_text("❓ سوالات متداول:", reply_markup=faq_consulting_keyboard())

    elif text == "📞 ارتباط با پشتیبانی":
        await update.message.reply_text(
            "📞 *ارتباط با پشتیبانی*\n\n👤 @ArtApplyContact",
            parse_mode="Markdown"
        )

    elif text == "🏆 پرونده‌های موفق":
        await update.message.reply_text(
            "🏆 *پرونده‌های موفق*\n\n👉 @ArtApplyStories",
            parse_mode="Markdown"
        )

    elif text == "↩️ بازگشت به منوی اصلی":
        await update.message.reply_text("👇 از منوی زیر سرویس مورد نظر را انتخاب کنید:", reply_markup=main_menu)

    else:
        await update.message.reply_text("لطفاً از منوی زیر انتخاب کنید 👇", reply_markup=main_menu)

async def handle_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("back_"):
        prefix = data.replace("back_", "")
        keyboard_fn = back_keyboards.get(prefix)
        if keyboard_fn:
            await query.message.reply_text("❓ سوالات متداول:", reply_markup=keyboard_fn())
        return

    answer = answers.get(data)
    question = question_titles.get(data, "")
    if not answer:
        return

    prefix = "md" if data.startswith("md_") else data.split("_")[0]

    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("↩️ بازگشت به سوالات", callback_data=f"back_{prefix}")]
    ])

    await query.message.reply_text(
        f"❓ *{question}*\n\n{answer}",
        reply_markup=back_button,
        parse_mode="Markdown"
    )

# ==================== اجرا ====================

def main():
    app = Application.builder().token(TOKEN).build()

    # ConversationHandler برای فرم ارزیابی
    form_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^✅ ارزیابی رایگان$"), form_start)],
        states={
            F_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_name)],
            F_TELEGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_telegram)],
            F_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_email)],
            F_BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_birth)],
            F_DEGREE: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_degree)],
            F_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_field)],
            F_UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_university)],
            F_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_status)],
            F_GRAD_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_grad_year)],
            F_REMAINING: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_remaining)],
            F_GPA: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_gpa)],
            F_TARGET_DEGREE: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_target_degree)],
            F_TARGET_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_target_field)],
            F_COUNTRIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_countries)],
            F_PAPERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_papers)],
            F_EXHIBITIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_exhibitions)],
            F_LANG_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_lang_status)],
            F_LANG_SCORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_lang_score)],
            F_APPLY_KNOW: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_apply_know)],
            F_PORTFOLIO_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_portfolio_level)],
            F_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_other)],
            F_FILES: [
                MessageHandler(filters.Document.ALL, f_files),
                MessageHandler(filters.PHOTO, f_files),
                MessageHandler(filters.TEXT & ~filters.COMMAND, f_files),
            ],
        },
        fallbacks=[CommandHandler("cancel", form_cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("services", services_command))
    app.add_handler(form_handler)
    app.add_handler(CallbackQueryHandler(handle_faq))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
