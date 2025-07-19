import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
from app.config import config

redis_broker = RedisBroker(host=config.REDIS_HOST, port=config.REDIS_PORT)
redis_broker.add_middleware(AsyncIO())
dramatiq.set_broker(redis_broker)


from app.src.ai import service as ai

ai.model = ai.LoraModelForCausalLM(
    path_to_model=config.PATH_TO_MODEL, use_emoji=False
)