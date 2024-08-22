import redis
import logging
import json
from typing import Any, Optional, Dict, Union

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """Initialize the Redis client."""
        self.host = host
        self.port = port
        self.db = db
        self.client = self._connect()

    def _connect(self) -> redis.Redis:
        """Establish a connection to Redis."""
        try:
            client = redis.Redis(host=self.host, port=self.port, db=self.db)
            client.ping()  # Check connection
            logger.info(f"Connected to Redis at {self.host}:{self.port}, DB: {self.db}")
            return client
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    def save_object(self, key: str, obj: Union[Dict[str, Any], str]) -> None:
        """Save a Python dictionary object or a string in Redis."""
        try:
            if isinstance(obj, dict):
                obj_json = json.dumps(obj)
            else:
                obj_json = str(obj)  # Convert the object to string if it's not a dictionary

            self.client.set(key, obj_json)
            logger.info(f"Saved object to Redis with key: {key}")
        except redis.RedisError as e:
            logger.error(f"Failed to save object to Redis: {e}")
            raise

    def get_object(self, key: str) -> Optional[Union[Dict[str, Any], str]]:
        """Retrieve a Python dictionary object or string from Redis by key."""
        try:
            obj_json = self.client.get(key)
            if obj_json:
                try:
                    # Try to parse the JSON string as a dictionary
                    obj = json.loads(obj_json)
                    logger.info(f"Retrieved JSON object from Redis with key: {key}")
                    return obj
                except json.JSONDecodeError:
                    # If parsing fails, return the string as-is
                    logger.info(f"Retrieved string from Redis with key: {key}")
                    return obj_json.decode('utf-8')
            logger.warning(f"Key {key} not found in Redis.")
            return None
        except redis.RedisError as e:
            logger.error(f"Failed to retrieve object from Redis: {e}")
            raise
