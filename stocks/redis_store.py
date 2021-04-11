import json
import redis

class RedisStore:
    """
    Class responsible for establishing connection to Redis, inserting and
    fetching data operations to and from Redis.
    """
    def __init__(self, connection_pool):
        """
        Establish Redis Connection from Connection Pool
        """
        self._conn = redis.Redis(connection_pool=connection_pool)

    def _parse_stock_list(self, stocks):
        """
        Function responsible for parsing data returned by pipeline
        """
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
        """
        Function responsible for getting stocks data from Redis according to given match term 
        """
        search_key = f"search:{match}*"

        # Check if search result already exists in Redis
        if self._conn.exists(search_key):
            search_result = self._conn.get(search_key)
            search_result = json.loads(search_result)
        else:
            search_result = []
            # Get the stocks data through pipeline, 60 at a time
            with self._conn.pipeline() as pipe:
                i = 0
                for key in self._conn.scan_iter(f'stock:{match}*', 1000):
                    pipe.hgetall(key) 
                    i += 1
                    # Get data 60 at a time through pipeline
                    if i % 60 == 0:
                        results = pipe.execute()
                        search_result += self._parse_stock_list(results)
                results = pipe.execute()
                search_result += self._parse_stock_list(results)
            
            # Store the search result in Redis for quicker fetching in future 
            self._conn.set(search_key, json.dumps(search_result), ex=300)
        
        return search_result

    def insert_stock_data(self, stocks):
        """
        Insert stock data into Redis via pipeline 60 at a time through a pipeline
        """
        # insert 60 stock values at a time
        with self._conn.pipeline() as pipe:
            for i, stock in enumerate(stocks):
                stock_key = f'stock:{stock["name"]}'
                fields = ["code", "name", "open", "high", "low", "close"]                
                
                # Data is stored using hset operation
                for field in fields:
                    pipe.hset(stock_key, field, stock[field])
                
                # 60 = 6 fields in one loop x 10 loops
                if (i+1) % 10 == 0:
                    pipe.execute()
            pipe.execute()

    def delete_stock_data(self):
        """
        Function used to delete stock and search data from Redis 60 at a time through a pipeline
        """
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
                pipe.delete(key)
                i += 1
                if i % 60 == 0:
                    pipe.execute()
            pipe.execute()


