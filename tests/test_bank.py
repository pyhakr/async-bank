import json
import asyncio
import random
from async_bank.bank_client import BankClientProtocol


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


loop = asyncio.get_event_loop()

for message in messages:
    coro = loop.create_connection(lambda: BankClientProtocol(message, loop), '127.0.0.1', 8888)
    loop.run_until_complete(coro)

loop.run_forever()
loop.close()