from bin.redis_client import RedisClient
from bin.proxies_getter import ProxiesGetter
import aiohttp
import asyncio
import async_timeout
import time
from bin.config import *


class PoolExtender(object):
    def __init__(self):
        self.conn = RedisClient(host=HOST, port=PORT)
        self.getter = ProxiesGetter()

    def check_pool(self):
        """
        Check if pool reached max capacity
        """
        if self.conn.queue_len() < MAX_PROXIES:
            return True
        return False

    def add_to_pool(self):
        """
        add free proxies to pool
        """
        if self.check_pool():
            for func in self.getter._func:
                proxies = self.getter.get_proxies(func)
                for proxy in proxies:
                    self.conn.push_to_right(proxy)
        else:
            print('Pool reached max capacity')


class PoolTester(object):
    def __init__(self):
        self.conn = RedisClient()

    async def test_single_proxy(self, session, proxy):
        """
        asyncio test if the proxy if valid
        if it is valid, push it to the right of the poll
        otherwise, remove it
        """
        with async_timeout.timeout(10):
            test_proxy = 'http://' + proxy
            print('Testing proxy', proxy)
            try:
                headers = HEADERS
                headers['http'] = test_proxy
                async with session.get(TEST_URL, headers=headers, allow_redirects=False) as response:
                    if response.status == 200:
                        self.conn.push_to_right(proxy)
                        print('Valid proxy', proxy)
                    else:
                        print('Invalid proxy {} Response status {}'.format(proxy, response.status))
            except:
                print('Invalid proxy {} Connection error'.format(proxy))

    async def test_proxies(self, loop):
        """
        asyncio test all proxies in current proxy pool
        """
        proxies = self.conn.get(int(self.conn.queue_len()))
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = [self.test_single_proxy(session, proxy) for proxy in proxies]
            await asyncio.gather(*tasks)


class Schedule(object):
    @staticmethod
    def add_to_pool():
        conn = RedisClient()
        extender = PoolExtender()
        if conn.queue_len() < MIN_PROXIES:
            extender.add_to_pool()
        else:
            print('Enough proxies in pool')

    @staticmethod
    def test_pool(cycle=SLEEP_CYCLE):
        tester = PoolTester()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tester.test_proxies(loop))
        print('SLEEPING ...')
        time.sleep(SLEEP_CYCLE)

    def run(self):
        while True:
            Schedule.add_to_pool()
            Schedule.test_pool()


if __name__ == '__main__':
    s = Schedule()
    s.run()

