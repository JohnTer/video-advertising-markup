"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import time
import uuid
import datetime

from aiogram import Bot, Dispatcher, executor, types
from main import AdsMarkup

API_TOKEN = ''

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
    await message.reply("""🤖 Данный бот предназначен для оптимальной разметки видео, куда можно вставить рекламу.

📀 Чтобы разметить видео, загрузите его через специальную форму вашего телеграм-клиента. Процесс разметки может идти достаточно долго (в зависимости от длины загруженного ролика).

⏱ После обработки, будет отправлен список таймкодов, по котором можно переходить к нужному месту ролика просто кликнув на них.

⭕ Чтобы включить режим рестриминга пришлите ссылку на валидный стрим после команды '/link <ссылка>'

Число обработанных видео: 0""")


@dp.message_handler(commands=['link'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    time.sleep(30)
    await message.reply(f'Stream: udp://194.135.22.86:2222?pkt_size=1316')





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

    answer_message = ''
    
    time_by_score_list = []
    for res in v:
        t = (res['time'])
        if t not in time_by_score_list:
            time_by_score_list.append(t)

    
    for t in time_by_score_list:
        line_message = str(datetime.timedelta(seconds=t))

        answer_message += f'⏱ {line_message}\n'

    await message.reply(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)