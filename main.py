from loguru import logger
from modules.env import Env
import asyncio
import os

import aiogram
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from routers.ai import app as ai_router

Env.create()
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message) -> None:
    try:
        user_fullname = message.from_user.full_name
        
        reply_message = f'''
Hello, <b>{user_fullname}!</b>\n
<i>For looking other commands, click</i> <b>/help</b>
        '''
        await message.reply(reply_message, parse_mode='HTML')
    
    except aiogram.exceptions.TelegramBadRequest as e:
        logger.error(str(e))
        
    except Exception as e:
        logger.error(str(e))
    
@dp.message(Command('help'))
async def help(message: Message) -> None:
    try:
        cmds = '''
/start - Relaunch bot
/help - Show all commands
        '''
        
        await message.answer(cmds, parse_mode='HTML')
        
    except aiogram.exceptions.TelegramBadRequest as e:
        logger.error(str(e))
        
    except Exception as e:
        logger.error(str(e))
    
async def main() -> None:
    bot = Bot(token=os.environ.get('BOT_TOKEN'))
    dp.include_router(ai_router)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        loop.close()
        
    except KeyboardInterrupt:
        logger.info('Close bot executing.')
        
    except Exception as e:
        logger.error(str(e))
