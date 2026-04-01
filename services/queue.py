import redis
from rq import Queue

redis_conn = redis.Redis(host="localhost", port=6379, db=0)

high_queue = Queue("high", connection=redis_conn)
medium_queue = Queue("medium", connection=redis_conn)
low_queue = Queue("low", connection=redis_conn)