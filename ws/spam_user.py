import asyncio
import websockets

from config import Settings

import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())


async def people_list(websocket):
    await websocket.send('?')

    people_str = await websocket.recv()
    people = people_str.split(', ')
    people.remove(Settings.WS_SPAM_USER)
    return people


async def register_spamer(websocket):
    await websocket.send(Settings.WS_SPAM_USER)
    await websocket.send('?')
    _rs = False
    while not _rs:

        people_str = await websocket.recv()
        people = people_str.split(', ')
        if Settings.WS_SPAM_USER in people:
            _rs = True
    return _rs


async def spammer():
    # establish connection to ws server
    async with websockets.connect(uri=f"ws://{Settings.WS_HOST}:{Settings.WS_PORT}") as websocket:
        # registering our spamer in ws server
        _rs = await register_spamer(websocket)
        try:
            while _rs:
                # receive list of users
                people = await people_list(websocket)
                if len(people) > 0:
                    for name in people:
                        # check if user exited
                        if name in await people_list(websocket):
                            await websocket.send(f'{name}: Привет {name}! {Settings.SPAM_MESSAGE} ')
                        # update our working list
                        else:
                            people.remove(name)
                await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Exception occured in spamer: {e}")

loop = asyncio.get_event_loop()
loop.run_until_complete(spammer())
