FROM python:3.6.3
MAINTAINER yehiyam@gmail.com
RUN apt-get update && apt-get install --yes nano python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install aiohttp socketIO_client
RUN mkdir /hkube
COPY ./wrapper /hkube/algoPackage
COPY ./libStub/build/liblibStub.so /hkube/algoPackage/bin/

WORKDIR /hkube/algoPackage/
ENV DLL_PATH "/hkube/algoPackage/bin/liblibStub.so"
CMD ["python3","-u", "wrapper.py"]