#!/usr/bin/env python

import asyncio
import websockets
import json


async def producer_handler(websocket, path):
    while True:
        message = await producer()
        await websocket.send(message)

async def producer():
    greeting = {'hello': 'world'}
    json_object = json.dumps(greeting)
    
    return json_object

start_server = websockets.serve(producer_handler, 'localhost', 9999)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
