import json

import redis.asyncio as redis

from app.core.config import settings

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)


async def publish_task_event(event: dict):
    await r.publish("task_events", json.dumps(event))
