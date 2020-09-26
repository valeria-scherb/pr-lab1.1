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
        challenge = json.loads(await ws.recv())
        op1 = challenge['data']['operands'][0]
        op2 = challenge['data']['operands'][1]
        op = challenge['data']['operator']
        if op == '+': res = op1 + op2
        elif op == '-': res = op1 - op2
        elif op == '*': res = op1 * op2
        else: res = 0
        await ws.send(json.dumps({'data': {'answer': res}}))
        print(await ws.recv())
    pass

asyncio.get_event_loop().run_until_complete(main())
