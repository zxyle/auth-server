# databases module

import redis

# Use default configuration: localhost, port: 6379, db:0, passwd:None
pool = redis.ConnectionPool()
r = redis.Redis(connection_pool=pool)
