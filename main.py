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

    message: Message = await client.get_messages(bot_chat.id, 1272)
    while True:
        try:
            logging.info(await message.click(0))
            time.sleep(121)
        except Exception as e:
            logging.warning(e)
            asyncio.sleep(10)


    await idle()
    await client.stop()


if __name__ == '__main__':
    asyncio.run(start())
