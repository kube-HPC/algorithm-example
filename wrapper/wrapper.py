from concurrent.futures import ThreadPoolExecutor
from ctypes import *
from time import sleep
import json
import os
from socketIO_client import SocketIO, LoggingNamespace


def get_progress(future, progressFunc):
    while future.running():
        progress = progressFunc()
        print(progress)
        outMessage = {'command': 'progress', 'data': {'progress': progress}}
        socketIO.emit('commandMessage', outMessage)
        sleep(1)
    outMessage = {'command': 'done', 'data': {'output':['out1', 'out2']}}
    socketIO.emit('commandMessage', outMessage)


def run_algo():
    # connect to c++ library
    algodll = cdll.LoadLibrary('../libStub/build/liblibStub.so')
    progress = algodll.progress
    progress.restype = c_double
    doAlgo = algodll.doAlgo
    doAlgo.restype = c_int
    # start the algorithm async
    pool = ThreadPoolExecutor(2)
    future = pool.submit(doAlgo, 3)
    progress_future = pool.submit(get_progress, future, progress)


def on_connect():
    print('connect')


def on_disconnect():
    print('disconnect')


def on_reconnect():
    print('reconnect')


def on_command(*args):
    message = args[0]
    command = message["command"]
    data = message["data"]
    print('command: ', command)
    print('data: ', data)
    if command == 'initialize':
        outMessage = {'command': 'initialized'}
        socketIO.emit('commandMessage', outMessage)
    elif command == 'start':
        run_algo()
        outMessage = {'command': 'started'}
        socketIO.emit('commandMessage', outMessage)


socketPort = os.getenv('WORKER_SOCKET_PORT', 3000)
socketIO = SocketIO('127.0.0.1', socketPort)

socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

# Listen
socketIO.on('commandMessage', on_command)

socketIO.wait()
#
# # read input
# with open('./input.json', 'r') as data_file:
#     data = json.load(data_file)
# secondsToRun = int(data["secondToRun"])
# # is works but why ? data is supposed to be in a n inner scope...
#
#
# # open progress file:
# progress_file = open("progress.txt", "w")
# progress_file.truncate(0)
#
#
# def printprogress():
#     progress_file.seek(0)
#     progress_file.write(str(progress()))
#
# # connect to c++ library
# algodll = cdll.LoadLibrary('../libStub/build/liblibStub.so')
# progress = algodll.progress
# progress.restype = c_double
# doAlgo = algodll.doAlgo
# doAlgo.restype = c_int
#
# # start the algorithm async
# pool = ThreadPoolExecutor(1)
# future = pool.submit(doAlgo, secondsToRun)
#
# while future.running():
#     print(progress())
#     printprogress()
#     sleep(1)
#
# # last progress check + progress file closeing
# print(progress())
# printprogress()
# progress_file.close()
#
# if future.done():
#     file = open("output.txt", "w")
#     file.truncate(0)
#     file.write(str(future.result()))
#     file.close()
#
#     print("result is ready : " + str(future.result()))
#
# else:
#     file = open("output.txt", "w")
#     file.truncate(0)
#     file.write("error!!")
#     file.close()
#
