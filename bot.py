from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import dispatcher
from aiogram.utils.executor import Executor
from config import TOKEN, admins_id
import os


order_number = ''
bot = Bot(token=TOKEN)
dp = dispatcher(bot)


main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add("Химчистка обуви").add("Химчистка сумок").add("Чистка аксессуаров из кожи")

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add("Химчистка обуви").add("Химчистка сумок").add("Чистка аксессуаров из кожи").add("Админка")

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Получить фото заказов')


@dp.message_handler(commands=['start']) 
async def process_start_command(message: types.Message):
    await message.reply(f"Здравствуйте, {message.from_user.first_name}! Я бот-менеджер, призванный упростить ваше общение и сэкономить время. \nКакая услуга вас интересует?", reply_markup=main)
    if message.from_user.id == int(admins_id):
        await message.answer("Вы вошли в админку", reply_markup=main_admin) 


@dp.message_handler(commands=['help']) 
async def process_help_command(message: types.Message):
    await message.reply("/start - начало работы с ботом\n/help - информация о возможностях бота")


@dp.message_handler(text="Химчистка обуви")
async def cleaning(message: types.Message):
    global order_number
    await message.answer('Отправьте 4 фото обуви со всех сторон', reply_markup=types.ReplyKeyboardRemove())
    if not os.path.exists(f'photos/{message.from_user.id}'):
        os.mkdir(f'photos/{message.from_user.id}')
    order_number = len(os.listdir(f'photos/{message.from_user.id}')) + 1


@dp.message_handler(text="Химчистка сумок")
async def cleaning(message: types.Message):
    global order_number
    await message.answer("Отправьте 4 фото сумки со всех сторон", reply_markup=types.ReplyKeyboardRemove())
    if not os.path.exists(f'photos/{message.from_user.id}'):
        os.mkdir(f'photos/{message.from_user.id}')
    order_number = len(os.listdir(f'photos/{message.from_user.id}')) + 1


@dp.message_handler(text="Чистка аксессуаров из кожи")
async def cleaning(message: types.Message):
    global order_number
    await message.answer("Отправьте фото изделия со всех сторон", reply_markup=types.ReplyKeyboardRemove())
    if not os.path.exists(f'photos/{message.from_user.id}'):
        os.mkdir(f'photos/{message.from_user.id}')
    order_number = len(os.listdir(f'photos/{message.from_user.id}')) + 1


@dp.message_handler(text="Админка")
async def admin(message: types.Message):
    await message.answer("Вы вошли в админку", reply_markup=admin_panel)


@dp.message_handler()
async def nothing(message: types.Message):
    await message.answer("Я вас не понимаю используйте комманду /help")


flag_group_id = None


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def save_photo(media_group_id):
    media_group = await bot.get_media_group(media_group_id)
    for message in media_group:
        if message.photo:
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            with open('photo.jpg', 'wb') as new_file:
                new_file.write(downloaded_file)
    # global order_number, flag_group_id
    # if message.media_group_id and not flag_group_id:
    #     flag_group_id = message.media_group_id 
    #     photo = message.photo[-1]
    #     image_name = message.from_user.first_name + '_' + message.from_user.last_name + "_" + message.message_id
    #     photo_path = f'photos/{message.from_user.id}/{image_name}.jpg'
    #     await photo.download(photo_path)
    #     await message.answer("Фото будут пересланы мастеру. Пожалуйста, ожидайте ответа")
    #     await message.answer(message.message_id)
    # else:
    #     if not message.media_group_id:
    #         flag_group_id = None



@dp.message_handler(text='Получить фото заказов')
async def send_orders(message: types.Message):
    await message.answer("Просто")



if __name__ == '__main__':
    Executor.start_polling(dp, skip_updates=True)
