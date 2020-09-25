#!/usr/bin/env python

import asyncio
import websockets

async def main():
    async with websockets.connect('wss://sprs.herokuapp.com/zeroth/valeria') as ws:
        await ws.send('{ "data": { "message": "Let\'s start" } }')
        print(await ws.recv())
    pass

asyncio.get_event_loop().run_until_complete(main())
