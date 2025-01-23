from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
                          ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



LANGUAGES_LABELS = (
    '🇺🇿  O\'zbekcha',
    "🇺🇿  Ўзбекча (Кирил)",
    "🇺🇸 English",      
    "🇷🇺 Русский"
)

def LANGUAGES():
    return ReplyKeyboardMarkup(
        keyboard=[[i] for i in LANGUAGES_LABELS],
        resize_keyboard=True
    )

def PROFESSION(lang):
    if lang == 'uz':
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🤵‍♂️ Tashkilotchi", callback_data="a-moderator:uz")],
                [InlineKeyboardButton("🧑‍🏫 O'qituvchi", callback_data="a-teacher:uz")],
            ]
        )
    elif lang == 'cr':
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🤵‍♂️ Ташкилотчи", callback_data="a-moderator:cr")],
                [InlineKeyboardButton("🧑‍🏫 Ўқитувчи", callback_data="a-teacher:cr")],
            ]
        )
    elif lang == 'ru':
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🤵‍♂️ Организатор", callback_data="a-moderator:ru")],
                [InlineKeyboardButton("🧑‍🏫 Учитель", callback_data="a-teacher:ru")],
            ]
        )
    elif lang == 'en':
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🤵‍♂️ Moderator", callback_data="a-moderator:en")],
                [InlineKeyboardButton("🧑‍🏫 Teacher", callback_data="a-teacher:en")],
            ]
        )
        
def AUTH(lang, url):
    if (lang == 'uz'):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🔑 Kirish", url=url)]
            ]
        )
    elif (lang == 'cr'):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🔑 Кириш", url=url)]
            ]
        )
    elif (lang == 'ru'):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🔑 Вход", url=url)]
            ]
        )
    elif (lang == 'en'):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("🔑 Login", url=url)]
            ]
        )