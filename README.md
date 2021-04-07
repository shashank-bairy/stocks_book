# Stocks Book

Todo:

- get data from redis cache and display in index.html [done]
- celery job to run on weekdays at 6pm or 18:00
- search operation and get data [done]
- have state for search stirng -> to extract easily [done]
- redis pipline to insert values
- delete values before inserting [done]
- implement search using redis cache [done]
- add expiry to search data
- django connection pool [done]
- display records not found when search is not successful

eval "for \_,k in ipairs(redis.call('keys','stock:\*')) do redis.call('del',k) end" 0

HGET WHIRLPOOL name
HGET WHIRLPOOL code
HGETALL WHIRLPOOL
SCAN 0 MATCH stock:WI\* COUNT 5000 (remove \)
KEYS \* (list all keys, remove \)

redis-cli
redis-server

As per Redis 4.0.0, HMSET is considered deprecated. Please use HSET in new code.
scan_iter

https://stackoverflow.com/questions/22255589/get-all-keys-in-redis-database-with-python
https://stackabuse.com/working-with-redis-in-python-with-django/
https://stackoverflow.com/questions/21975228/redis-python-how-to-delete-all-keys-according-to-a-specific-pattern-in-python

name
repo has jules
release/sonar scan has jules
if relese/sonar which branch has it
property in jules file -cron job

https://stackoverflow.com/questions/12967107/managing-connection-to-redis-from-python
