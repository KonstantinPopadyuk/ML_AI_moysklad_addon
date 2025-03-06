from functools import wraps
from datetime import timedelta
import redis
import json
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

def cache_response(key_prefix: str, ttl: timedelta):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{':'.join(map(str, kwargs.values()))}"
            cached_data = None
            
            try:
                cached_data = redis_client.get(cache_key)
            except redis.RedisError as e:
                logger.error(f"Redis error: {e}. Proceeding without cache.")
            
            if cached_data:
                return JSONResponse(content=json.loads(cached_data))
            
            result = await func(*args, **kwargs)
            
            try:
                ttl_seconds = int(ttl.total_seconds())
                redis_client.setex(cache_key, ttl_seconds, json.dumps(result))
            except redis.RedisError as e:
                logger.error(f"Redis error: {e}. Result not cached.")
            
            return result
        return wrapper
    return decorator