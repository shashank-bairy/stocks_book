import json
import redis

class RedisStore:
    def __init__(self, connection_pool):
        self._conn = redis.Redis(connection_pool=connection_pool)
        self._fields = [
            "code", "name", "open", "high", "low", "close"
        ]

    def _get_stock_list(self, stocks):
        stock_list = []
        for stock in stocks:
            stock = {
                "code": int(stock[b'code']),
                "name": stock[b'name'].decode("utf-8"),
                "open": float(stock[b'open']),
                "high": float(stock[b'high']),
                "low": float(stock[b'low']),
                "close": float(stock[b'close'])
            }
            stock_list.append(stock)
        return stock_list

    def get_stock_data(self, match):
        search_key = f"search:{match}*"
        if self._conn.exists(search_key):
            search_result = self._conn.get(search_key)
            search_result = json.loads(search_result)
        else:
            search_result = []
            with self._conn.pipeline() as pipe:
                i = 0
                for key in self._conn.scan_iter(f'stock:{match}*', 1000):
                    pipe.hgetall(key) 
                    i += 1
                    if i % 60 == 0:
                        results = pipe.execute()
                        search_result += self._get_stock_list(results)
                results = pipe.execute()
                search_result += self._get_stock_list(results)
            
            self._conn.set(search_key, json.dumps(search_result), ex=300)
        
        return search_result

    def insert_stock_data(self, stocks):
        # send 60 insertions at a time to redis
        with self._conn.pipeline() as pipe:
            for i, stock in enumerate(stocks):
                stock_key = f'stock:{stock["name"]}'
                fields = ["code", "name", "open", "high", "low", "close"]
                for field in fields:
                    pipe.hset(stock_key, field, stock[field])
                if (i+1) % 10 == 0:
                    pipe.execute()
            pipe.execute()

    def delete_stock_data(self):
        with self._conn.pipeline() as pipe:
            # delete stock values 60 at a time
            i = 0
            for key in self._conn.scan_iter('stock:*'):
                pipe.delete(key)
                i =+ 1
                if i % 60 == 0:
                    pipe.execute()
            pipe.execute()
            
            # delete search values 60 at a time
            i = 0
            for key in self._conn.scan_iter('search:*'):
                self._conn.delete(key)
                i += 1
                if i % 60 == 0:
                    pipe.execute()
            pipe.execute()


