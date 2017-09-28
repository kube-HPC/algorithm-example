# Docker file for a slim Ubuntu-based Python3 image

FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# Set the working directory to /app
WORKDIR /wrapper

# Copy the current directory contents into the container at /app
ADD ../libStub/cmake-build-debug/liblibStub.so /libStub/cmake-build-debug
ADD ../wrapper/wrapper.py /wrapper

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD ["", "app.py"]