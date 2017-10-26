from socketIO_client import SocketIO
import json

def on_connect():
    print('connect')


def on_disconnect():
    print('disconnect')


def on_reconnect():
    print('reconnect')


def on_initialize_response(*args):
    print('got \"initialize\" response', args)
    socketIO.emit('initialized')


def on_command(*args):
    message = args[0]
    command = message["command"]
    data = message["data"]
    print('command: ', command)
    print('data: ', data)
    if command == 'initialize':
        outmessage = {'command':'initialized'}
        socketIO.emit('commandMessage', outmessage)
    elif command == 'start':
        outmessage = {'command': 'started'}
        socketIO.emit('commandMessage', outmessage)


def on_start_response(*args):
    print('got \"start\" response', args)
    socketIO.emit('started')



def on_finished_response(*args):
    print('got \"finished\" response', args)


def on_stopped_response(*args):
    print('got \"stopped\" response', args)


socketIO = SocketIO('127.0.0.1', 3000)


socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

# Listen
socketIO.on('commandMessage', on_command)
socketIO.on('start', on_start_response)

socketIO.wait()
#
# print("emitting initialize!")
# socketIO.emit('initialize', "initialize data")
# socketIO.wait(seconds=4)
# print("emitting start!")
# socketIO.emit('start', "start data")
# socketIO.wait(seconds=4)
# print("emitting stop!")
# socketIO.emit('stop', "stop data")
# socketIO.wait(seconds=4)
