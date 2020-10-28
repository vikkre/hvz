from logging import exception
import urllib3
import os
import time
import logging


web_host = os.getenv("WEB_HOST", "localhost")
log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
max_count = 10
url = f'http://{web_host}/builddone'
sleep_seconds = 2

logging.basicConfig(format='%(name)s : %(message)s', level=log_level)
logger = logging.getLogger("waitfor_frontend_build")
if __name__ == "__main__":
    http = urllib3.PoolManager()
    cnt = 1
    while True:
        logger.info(f"Waiting for {url} ({cnt} of {max_count})")
        try:
            response = http.request('GET', url, retries=False)
            if response.status == 200:
                logger.info(f"Wait for {url} successfull")
                break
        except exception as e:
            logger.error(e)
            pass
        cnt += 1
        if cnt > max_count:
            logger.info(f"Wait for {url} failed")
            break
        time.sleep(sleep_seconds)
