# utils/common.py

import redis
import logging

def connect_to_keydb(keydb_url):
    """Connect to KeyDB and return the connection object."""
    try:
        r = redis.Redis.from_url(keydb_url)
        r.ping()
        logging.info("Successfully connected to KeyDB.")
        return r
    except redis.ConnectionError as e:
        logging.error(f"Failed to connect to KeyDB: {e}")
        raise Exception("Failed to connect to KeyDB")
