from concurrent.futures import ThreadPoolExecutor
from ctypes import *
from time import sleep


def printprogress():
    progress_file = open("progress.txt", "w")
    progress_file.truncate(0)
    progress_file.write(str(progress()))
    progress_file.close()


# connect to c++ library
algodll = cdll.LoadLibrary('../libStub/cmake-build-debug/liblibStub.so')
progress = algodll.progress
progress.restype = c_double
doAlgo = algodll.doAlgo
doAlgo.restype = c_int

# start the algorithm async
pool = ThreadPoolExecutor(1)
future = pool.submit(doAlgo, int(60))

while future.running():
    print(progress())
    printprogress()
    sleep(0.5)

# last progress check
print(progress())

if future.done():
    file = open("output.txt", "w")
    file.truncate(0)
    file.write(str(future.result()))
    file.close()

    print("result is ready : " + str(future.result()))


