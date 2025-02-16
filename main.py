import asyncio
import logging

from pyrogram import Client, idle
from pyrogram.types import Message

from config import Config

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s - %(message)s",
    level=logging.INFO
)


async def start():
    client = Client('my_account', api_id=Config.API_ID, api_hash=Config.API_HASH)

    await client.start()

    bot_chat = await client.get_chat('GoStars_robot')
    messages = client.get_chat_history(chat_id=bot_chat.id, limit=1)
    async for i in messages:
        message: Message = i

    while True:
        try:
            # Если нет reply_markup (кнопки)
            if not message.reply_markup:
                await client.send_message(bot_chat.id, '/start')
                await asyncio.sleep(2)
                messages = client.get_chat_history(chat_id=bot_chat.id, limit=1)
                async for i in messages:
                    message: Message = i

            # Пытаемся нажать кнопку
            response = await message.click(0)
            logging.info(response)

            # Если в ответе указано время ожидания, парсим его
            if "⌛ Подождите еще" in response.message:
                wait_time = extract_wait_time(response.message)
                logging.info(f"Ожидание {wait_time} секунд перед следующим кликом")
                await asyncio.sleep(wait_time)
            else:
                # Если времени ожидания нет, ждем стандартное время
                await asyncio.sleep(121)

        except Exception as e:
            logging.warning(e)

            # При ошибке ждем несколько секунд и пробуем заново
            await asyncio.sleep(10)
            await client.send_message(bot_chat.id, '/start')
            await asyncio.sleep(2)
            messages = client.get_chat_history(chat_id=bot_chat.id, limit=1)
            async for i in messages:
                message: Message = i

    await idle()
    await client.stop()


def extract_wait_time(message: str) -> int:
    """
    Извлекает время ожидания в секундах из сообщения бота.
    Например: "⌛ Подождите еще 1 мин 54 сек перед следующим кликом"
    """
    import re

    match = re.search(r"(\d+)\s*мин.*?(\d+)\s*сек", message)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        return minutes * 60 + seconds
    match = re.search(r"(\d+)\s*сек", message)
    if match:
        return int(match.group(1))
    return 121  # По умолчанию, если время не указано


if __name__ == '__main__':
    asyncio.run(start())