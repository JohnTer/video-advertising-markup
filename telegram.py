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

📀 Чтобы разметить видео, загрузите его через специальную форму вашего телеграм-клиента. Процесс разметки может идти достаточно долго (в зависимости от длины загруженного ролика). К подписи у видео укажите желаемое число ключевых точек (1-10) и режим работы (s - равномерное распределение). 

⏱ После обработки, будет отправлен список таймкодов, по котором можно переходить к нужному месту ролика просто кликнув на них.

""")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Необходимо прислать видео.')

@dp.message_handler(content_types=["video"])
async def video_answer(message: types.Message):
    file_id = message['video']['file_id']
    file = await bot.get_file(file_id)
    file_path = file.file_path

    smart_mode = False
    try:
        caption_text = message.caption
        if caption_text[0] == 's':
            smart_mode = True
            caption_text = caption_text[1:]
        point_num = int(caption_text)
        if point_num > 10 or point_num < 1:
            point_num = 10
    except:
        point_num = 5
        smart_mode = False

    
    disk_path = f"/home/john/Downloads/{uuid.uuid4()}.mp4"

    await bot.download_file(file_path, disk_path)
    ffmpeg = 'ffmpeg'

    
    a = AdsMarkup(disk_path, ffmpeg)
    a.get_markup_vector()

    if smart_mode:
        v = a.get_n_result(point_num)
    else:
        v = a.get_top_result(point_num)

    answer_message = 'Таймкоды:\n'
    
    time_by_score_list = []
    for res in v:
        t = (res['time'])
        if t not in time_by_score_list:
            time_by_score_list.append(t)

    
    for t in time_by_score_list:
        line_message = str(datetime.timedelta(seconds=t))
        line_message = line_message.split('.')
        if len(line_message) > 1:
            answer_message += f'⏱ {line_message[0]}.{line_message[1][:2]}\n'
        else:
            answer_message += f'⏱ {line_message[0]}.00\n'


    await message.reply(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)