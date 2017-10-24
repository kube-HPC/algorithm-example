from concurrent.futures import ThreadPoolExecutor
from ctypes import *
from time import sleep
import json





# read input
with open('./input.json', 'r') as data_file:
    data = json.load(data_file)
secondsToRun = int(data["secondToRun"])
# is works but why ? data is supposed to be in a n inner scope...


# open progress file:
progress_file = open("progress.txt", "w")
progress_file.truncate(0)


def printprogress():
    progress_file.seek(0)
    progress_file.write(str(progress()))

# connect to c++ library
algodll = cdll.LoadLibrary('../libStub/cmake-build-debug/liblibStub.so')
progress = algodll.progress
progress.restype = c_double
doAlgo = algodll.doAlgo
doAlgo.restype = c_int

# start the algorithm async
pool = ThreadPoolExecutor(1)
future = pool.submit(doAlgo, secondsToRun)

while future.running():
    print(progress())
    printprogress()
    sleep(1)

# last progress check + progress file closeing
print(progress())
printprogress()
progress_file.close()

if future.done():
    file = open("output.txt", "w")
    file.truncate(0)
    file.write(str(future.result()))
    file.close()

    print("result is ready : " + str(future.result()))

else:
    file = open("output.txt", "w")
    file.truncate(0)
    file.write("error!!")
    file.close()

