FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y \
    gcc cmake cmake-curses-gui uuid-dev \
    libssl-dev \
    libsasl2-2 libsasl2-dev \
    swig python3-dev \
    python3-pip \
    libffi-dev \
    wget

RUN mkdir /qpid-proton

WORKDIR /qpid-proton

RUN wget http://mirror.yannic-bonenberger.com/apache/qpid/proton/0.17.0/qpid-proton-0.17.0.tar.gz \
    && tar xzf qpid-proton-0.17.0.tar.gz \
    && cd qpid-proton-0.17.0 \
    && mkdir build \
    && cd build \
    && cmake .. -DCMAKE_INSTALL_PREFIX=/usr -DSYSINSTALL_BINDINGS=ON \
    && make \
    && make install

RUN locale-gen en_US.UTF-8 \
    && export LANG=en_US.UTF-8 \
    && pip3 install bigchaindb_driver

WORKDIR /app
