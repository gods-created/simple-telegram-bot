import aiogram
import os
from aiogram import Router
from aiogram.types import Message, FSInputFile
from loguru import logger

from modules.ai import AI

app = Router()

@app.message()
async def _generate_image(message: Message) -> None:
    image_name = None
    
    try:
        await message.answer('⏰ ...')
                
        text = message.text
        
        with AI() as ai_class:
            generate_image_response = await ai_class.generate_image(text)
        
        status = generate_image_response['status']
        response = generate_image_response['response']
        image_name = generate_image_response['image_name']
        
        await message.answer(response)
        
        if status == 'success':
            await message.answer_photo(
                FSInputFile(image_name),
                caption=text
            )
    
    except aiogram.exceptions.TelegramBadRequest as e:
        logger.error(str(e))
        
    except Exception as e:
        logger.error(str(e))
        
    finally:
        if image_name is not None:
            os.remove(image_name)
