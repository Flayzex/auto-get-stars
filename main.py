import asyncio
import time
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

            if not message.reply_markup:
                await client.send_message(bot_chat.id, '/start')
                time.sleep(2)
                messages = client.get_chat_history(chat_id=bot_chat.id, limit=1)
                async for i in messages:
                    message: Message = i

            logging.info(await message.click(0))
            time.sleep(121)
        except Exception as e:
            logging.warning(e)
            await asyncio.sleep(10)


    await idle()
    await client.stop()


if __name__ == '__main__':
    asyncio.run(start())
