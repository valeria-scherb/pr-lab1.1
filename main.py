#!/usr/bin/env python

import asyncio
import json
import websockets

initial_message = json.dumps({'data': {'message': "Let's start"}})
task = 'first'
session = 'valeria'
scale = 5
settings = {
    'width': scale, 
    'height': scale,
    'noise': 0.1, 
    'totalSteps': 1,
    'shuffle': False
}

async def main():
    url = 'wss://sprs.herokuapp.com/{}/{}'.format(task, session)
    async with websockets.connect(url) as ws:
        await ws.send(initial_message)
        info = json.loads(await ws.recv())
        print(info)
        await ws.send(json.dumps({'data': settings}))
        templ = json.loads(await ws.recv())
        print(templ)
    pass

asyncio.get_event_loop().run_until_complete(main())
