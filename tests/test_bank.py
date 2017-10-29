import json
import asyncio
import random
import logging
from async_bank.bank_client import BankClientProtocol

# show asyncio debug events
logging.basicConfig(level=logging.DEBUG)

# create some test messages to cover all bank actions
messages = [
    {"id": random.randrange(500000, 6000000), "account": 345, "action": "open", "funds": 50},
    {"id": random.randrange(500000, 6000000), "account": 789, "action": "open", "funds": 100},
    {"id": random.randrange(500000, 6000000), "account": 345, "action": "withdraw", "funds": 25},
    {"id": random.randrange(500000, 6000000), "account": 345, "action": "deposit", "funds": 100},
    {"id": random.randrange(500000, 6000000), "account": 345, "action": "withdraw", "funds": 25},
    {"id": random.randrange(500000, 6000000), "account": 345, "action": "check", "funds": None},
    {"id": random.randrange(500000, 6000000), "account": 345, "action": "check", "funds": None},
    {"id": random.randrange(500000, 6000000), "account_from": 345, "account_to": 789, "action": "transfer", "funds": 50},
    {"id": random.randrange(500000, 6000000), "account": 345, "action": "check", "funds": None},
    {"id": random.randrange(500000, 6000000), "account": 789, "action": "check", "funds": None}
]


# create the central execution scheduler
# Lib/asyncio/events.py
loop = asyncio.get_event_loop()
loop.set_debug(True)

# we make separate connection for each message
# this simulates multiple client connections

for message in messages:
    # create_connection is actually wrapped by @coroutine in Lib/asyncio/coroutines.py
    # so the return object is a coroutine generator object that we can pass into
    # the event loop to crate the connection
    # when the connection is made on the transport (tcp socket)
    # the connection_made method is called on the BankClientProtocol
    # because create_connection needs a callable object, we use lambda
    coro = loop.create_connection(lambda: BankClientProtocol(message, loop), '127.0.0.1', 8888)

    # make the coroutine generator into a Future and create task for the event loop
    # the new task is to create the connection
    # BankClientProtocol.connection_made will be called
    loop.run_until_complete(coro)

loop.run_forever()
loop.close()