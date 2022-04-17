"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import uuid

from aiogram import Bot, Dispatcher, executor, types
from main import AdsMarkup

API_TOKEN = '5335539843:AAEvL83JVodo7PJ0BUT_eoucFN9fGoztOt4'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)

@dp.message_handler(content_types=["video"])
async def video_answer(message: types.Message):
    file_id = message['video']['file_id']
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    disk_path = f"/home/john/Downloads/{uuid.uuid4()}.mp4"

    await bot.download_file(file_path, disk_path)
    f = 'ffmpeg'

    
    a = AdsMarkup(disk_path, f)
    a.get_markup_vector()
    v = a.get_top_result()


    await message.answer(str(v))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)