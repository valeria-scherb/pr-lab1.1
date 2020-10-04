#!/usr/bin/env python

import asyncio
import json
import websockets

from recognizer import Recognizer

initial_message = json.dumps({'data': {'message': "Let's start"}})
ready_message = json.dumps({'data': {'message': "Ready"}})
bye_message = json.dumps({'data': {'message': 'Bye'}})
task = 'first'
session = 'valeria'
scale = 5
p = 0.4
q = 1.0 - p
total = 10
settings = {
    'width': scale, 
    'height': scale,
    'noise': p,
    'totalSteps': total,
    'shuffle': False
}


async def main():
    url = 'wss://sprs.herokuapp.com/{}/{}'.format(task, session)
    async with websockets.connect(url) as ws:
        await ws.send(initial_message)
        info = json.loads(await ws.recv())
        # print(info)
        rec = Recognizer()
        rec.set_noise_prob(p)
        n = scale * info['data']['height']
        m = scale * info['data']['width']
        rec.set_size(n, m)
        await ws.send(json.dumps({'data': settings}))
        templates = json.loads(await ws.recv())
        digits = templates['data']
        for k in digits.keys():
            rec.remember(k, digits[k])
        for step in range(0, total):
            await ws.send(ready_message)
            problem = json.loads(await ws.recv())
            x = problem['data']['matrix']
            answer = rec.recognize(x)
            print(step, '|', answer)
            cs = problem['data']['currentStep']
            await ws.send(json.dumps({'data': {'step': cs, 'answer': answer}}))
            step_res = json.loads(await ws.recv())
            print(step_res)
        await ws.send(bye_message)
        summary = json.loads(await ws.recv())
        print(summary)

asyncio.get_event_loop().run_until_complete(main())
