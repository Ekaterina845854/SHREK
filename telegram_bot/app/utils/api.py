import json
from typing import Optional

import aiohttp
from app.config import config
from app.utils.constants import CacheKeys, CachetTTL
from redis.asyncio import Redis

CACHE_TTL = config.CACHE_TTL

redis: Redis = None


class API:
    API_BASE_URL = config.API_BASE_URL

    @classmethod
    async def get_archetypes(cls) -> list[dict]:
        archetypes = await cls._get_data("/archetypes")
        return archetypes
    
    @classmethod
    async def get_styles(cls) -> list[dict]:
        styles = await cls._get_data("/styles")
        return styles
    
    @classmethod
    async def get_characters(cls, user_id: int) -> list[dict]:
        return await cls._get_characters(user_id)


    @classmethod
    async def get_character(cls, user_id: int, character_id: int) -> Optional[dict]:
        return await cls._get_character(user_id, character_id)
    
    @classmethod
    async def get_user_characters(cls, user_id: int) -> list[dict]:
        return await cls._get_characters(user_id, only_user=True)
    
    @classmethod
    async def delete_character(cls, user_id: int, character_id: int):
        return await cls._delete_character(user_id, character_id)
    
    @classmethod
    async def ask_character(cls, user_id: int, character_id: int, query):
        return await cls._ask_character(user_id, character_id, query)
    
    @classmethod
    async def check_task(cls, task_id: int):
        return await cls._check_task(task_id)
    
    @classmethod
    async def _ask_character(cls, user_id: int, character_id: int, query: str):
        return (await cls._post_query_to_api(
            f"/characters/{character_id}",
            params={
                "user_id": user_id,
                "query": query
            }
        ))["response"]
    
    @classmethod
    async def _check_task(cls, task_id: int):
        task_info = await cls._fetch_data_from_api(f"/tasks/{task_id}")
        
        if task_info["status"] == "failed":
            return False
        
        if task_info["status"] == "completed":
            return task_info["result"]
        
        return None
    
    @classmethod
    async def _get_character(
        cls, user_id: int, character_id: int, update_cache: bool = False
    ) -> Optional[dict]:
        character = await cls._get_data(
            f"/characters/{character_id}",
            params={"user_id": user_id, "expand": "style,archetype"},
            cache_key=CacheKeys.character(character_id),
            ttl=CachetTTL.CHARACTER,
            update_cache=update_cache
        )
        
        return character

    @classmethod
    async def _get_characters(cls, user_id: int, update_cache: bool = False, only_user: bool = False) -> list[dict]:
        characters = []
        
        if not only_user:
            characters.extend(await cls._get_data(
                "/characters",
                cache_key=CacheKeys.default_characters,
                update_cache=update_cache
            ))
        
        user_characters = await cls._get_data(
            "/characters",
            params={"user_id": user_id, "only": 1},
            cache_key=CacheKeys.user_characters(user_id),
            update_cache=update_cache,
            ttl=CachetTTL.CHARACTERS
        )
        
        if user_characters:
            characters.extend(user_characters)
        
        return characters
    
    @classmethod
    async def _delete_character(cls, user_id: int, character_id: int):
        status = await cls._delete_query_to_api(
            f"/characters/{character_id}",
            params={"user_id": user_id},
        )
        
        await cls._get_characters(user_id=user_id, update_cache=True, only_user=True)
        
        return status
    
    @classmethod
    async def create_character(cls, name: str, archetype_id: int, style_id: int, user_id: int) -> dict:
        data = {
            "name": name,
            "archetype_id": archetype_id,
            "style_id": style_id,
            "user_id": user_id,
        }
        
        params = {
            "expand": "archetype,style"
        }
        
        character = await cls._post_query_to_api("/characters", data, params)
        
        await cls._get_characters(user_id=user_id, update_cache=True)
        await cls._get_character(
            user_id=user_id, character_id=character["character_id"], update_cache=True
        )
        
        return character
    
    @classmethod
    async def _get_data(
        cls, resource: str, cache_key: Optional[str] = None, params: Optional[dict] = None,
        update_cache: bool = False, ttl: Optional[int] = CACHE_TTL
    ) -> list[dict]:
        if not cache_key:
            cache_key = "cache" + resource.replace('/', ':')
        
        if not update_cache:
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
        
        data = await cls._fetch_data_from_api(resource, params=params)
        
        await redis.set(cache_key, json.dumps(data), ex=ttl)
        return data
    
    @classmethod
    async def _fetch_data_from_api(cls, url: str, params: Optional[dict] = None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{cls.API_BASE_URL}{url}", params=params) as resp:
                    if not resp.ok:
                        text = await resp.text()
                        print(f"[ERROR] {resp.status} {url}: {text}")
                        return None
                    return await resp.json()
        except aiohttp.ClientError as e:
            print(f"[ERROR] Network error: {e}")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return None
    
    @classmethod
    async def _post_query_to_api(cls, url, data: Optional[dict] = None, params: Optional[dict] = None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{cls.API_BASE_URL}{url}", params=params, json=data) as resp:
                    return await resp.json()
        except aiohttp.ClientError as e:
            print(f"[ERROR] Network error: {e}")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return None

    @classmethod
    async def _delete_query_to_api(cls, url, params: Optional[dict] = None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(f"{cls.API_BASE_URL}{url}", params=params) as resp:
                    return resp.ok
        except aiohttp.ClientError as e:
            print(f"[ERROR] Network error: {e}")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return None