import logging
from pprint import pprint

from django.db import connection

logger = logging.getLogger(__name__)

class QueryDebuggerMiddleware(object):
    def process_response(self, request, response):
        pprint(connection.queries)
        return response    