ARG BASE_PRIVATE_REGISTRY=""
FROM ${BASE_PRIVATE_REGISTRY}hkube/python-algorithm-base:v1.0.0
LABEL maintainer="yehiyam@gmail.com"
RUN mkdir /hkube
COPY ./wrapper /hkube/algoPackage
COPY ./libStub/build/liblibStub.so /hkube/algoPackage/bin/

WORKDIR /hkube/algoPackage/
ENV DLL_PATH "/hkube/algoPackage/bin/liblibStub.so"
CMD ["python3","-u", "wrapper.py"]