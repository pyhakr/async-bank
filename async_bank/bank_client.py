import json
import asyncio

"""
Client Streaming Protocol with TCP Transport
The transport is created when create_connection is called on event loop
Lib/asyncio/protocols.py

In this implementation, we define what to do when a connection is made,
and when data is received by the client

"""
class BankClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    # called by the transport when socket connection is made
    # transport is created by the event loop create_connection
    # which pairs the transport and this protocol
    def connection_made(self, transport):
        transport.write(json.dumps(self.message).encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))


    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()