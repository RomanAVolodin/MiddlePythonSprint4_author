import backoff
from elasticsearch import Elasticsearch
from logger import logger

from tests.functional.settings import test_settings


def backoff_hdlr(details):
    logger.info(
        'Backing off {wait:0.1f} seconds after {tries} tries '
        'calling function {target} with args {args} and kwargs '
        '{kwargs}'.format(**details)
    )


@backoff.on_exception(backoff.expo, Exception, max_time=300, on_backoff=[backoff_hdlr])
def connect_to_elasticsearch(es_client):
    if es_client.ping():
        logger.info('Success connecting to Elasticsearch')
        return True
    raise Exception('Failed to connect to Elasticsearch')


if __name__ == '__main__':
    es_host = test_settings.elastic_settings.get_host()
    with Elasticsearch(hosts=es_host) as es_client:
        connect_to_elasticsearch(es_client)
