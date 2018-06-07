from flask import Flask, g
from bin.redis_client import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    """
    Opens a new redis connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'redis_client'):
        g.redis_client = RedisClient()
    return g.redis_client


@app.route('/')
def index():
    return '<h2>WELCOME! MORTALS!</h2>'


@app.route('/get')
def get_proxy():
    """
    Get a proxy
    """
    conn = get_conn()
    if conn.queue_len() >= 1:
        return conn.pop()
    else:
        return None


@app.route('/count')
def get_total_number():
    """
    Get the count of proxies
    """
    conn = get_conn()
    return str(conn.queue_len())


@app.route('/add/<key>/')
def add_to_pool(key):
    """
    Add a proxy to the left of the pool
    """
    conn = get_conn()
    conn.push_to_left(key)
    return '<h2>Proxy {} added to pool<h2>'.format(key)


@app.route('/clear')
def clear_pool():
    """
    Clear proxy pool
    """
    conn = get_conn()
    conn.flush()
    return '<h2>Pool cleared<h2>'


if __name__ == '__main__':
    app.run()
