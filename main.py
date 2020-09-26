#!/usr/bin/env python

import asyncio
import json
import websockets

initial_message = json.dumps({'data': {'message': "Let's start"}})
task = 'zeroth'
session = 'valeria'

async def main():
    url = 'wss://sprs.herokuapp.com/{}/{}'.format(task, session)
    async with websockets.connect(url) as ws:
        await ws.send(initial_message)
        print(await ws.recv())
    pass

asyncio.get_event_loop().run_until_complete(main())
