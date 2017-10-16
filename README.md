this project contains the algorithm part of the project. it actually the one part that is not included in the project (we do not make the algorithm packages, now, do we?) but is essential for it to test run and client how-to samples.

the docker contains the python script to run the algorithm, a shared library in c/c++ that executes the algorithm and a generic algorithm runner to launch the python script. we are using ubuntu16 and python3 for the docker image.

components ICD:

    the python script (wrapper) is invoked with the following parameters:
    ---------------------------------------------------------------------
    "python wrapper.py <input file name> <output file name> <progress file name>"

    the python script's job is:
        - read the input from the input file and asynchoniously trigger the c++ algorithem with it
        - periodically call progress() and write the result in the progress file
        - after the c++ algorithem finishes, write 100 in the progress file and write
            the result in the output file


    c/c++ shared library must export the following interface:
    ---------------------------------------------------------
    extern "C" <the algorithem output type> doAlgo(<the algorithem input types>);
    extern "C" double progress();
///////