from concurrent.futures import ThreadPoolExecutor
from ctypes import *
from time import sleep
import os

import botocore
from socketIO_client import SocketIO
import boto3
import csv

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
    basePath = os.path.dirname(os.path.realpath(__file__));
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
    stop = algodll.stop
    stop.restype = c_bool
    stop()

def on_connect():
    print('connect')


def on_disconnect():
    print('disconnect')


def on_reconnect():
    print('reconnect')

def on_init(*args):
    message = args[0]
    print('Got init with message',message)
    data = message["data"]
    input = data["input"][0]
    downloadIfNeeded(input)

    outMessage = {'command': 'initialized'}
    socketIO.emit('initialized', outMessage)

def on_start(*args):
    run_algo()
    outMessage = {'command': 'started'}
    socketIO.emit('started', outMessage)

def on_stop(*args):
    stop_algo()

def downloadIfNeeded(input,fileKey="input_file_path"):
    if input[fileKey].startswith('http'):
        input[fileKey] = downloadFromS3(input[fileKey])
    if input[fileKey].endswith('csv'):
        d = []
        with open(input[fileKey]) as csvFile:
            csvReader = csv.DictReader(csvFile)
            for line in csvReader:
                d.append(line)
        for line in d:
            downloadIfNeeded(line,'SessionFilePath')
        with open(input[fileKey], 'w') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, d[0].keys())
            w.writeheader()
            for line in d:
                w.writerow(line)

def downloadFromS3(url):
    try:
        segments = url.rpartition('/')
        filename = segments[2]
        segments=segments[0].rpartition('/')
        backetname = segments[2]
        bucket=s3_client.Bucket(backetname)
        localfilename = os.path.join(localStoragePath,filename)
        bucket.download_file(filename, localfilename)
        return localfilename
    except botocore.exceptions.ClientError as e:
        print("Error",e)
    


print('starting algorithm-example')

key=os.getenv('AWS_ACCESS_KEY_ID',"")
secret=os.getenv('AWS_SECRET_ACCESS_KEY',"")
s3EndpointUrl=os.getenv('S3_ENDPOINT_URL',"")
localStoragePath=os.getenv('LOCAL_STORAGE_PATH','./localStoragePath')
if not os.path.exists(localStoragePath):
    os.makedirs(localStoragePath)

if s3EndpointUrl:

    s3_client_session = boto3.session.Session(
        aws_access_key_id=key,
        aws_secret_access_key=secret,
    )
    s3_client = s3_client_session.resource(
        service_name='s3',
        endpoint_url=s3EndpointUrl
        )
    # url = 'http://10.32.10.24:9000/minio/apak/test1.csv'
    #
    # try:
    #     # parsedUrl = urlparse(url);
    #     segments = url.rpartition('/')
    #     filename = segments[2]
    #     segments=segments[0].rpartition('/')
    #     backetname = segments[2]
    #     bucket=s3_client.Bucket(backetname)
    #     bucket.download_file(filename, filename)
    # except botocore.exceptions.ClientError as e:
    #     print("Error",e)
    
    # for bucket in s3_client.buckets.all():
    #     print(bucket.name)
    # auth=S3Auth(key,secret,s3EndpointUrl)
    # r = requests.get('http://10.32.10.24:9000/minio/apak/test1.csv', auth=auth)
    print('s3 init')
else:
    print('s3 not init')

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
