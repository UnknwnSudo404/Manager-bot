from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import dispatcher
from aiogram.utils import executor
from aiogram.types import input_media
from aiogram.types import input_file

import asyncio
import requests
import io
import os
from PIL import Image
from typing import List

from aiogram import __version__

from config import TOKEN, admins_id

print(__version__)
bot = Bot(token=TOKEN)
dp = dispatcher.Dispatcher(bot)


main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add("Химчистка обуви").add("Химчистка сумок").add("Чистка аксессуаров из кожи")

main_master = ReplyKeyboardMarkup(resize_keyboard=True)
main_master.add("Химчистка обуви").add("Химчистка сумок").add("Чистка аксессуаров из кожи").add("Мастер панель")

master_panel = ReplyKeyboardMarkup(resize_keyboard=True)
master_panel.add('Просмотр заказов')


@dp.message_handler(commands=['start']) 
async def process_start_command(message: types.Message):
    await message.reply(f"Здравствуйте, {message.from_user.first_name}! Я бот-менеджер, призванный упростить ваше общение и сэкономить время. \nКакая услуга вас интересует?", reply_markup=main)
    if message.from_user.id == int(admins_id):
        await message.reply("Вы находитесь в мастер режиме", reply_markup=main_master) 


@dp.message_handler(commands=['help']) 
async def process_help_command(message: types.Message):
    await message.reply("/start - начало работы с ботом\n/help - информация о возможностях бота")


@dp.message_handler(text="Химчистка обуви")
async def cleaning(message: types.Message):
    await message.reply('Отправьте фото обуви', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text="Химчистка сумок")
async def cleaning(message: types.Message):
    await message.reply("Отправьте фото сумки", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text="Чистка аксессуаров из кожи")
async def cleaning(message: types.Message):
    await message.reply("Отправьте фото изделия", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text="Мастер панель")
async def admin(message: types.Message):
    await message.reply("Вы вошли в мастер режим", reply_markup=master_panel)


@dp.message_handler(text="Просмотр заказов")
async def watching_orders(message: types.Message):
    for i in range(len(os.listdir("database"))):
        if len(os.listdir('database' + '/' + os.listdir(f"database")[i])) != 0:
            a = input_file.InputFile('database' + '/' + os.listdir('database')[i] + '/' + os.listdir('database' + '/' + os.listdir('database')[i])[0])
            phhot = input_media.InputMediaPhoto(a)
            await bot.send_photo(chat_id=message.from_user.id,photo=a)
            await message.reply("Оцените стоимость данной работы, а затем она будет отправлена", reply_markup=master_panel)
            path_price = 'database/' + os.listdir('database')[i]
            with open(path_price, 'r+') as file:
                file.write(save_user_response())


@dp.message_handler()
async def save_user_response(message: types.Message):
    price = message.text
    return price


@dp.message_handler(content_types=['photo'])
async def save_photo(message: types.Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    photo_path = file.file_path
    downloaded_photo = await bot.download_file(photo_path)
    if not os.path.exists(f"database/{message.from_user.id}"):
        os.mkdir(f"database/{message.from_user.id}")
    with open(f"database/{message.from_user.id}/{message.message_id}.jpg", 'wb') as new_photo_file:
        new_photo_file.write(downloaded_photo.read())
    await message.reply("Фото будет переслано мастеру, мы ответим вам как только мастер оценит стоимость работы", reply_markup=main)


@dp.message_handler()
async def fignya(message: types.Message):
    await message.reply("Я устал /help")

# тык
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
