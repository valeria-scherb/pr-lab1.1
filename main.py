#!/usr/bin/env python

import asyncio
import json
import websockets

initial_message = json.dumps({'data': {'message': "Let's start"}})
ready_message = json.dumps({'data': {'message': "Ready"}})
bye_messsage = json.dumps({'data': {'message': 'Bye'}})
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
digits = {}

async def main():
    url = 'wss://sprs.herokuapp.com/{}/{}'.format(task, session)
    async with websockets.connect(url) as ws:
        await ws.send(initial_message)
        info = json.loads(await ws.recv())
        # print(info)
        n = scale * info['data']['height']
        m = scale * info['data']['width']
        await ws.send(json.dumps({'data': settings}))
        templ = json.loads(await ws.recv())
        digits = templ['data']
        for step in range(0, total):
            await ws.send(ready_message)
            problem = json.loads(await ws.recv())
            x = problem['data']['matrix']
            # for r in x:
            #     line = ''
            #     for el in r:
            #         line += '# ' if el == 1 else '. '
            #     print(line)
            probs = {}
            for k in digits.keys():
                gk = digits[k]
                mult = 1
                for i in range(0, n):
                    for j in range(0, m):
                        mult *= p ** (x[i][j] ^ gk[i][j])
                        mult *= q ** (1 ^ x[i][j] ^ gk[i][j])
                probs[k] = mult
            sprobs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
            # print(sprobs)
            answer, certainity = sprobs[0]
            print(step, '|', answer, ':', certainity)
            cs = problem['data']['currentStep']
            await ws.send(json.dumps({'data': {'step': cs, 'answer': answer}}))
            step_res = json.loads(await ws.recv())
            print(step_res)
        await ws.send(bye_messsage)
        summary = json.loads(await ws.recv())
        print(summary)

asyncio.get_event_loop().run_until_complete(main())
