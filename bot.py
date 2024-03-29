import asyncio
import logging

from aiogram import Bot, Dispatcher, F

from handlers import (start, choose_group, get_day_schedule, info, get_week_schedule, get_next_day_schedule,
                      check_sub)

from config import BOT_TOKEN

from aiogram.fsm.strategy import FSMStrategy

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.sub_send import send_sub_cron

from handlers.check_sub import edit_sub
# from handlers import choose_schedule, choose_group, week_schedule, start, rofl, groups, info, day_schedule

from utils.commands import set_commands




# GROUP = ''

CREATORS = "{<} Студенты Фокультета программирования {<}\n\nЯзыкин Артем \nИлья Конищук \nТретьяков Андрей"

"""ВТОРАЯ ВЕРСИЯ"""

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# logging.basicConfig(level=logging.INFO, filename='data/logs/my_logging.log',
#                     format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
#                     datefmt='%d/%m/%Y %I:%M:%S',
#                     encoding='utf-8', filemode='w')


# Запуск процесса поллинга новых апдейтов
async def main():

    # Объект бота
    bot = Bot(token=BOT_TOKEN)
    # Диспетчер
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
    await set_commands(bot)

    sendler = AsyncIOScheduler(timezone="Europe/Moscow")
    sendler.add_job(send_sub_cron, 'cron', day_of_week='mon-fri', hour=19, minute=0, end_date='2024-12-30',
                    kwargs={'bot': bot})
    sendler.start()

    dp.include_routers(start.router, choose_group.router, get_day_schedule.router,
                       get_week_schedule.router, get_next_day_schedule.router, info.router, check_sub.router)
    dp.callback_query.register(edit_sub, F.data.startswith('edit_sub'))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
