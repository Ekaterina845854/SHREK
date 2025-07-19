import asyncio

import redis.asyncio as redis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from app.config import config
from app.handlers import base, character, errors, chat
from app.utils import commands


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    
    redis_client = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=0,
        decode_responses=True,
    )
    storage = RedisStorage(redis_client, state_ttl=3600) 
    
    redis_cache = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=0
    )
    
    dp = Dispatcher(storage=storage)

    dp.include_router(base.router)
    dp.include_router(errors.router)
    dp.include_router(character.router)
    dp.include_router(chat.router)
    
    from app.utils import api
    api.redis = redis_cache
    
    await bot.set_my_commands(
        commands=commands.private_commands
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
