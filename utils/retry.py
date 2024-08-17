from functools import wraps
import logging
import time

logger = logging.getLogger(__name__)

def retry(retries=3, delay=15):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                    attempt += 1
                    time.sleep(delay)
            logging.error(f"All {retries} retry attempts failed.")
            raise Exception("Failed after all retries")
        return wrapper
    return decorator