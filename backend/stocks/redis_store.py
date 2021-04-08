import json
import redis

class RedisStore:
    def __init__(self, connection_pool):
        self._conn = redis.Redis(connection_pool=connection_pool)
        self._fields = [
            "code", "name", "open", "high", "low", "close"
        ]  

    def get_stock_data(self, match):
        search_key = f"search:{match}*"
        if self._conn.exists(search_key):
            stocks = self._conn.get(search_key)
            stocks = json.loads(stocks)
        else:
            stocks = []
            for key in self._conn.scan_iter(f'stock:{match}*', 1000):
                result = self._conn.hgetall(key) 
                stock = {
                    "code": int(result[b'code']),
                    "name": result[b'name'].decode("utf-8"),
                    "open": float(result[b'open']),
                    "high": float(result[b'high']),
                    "low": float(result[b'low']),
                    "close": float(result[b'close'])
                }
                stocks.append(stock)
            self._conn.set(search_key, json.dumps(stocks), ex=300)
        
        return stocks

    def insert_stock_data(self, stocks):
        for stock in stocks:
            stock_key = f'stock:{stock["name"]}'
            fields = ["code", "name", "open", "high", "low", "close"]
            for field in fields:
                self._conn.hset(stock_key, field, stock[field])

    def delete_stock_data(self):
        for key in self._conn.scan_iter('stock:*'):
            self._conn.delete(key)
        for key in self._conn.scan_iter('search:*'):
            self._conn.delete(key)


