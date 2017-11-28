#include "library.h"
#include <iostream>

#include <chrono>
#include <thread>


static volatile double progressPercent = 0;
static volatile bool shouldStopFlag = false;
int doAlgo( int seconds)
{
    //we will have to make a concurrency safe progress mechanism
    //progressPercent = 0;
    progressPercent = 0;
    double quanta = 100/seconds;

    for (int i = 0 ; i< seconds ; i++)
    {
        if (shouldStopFlag){
            shouldStopFlag = false;
            progressPercent = 100;
            return -1;
        }
        //std::cout << "dd- " << i <<" of " << seconds << ".    progress: "<< progressPercent << "   q=" << quanta <<std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(350));
        progressPercent += quanta;
        std::cout << "iterate";
    }

    printf("wait has ended! :)");

    progressPercent = 100;
    return  42;//2*seconds;
}

double progress()
{
    return progressPercent;
}

bool stop(){
    shouldStopFlag = true;
    return shouldStopFlag;
}