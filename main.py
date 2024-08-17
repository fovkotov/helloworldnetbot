import requests
import time
from random import choice


API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
BOT_TOKEN = '7533832481:AAF-al04aUVQHfVzbIE-Ro5M7Iw2qtkGgaA'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('
HH_API_URL = 'https://api.hh.ru/vacancies'

from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token


params = {
    'text': 'уборщик',
    'area': '1',
    'per_page': '1',
    'page': '0'
}

offset = -2
counter = 0

def get_random_cleaner_vacancy():
    try:
        response = requests.get(HH_API_URL, params={
            'text': 'уборщик',
            'per_page': 100,  # Запрашиваем до 100 вакансий
            'page': 0
        })
        response.raise_for_status()
        data = response.json()
        vacancies = data.get('items', [])
        if vacancies:
            # Выбираем случайную вакансию
            import random
            vacancy = random.choice(vacancies)
            return vacancy.get('alternate_url', 'Нет ссылки на вакансию')
        else:
            return 'Вакансий не найдено'
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе вакансий: {e}")
        return ERROR_TEXT

while counter < 100000:
    print('attempt =', counter)
    try:
        updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset}').json()
        print("Response from Telegram API:", updates)

        if updates.get('ok') and updates.get('result'):
            for result in updates['result']:
                offset = result['update_id'] + 1
                chat_id = result['message']['chat']['id']

                # Получаем случайную вакансию уборщика
                vacancy_link = get_random_cleaner_vacancy()

                # Отправляем ссылку на вакансию
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Вот вакансия уборьщика: {vacancy_link}')

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к Telegram API: {e}")

    time.sleep(1)
    counter += 1

# commit
# from aiogram import Bot, Dispatcher, F
# from aiogram.filters import CommandStart
# from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# from aiogram.types import CallbackQuery
# from aiogram.types import InputMediaPhoto
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup

# class IdeaSubmission(StatesGroup):
#     waiting_for_idea = State()


# # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# # полученный у @BotFather
# BOT_TOKEN = '7269905708:AAEREWA1eQYooU_BvlZM5ni3No_aLt4KwWE'

# # Создаем объекты бота и диспетчера
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()

# # Создаем объекты кнопок
# button_1 = KeyboardButton(text='О проекте')
# button_2 = KeyboardButton(text='Каталог')
# button_3 = KeyboardButton(text='FAQ')
# button_4 = KeyboardButton(text='Наш процесс')

# # Создаем объект клавиатуры, добавляя в него кнопки
# keyboard = ReplyKeyboardMarkup(
#     keyboard=[[button_1, button_2],
#               [button_3, button_4]],
#     resize_keyboard=True
# )


# # Этот хэндлер будет срабатывать на команду "/start"
# # и отправлять в чат клавиатуру
# @dp.message(CommandStart())
# async def process_start_command(message: Message):
#     photo = open('/Users/hanna/Desktop/тг-боты-codje/codje_bot/clone_git/cod.je_28.07/img/photo_2024-07-28_23-30-57.jpg', 'rb')
#     await message.answer(
#         text='Привет! Это COD.JE \n'
#         'Мы -  бренд генеративной ювелирки. Создаем украшения, существующие на грани диджитал и физической среды. \n'
#         '\n'
#         'Тут можно узнать все о проекте и заказать колечко во всем боте (пока тестовый текст)',
#         media = InputMediaPhoto(media=photo, caption=caption)
#         await bot.send_media_group(chat_id=message.chat.id, media=[media])
#         reply_markup=keyboard
#     )

# # Создаем объекты инлайн-кнопок (цели)
# our_goals_button = InlineKeyboardButton(
#     text='Наши планы',
#     callback_data='goals_bt_pressed'
# )
# our_team_button = InlineKeyboardButton(
#     text='Комана',
#     callback_data='team_bt_pressed'
# )
# suggest_idea_btn = InlineKeyboardButton(
#     text='У меня есть идея',
#     url='https://t.me/fovkotov'
# )


# # Создаем объект инлайн-клавиатурки
# keyboard_goals = InlineKeyboardMarkup(
#     inline_keyboard=[[our_goals_button]]
# )
# keyboard_suggest = InlineKeyboardMarkup(
#     inline_keyboard=[[suggest_idea_btn]]
# )

# # "О проекте"
# @dp.message(F.text == 'О проекте')
# async def process_about_answer(message: Message):
#     await message.answer(
#         text='Границы между мирами стираются, мы чувствуем это. \n'
#         'Мы не сковываем наши объекты в рамки, мы даем им свободу и возможность перетекать из одной среды в другую, создавая новые формы и смыслы.'
#         'Наши украшения — это произведение искусства, созданное на стыке цифрового и физического миров...',
#         reply_markup=keyboard_goals
#     )

# # CallbackQuery "Наши цели"
# @dp.callback_query(F.data.in_(['goals_bt_pressed']))
# async def process_buttons_press(callback: CallbackQuery):
#     await callback.message.answer(
#         text='Мы постоянно растем, придумываем и воплощаем новые идеи. Вот, что мы запланировали на 2025 год: \n'
#         '20 сентября - выпустим новую партию колечек \n'
#         '30 сентября - станет доступной расширенная размерная сетка \n'
#         '10 декабря - крутейший колаб (пока не раскрываем с кем) \n'
#         '\n'
#         'А еще мы любим болтать с вами, вместе генерить идеи и создавать новое. Напишите нам, вместе подумаем как реализовать.',
#         reply_markup=keyboard_suggest
#         )

# # Пользователь написал идею и что-то ответил боту
# @dp.message(F.text.lower().in_(['готово', 'написал', 'написала', 'отправил',
#                                 'отправила']))
# async def process_ideasended_answer(message: Message):
#     await message.answer(
#         text='спасибо за идею! наш менеджер сейчас немного занят, он ответит тебе в течение дня, сразу как освободится. А пока можешь посмотреть наш каталог',
#         reply_markup=keyboard
#     )







# # # CallbackQuery "Предложить идею"
# # @dp.callback_query(F.data.in_(['idea_bt_pressed']))
# # async def process_buttons_press(callback: CallbackQuery):
# #     await callback.message.answer(
# #         text='Пожалуйста, опишите вашу идею:'
# #         )
# # @dp.callback_query(F.data == 'idea_bt_pressed')
# # async def process_suggest_idea(callback: CallbackQuery):
# #     await callback.message.answer(
# #         text='Пожалуйста, опишите вашу идею:'
# #     )
# #     await bot.set_state(user=callback.from_user.id, state=IdeaSubmission)

# # CallbackQuery "Предложить идею--2"
# # @dp.callback_query(F.data == 'idea_bt_pressed')
# # async def process_suggest_idea(callback: CallbackQuery):
# #     await callback.message.answer(
# #         text='Пожалуйста, опишите вашу идею:'
# #     )
# #     await bot.set_state(user=callback.from_user.id, state='waiting_for_idea')

# # State handler with state context
# @dp.message  # Use state group instead of state argument
# async def process_idea(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['idea'] = message.text
#     await bot.send_message(chat_id=YOUR_ADMIN_ID, text=f"Новая идея от {message.from_user.full_name}:\n{data['idea']}")
#     await message.answer("Спасибо за вашу идею! Мы обязательно ее рассмотрим.")
#     await state.finish()








# # Этот хэндлер будет срабатывать на ответ "Каталог"
# @dp.message(F.text == 'Каталог')
# async def process_catalog_answer(message: Message):
#     await message.answer(
#         text='Тут будет подробное описание проекта',
#     )



# if __name__ == '__main__':
#     dp.run_polling(bot)