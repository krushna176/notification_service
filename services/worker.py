
import os
import redis
from rq import Worker, Queue

redis_conn = redis.Redis() 

if __name__ == "__main__":
    worker = Worker(
        [Queue("high"), Queue("medium"), Queue("low")],
        connection=redis_conn
    )
    worker.work()