import backoff
from logger import logger

import redis
from tests.functional.settings import test_settings


def backoff_hdlr(details):
    logger.info(
        'Backing off {wait:0.1f} seconds after {tries} tries '
        'calling function {target} with args {args} and kwargs '
        '{kwargs}'.format(**details)
    )


@backoff.on_exception(backoff.expo, Exception, max_time=300, on_backoff=[backoff_hdlr])
def connect_to_redis(es_client):
    if es_client.ping():
        logger.info('Success connecting to Redis')
        return True
    raise Exception('Failed to connect to Redis')


if __name__ == '__main__':
    redis_conf = test_settings.redis_settings
    with redis.Redis(host=redis_conf.host, port=redis_conf.port) as r_client:
        connect_to_redis(r_client)
