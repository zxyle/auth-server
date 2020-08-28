# databases module

import redis

from utils.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PWD

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PWD)
r = redis.Redis(connection_pool=pool)
