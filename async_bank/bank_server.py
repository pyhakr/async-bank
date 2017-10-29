import json
import logging
import asyncio
from async_bank.bank import Bank, BankAccount


"""
Server Streaming Protocol with TCP Transport
The transport is created when create_server is called on event loop
Lib/asyncio/protocols.py

In this implementation, we define what to do when a connection is made,
and when data is received by the server

"""
class BankServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    # work to do when server receives data
    def data_received(self, data):
        transfer_flag = False
        received_message = data.decode()

        if 'account_from' in json.loads(received_message).keys():
            transfer_flag = True

        piggy_bank.message_log_update("{}\n".format(received_message))

        # based on transfer flag, do bank transaction
        # and return account(s) affected and result of transaction
        if transfer_flag:
            account_from, account_to, result = piggy_bank.transact(message=received_message, log=piggy_bank.transact_log)
        else:
            account, result = piggy_bank.transact(message=received_message, log=piggy_bank.transact_log)

        if transfer_flag:
            self.transport.write(json.dumps(account_from.__dict__).encode())
            self.transport.write(json.dumps(account_from.__dict__).encode())
        else:
            if isinstance(account, BankAccount):
                self.transport.write(json.dumps(account.__dict__).encode())
            else:
                self.transport.write(json.dumps(account).encode())

# show asyncio debug events
logging.basicConfig(level=logging.DEBUG)

piggy_bank = Bank()
# create the central execution scheduler
# Lib/asyncio/events.py
loop = asyncio.get_event_loop()
loop.set_debug(True)
# create_server is actually wrapped by @coroutine in Lib/asyncio/coroutines.py
# so the return object is a coroutine generator object that we can pass into
# the event loop to crate the server
coro = loop.create_server(BankServerProtocol, '127.0.0.1', 8888)

# make the coroutine generator into a Future and return
# task for the event loop
# the new task is to create the server
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    # now the loop runs the task to create the server
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()