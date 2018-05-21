# ProxyPool
Maintain a dynamic proxy pool using flask and redis

Requirements:
aiohttp
asyncio
flask
redis
bs4

In terminal, run the following command: 
$python start.py

If you find the port already in use, try:

$sudo lsof -i:5000

You will get a pid.Then

$kill pid

Interfaces are provided by flask

At 'localhost:5000/' you will see a welcome page.

At 'localhost:5000/count' you will get the total number of proxies in proxy pool currently

At 'localhost:5000/get' you will get the newest valid proxy in the proxy pool
