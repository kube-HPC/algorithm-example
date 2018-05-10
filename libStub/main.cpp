#include <iostream>

#include "library.h"
#include <thread>
#include <future>

int doWork()
{
    int ret = doAlgo(3);
    // std::cout<<"algo returned "<< ret<<std::endl;
    return ret;
}
int main(int argc, char **argv)
{
  std::cout<<"Starting"<<std::endl;
  std::future<int> fut = std::async(doWork);
//   std::thread first (doWork); 
  std::this_thread::sleep_for(std::chrono::milliseconds(500));
  stop();
//   first.join();
  int ret = fut.get();
  std::cout<<"algo returned "<< ret<<std::endl;
  std::cout<<"Done"<<std::endl;
  
}