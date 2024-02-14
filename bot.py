from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
import io
import os
from PIL import Image


from config import TOKEN, admins_id


URI_info = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id="
URI = f"https://api.telegram.org/file/bot{TOKEN}/" 

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add("Химчистка обуви").add("Химчистка сумок").add("Чистка аксессуаров из кожи")

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add("Химчистка обуви").add("Химчистка сумок").add("Чистка аксессуаров из кожи").add("Админ панель")

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Админка')


@dp.message_handler(commands=['start']) 
async def process_start_command(message: types.Message):
    await message.reply(f"Здравствуйте, {message.from_user.first_name}! Я бот-менеджер, призванный упростить ваше общение и сэкономить время. \nКакая услуга вас интересует?", reply_markup=main)
    if message.from_user.id == int(admins_id):
        await message.answer("Вы вошли в админку", reply_markup=admin) 


@dp.message_handler(commands=['help']) 
async def process_help_command(message: types.Message):
    await message.reply("/start - начало работы с ботом\n/help - информация о возможностях бота")


@dp.message_handler(text="Химчистка обуви")
async def cleaning(message: types.Message):
    await message.answer('Отправьте 4 фото обуви со всех сторон', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text="Химчистка сумок")
async def cleaning(message: types.Message):
    await message.answer("Отправьте 4 фото сумки со всех сторон", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text="Чистка аксессуаров из кожи")
async def cleaning(message: types.Message):
    await message.answer("Отправьте фото изделия со всех сторон", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text="Админка")
async def admin(message: types.Message):
    await message.answer("Вы вошли в админку", reply_markup=admin_panel)


@dp.message_handler()
async def fignya(message: types.Message):
    await message.answer("Я устал /help")


# @dp.message_handler(content_types=['photos'])
# async def save_photo(message: types.Message):
#     await message.answer("Крутые фотки, бро")
#     file_id = message.photo[3].file_id
#     uri = URI_info + file_id
#     resp = requests.get(uri)
#     img_path = resp.json()['result']['file_path']
#     img = requests.get(URI + img_path)
#     img = Image.open(io.BytesIO(img.content))
#     if not os.path.exists("database"):
#         os.mkdir('database')
#     img.save(f"database/{len(os.listdir)}.png", format="PNG")


@dp.message_handler(content_types=ContentType.PHOTO)
async def process_photo(message: types.Message):
    photos = message.photo
    for photo in photos:
        await photo.download()
        process_photo(photo.file)



if __name__ == '__main__':
    executor.start_polling(dp)
