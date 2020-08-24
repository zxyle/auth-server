import redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
r = redis.Redis(connection_pool=pool)
