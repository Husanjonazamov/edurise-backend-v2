
import requests
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
import dotenv

from helpers import texts, buttons
dotenv.load_dotenv('.env')

API_TOKEN = os.getenv('API_TOKEN')
BASE_URL = os.getenv('BASE_URL')
REDIRECT = os.getenv('REDIRECT')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode='html')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        text=texts.START,
        reply_markup=buttons.LANGUAGES()
    )

@dp.message_handler(lambda message: message.text.startswith(buttons.LANGUAGES_LABELS))
async def lang(message: types.Message):

    await message.answer('<b>Juda yaxshi</b>', reply_markup=types.ReplyKeyboardRemove())
    
    lang = {
        "🇺🇿  O'zbekcha":'uz',
        "🇺🇿  Ўзбекча (Кирил)":'cr',
        "🇺🇸 English":'en',
        "🇷🇺 Русский":'ru'
    }[message.text]
    
    await message.answer(
        text=texts.ROLE[lang],
        reply_markup=buttons.PROFESSION(lang)
    )

def CreateUser(role, call:types.CallbackQuery):
    user_id = call.from_user.id
    
    payload = {
        'user_id': user_id,
        'role': role,
    }

    return requests.post(BASE_URL + "user/auth/send-code/", data=payload)


@dp.callback_query_handler(lambda call: call.data.startswith('a-'))
async def profession(call: types.CallbackQuery):

    loading = await call.message.edit_text('⏳')
    
    data_split = call.data.replace('a-', '').split(':')
    role = data_split[0]
    lang = data_split[1]

    res = CreateUser(role, call)
    print("🚲 ~ bot.py:67 -> res: ",  res)

    if res.status_code == 201 or \
        res.status_code == 302 or \
        res.status_code == 200:
        data = res.json()
        redirect_url = REDIRECT + data['data']['redirect_url']
        return await loading.edit_text(
            text=texts.CODE_SUCCES[lang],
            reply_markup=buttons.AUTH(lang, redirect_url)
        )
    await call.message('Xatolik')
        

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)