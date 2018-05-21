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

$kill [pid]



