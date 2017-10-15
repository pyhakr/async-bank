import asyncio
import random
from async_bank.bank_client import BankClientProtocol

transact_id = random.randrange(500000, 6000000)

loop = asyncio.get_event_loop()
message = {"id": transact_id,
           "account": None,
           "action": "open",
           "funds": 50}

coro = loop.create_connection(lambda: BankClientProtocol(message, loop),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()