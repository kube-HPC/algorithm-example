from socketIO_client import SocketIO, LoggingNamespace


def on_connect():
    print('connect')


def on_disconnect():
    print('disconnect')


def on_reconnect():
    print('reconnect')


def on_initialized_response(*args):
    print('got \"initialized\" response', args)


def on_started_response(*args):
    print('got \"started\" response', args)


def on_finished_response(*args):
    print('got \"finished\" response', args)


def on_stopped_response(*args):
    print('got \"stopped\" response', args)

socketIO = SocketIO('127.0.0.1', 3000, LoggingNamespace)


socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

# Listen
socketIO.on('initialized', on_initialized_response)
socketIO.on('started', on_started_response)
socketIO.on('finished', on_finished_response)
socketIO.on('stopped', on_stopped_response)


print("emitting initialize!")
socketIO.emit('initialize', "initialize data")
socketIO.wait(seconds=4)
print("emitting start!")
socketIO.emit('start', "start data")
socketIO.wait(seconds=4)
print("emitting stop!")
socketIO.emit('stop', "stop data")
socketIO.wait(seconds=4)

'''

# Stop listening
socketIO.off('started')
socketIO.emit('start', "start data")
socketIO.wait(seconds=5)

# Listen only once
socketIO.once('start', on_started_response)
socketIO.emit('start', "start data")  # Activate aaa_response
socketIO.emit('start', "start data")  # Ignore
socketIO.wait(seconds=5)
'''