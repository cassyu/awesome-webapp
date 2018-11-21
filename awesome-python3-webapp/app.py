#!
#-*- coding:utf-8-*-
"""async web application"""
import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')

async def init(event_loop):
    #循环参数已被弃用
    app = web.Application()
    app.router.add_route('GET', '/', index)
    app_runner = web.AppRunner(app)
    srv = await loop.create_server(app_runner.app._make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

#获取eventloop
loop = asyncio.get_event_loop()
#执行coroutine
loop.run_until_complete(init(loop))
loop.run_forever()
