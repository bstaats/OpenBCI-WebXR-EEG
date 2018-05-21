#!/usr/bin/env python

import asyncio
import websockets
import json
import csvReader
import logging
import get_freq_int


def process_openbci_data():
    merge_data = get_freq_int.get_preprocessed_data()
    for row in merge_data:
        for key in row.keys():
            logging.error(key)
            yield row.get(key, None)

merge_data = process_openbci_data()
# this is for the data from freqcenter and intensity data
#merge_data = csvReader.run()



async def producer_handler(websocket, path):
    while True:
        message = producer()
        logging.info(message)
        await websocket.send(message)

def producer():
    global merge_data

    try:
        json_data = json.dumps(next(merge_data))
        logging.error('looping through data')     
    except StopIteration:
        merge_data = 0
        logging.error('reset data loop')
        merge_data = csvReader.run()
        json_data = json.dumps(next(merge_data))
    return json_data

    

start_server = websockets.serve(producer_handler, 'localhost', 9999)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
