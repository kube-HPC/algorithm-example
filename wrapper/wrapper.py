from concurrent.futures import ThreadPoolExecutor
from ctypes import *
from time import sleep
import json
import os
from socketIO_client import SocketIO


def get_progress(future, progressFunc):
    while future.running():
        progress = progressFunc()
        print(progress)
        outMessage = {'command': 'progress', 'data': {'progress': progress}}
        socketIO.emit('commandMessage', outMessage)
        sleep(1)
    res = 'execution halt requested' if (future.result() == -1) else future.result()
    out_message = {'command': 'done', 'data': {'output': res}}
    socketIO.emit('commandMessage', out_message)


def run_algo():
    # connect to c++ library
    basePath = os.path.dirname(os.path.realpath(__file__));
    dllPath = os.getenv('DLL_PATH', '../libStub/cmake-build-debug/liblibStub.so')
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
    future = pool.submit(doAlgo, 10)
    progress_future = pool.submit(get_progress, future, progress)

def stop_algo():
    # connect to c++ library
    dllPath = os.getenv('DLL_PATH', '../libStub/cmake-build-debug/liblibStub.so')
    algodll = cdll.LoadLibrary(dllPath)
    stop = algodll.stop
    stop.restype = c_bool
    stop()

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
    elif command == 'stop':
        stop_algo()
        outMessage = {'command': 'stopped'}
        socketIO.emit('commandMessage', outMessage)


socketPort = os.getenv('WORKER_SOCKET_PORT', 3000)
socketIO = SocketIO('127.0.0.1', socketPort)

socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

# Listen
socketIO.on('commandMessage', on_command)
socketIO.wait()

# ctypes defines a number of primitive C compatible data types:
#
# ctypes type	C type	Python type
# c_bool	_Bool	bool (1)
# c_char	char	1-character string
# c_wchar	wchar_t	1-character unicode string
# c_byte	char	int/long
# c_ubyte	unsigned char	int/long
# c_short	short	int/long
# c_ushort	unsigned short	int/long
# c_int	int	int/long
# c_uint	unsigned int	int/long
# c_long	long	int/long
# c_ulong	unsigned long	int/long
# c_longlong	__int64 or long long	int/long
# c_ulonglong	unsigned __int64 or unsigned long long	int/long
# c_float	float	float
# c_double	double	float
# c_longdouble	long double	float
# c_char_p	char * (NUL terminated)	string or None
# c_wchar_p	wchar_t * (NUL terminated)	unicode or None
# c_void_p	void *	int/long or None






















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
