#!/usr/bin/env python

import asyncio
import json
import websockets

initial_message = json.dumps({'data': {'message': "Let's start"}})

async def main():
    async with websockets.connect('wss://sprs.herokuapp.com/zeroth/valeria') as ws:
        await ws.send(initial_message)
        print(await ws.recv())
    pass

asyncio.get_event_loop().run_until_complete(main())
