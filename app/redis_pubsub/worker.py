import asyncio
import logging

import redis.asyncio as redis

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_worker():
    r = redis.Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
    )
    pubsub = r.pubsub()
    await pubsub.subscribe("task_events")
    logger.info("Worker started, listening for events...")
    async for message in pubsub.listen():
        if message["type"] == "message":
            logger.info(f"Event: {message['data']}")


if __name__ == "__main__":
    asyncio.run(run_worker())
