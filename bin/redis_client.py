import redis
from bin.config import HOST, PORT, PASSWORD
from bin.error import PoolEmptyError


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT, password=PASSWORD):
        if password:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        # get the left n proxies
        proxies = self._db.lrange('proxies', 0, count-1)
        proxies = [proxy.decode('utf-8') for proxy in proxies]
        self._db.ltrim('proxies', count, -1)
        return proxies

    def push_to_right(self, proxy):
        # add proxy to the right
        self._db.rpush('proxies', proxy)

    def push_to_left(self, proxy):
        # add proxy to the left
        self._db.lrem('proxies', proxy)
        self._db.lpush('proxies', proxy)

    def pop(self):
        # pop out the right most proxy
        try:
            return self._db.rpop('proxies').decode('utf-8')
        except PoolEmptyError:
            return None

    def queue_len(self):
        # get the number of proxies in pool
        return self._db.llen('proxies')

    def flush(self):
        # delete all proxies
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.random())
    print(str(conn.queue_len()))
