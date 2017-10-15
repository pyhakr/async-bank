import json
import asyncio
from async_bank.bank import Bank, BankAccount


class BankServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        transfer_flag = False
        received_message = data.decode()
        if 'account_from' in json.loads(received_message).keys():
            transfer_flag = True

        piggy_bank.message_log_update("{}\n".format(received_message))
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


piggy_bank = Bank()
loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(BankServerProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()