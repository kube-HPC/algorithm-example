from concurrent.futures import ThreadPoolExecutor
from ctypes import *
from time import sleep
import json
import os
import sys
from socketIO_client import SocketIO
from random import *


def get_progress(future, progressFunc):
    while future.running():
        progress = progressFunc()
        print(progress)
        outMessage = {'command': 'progress', 'data': {'progress': progress}}
        print('sending message: ',outMessage)
        socketIO.emit('progress', outMessage)
        sleep(1)

    if future.result() == -1:
        res = 'execution halt requested'
        outMessage = {'command': 'stopped', 'data': {'output': res}}
        socketIO.emit('stopped', outMessage)
    else:
        res = future.result()
        out_message = {'command': 'done', 'data': {'output': res}}
        socketIO.emit('done', out_message)


def run_algo():
    # connect to c++ library
    basePath = os.path.dirname(os.path.realpath(__file__))
    dllPath = os.getenv('DLL_PATH', '../libStub/build/liblibStub.so')
    print('dllPath: ', dllPath)
    if not os.path.isabs(dllPath):
        dllPath = os.path.join(basePath,dllPath)
    print('dllPath: ',dllPath)
    algodll = cdll.LoadLibrary(dllPath)
    progress = algodll.progress
    progress.restype = c_double
    doAlgo = algodll.doAlgo
    doAlgo.restype = c_int
    # start the algorithm async
    pool = ThreadPoolExecutor(2)
    future = pool.submit(doAlgo, 1)
    progress_future = pool.submit(get_progress, future, progress)

def stop_algo():
    print('got stop command')
    # connect to c++ library
    basePath = os.path.dirname(os.path.realpath(__file__));
    dllPath = os.getenv('DLL_PATH', '../libStub/build/liblibStub.so')
    print('dllPath: ', dllPath)
    if not os.path.isabs(dllPath):
        dllPath = os.path.join(basePath, dllPath)
    print('dllPath: ', dllPath)
    algodll = cdll.LoadLibrary(dllPath)
    print('1')    
    stop = algodll.stop
    print('2')    
    stop.restype = c_bool
    print('3')    
    stop()
    print('4')    
    

def on_connect():
    print('connect')


def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_init(*args):
    message = args[0]
    outMessage = {'command': 'initialized'}
    socketIO.emit('initialized', outMessage)

def on_start(*args):
    run_algo()
    outMessage = {'command': 'started'}
    socketIO.emit('started', outMessage)

def on_stop(*args):
    stop_algo()

def on_exit(*args):
    code=0
    print ("args:",args[0])
    if (args and args[0]):
        code=args[0].get('exitCode',0)
    print('Got exit command. Exiting with code',code)
    sys.exit(code)

print('starting algorithm-example')
socketPort = os.getenv('WORKER_SOCKET_PORT', 3000)
socketIO = SocketIO('127.0.0.1', socketPort)

socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

# Listen
# socketIO.on('commandMessage', on_command)
socketIO.on('initialize', on_init)
socketIO.on('start', on_start)
socketIO.on('stop', on_stop)
socketIO.on('exit',on_exit)
socketIO.wait()

