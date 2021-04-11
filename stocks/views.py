import redis
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from .redis_store import RedisStore
import json

class StocksSearchView(View):
    def get(self, request, input):
        rs = RedisStore(connection_pool=settings.REDIS_CONN_POOL)
        
        input = input.upper()
        stocks = rs.get_stock_data(input)

        return JsonResponse(stocks, safe=False)