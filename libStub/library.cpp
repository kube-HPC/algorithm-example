#include "library.h"
#include <iostream>
#include <fstream>
#include <unistd.h>

#include <chrono>
#include <thread>


static long h = 0;
static volatile double progressPercent = 0;
int doAlgo( int seconds)
{
    //we will have to make a concurrency safe progress mechanism
    //progressPercent = 0;

    double quanta = 100/seconds;

    for (int i = 0 ; i< seconds ; i++)
    {
        //std::cout << "dd- " << i <<" of " << seconds << ".    progress: "<< progressPercent << "   q=" << quanta <<std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        progressPercent += quanta;
    }

    progressPercent = 100;


    return  2*seconds;


}

double progress()
{
    return progressPercent;
}