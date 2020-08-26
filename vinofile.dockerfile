FROM ubuntu:18.04
USER root
WORKDIR /
RUN useradd -ms /bin/bash openvino && \
    chown openvino -R /home/openvino
ARG DEPENDENCIES="apt-utils \
                  autoconf \
                  sudo \
                  vim \
                  automake \
                  build-essential \
                  cmake \
                  cpio \
                  curl \
                  gnupg2 \
                  libdrm2 \
                  libglib2.0-0 \
                  lsb-release \
                  libgtk-3-0 \
                  libtool \
                  python-pip \
                  python3-pip \
                  python3-setuptools \
                  python3-dev \
                  libpython3.6 \
                  udev \
                  unzip \
                  git"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install lxml PyYAML requests numpy networkx==2.3 defusedxml

ARG DOWNLOAD_LINK="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/16803/l_openvino_toolkit_p_2020.4.287.tgz"
WORKDIR /tmp
ENV INSTALL_DIR /opt/intel/openvino
RUN curl -LOJ "${DOWNLOAD_LINK}" && \
    tar -xzf ./*.tgz && \
    cd l_openvino_toolkit* && \
    sed -i 's/decline/accept/g' silent.cfg && \
    ./install.sh -s silent.cfg && \
    rm -rf /tmp/*

#install openvino dependencies
WORKDIR $INSTALL_DIR/install_dependencies
RUN ./install_openvino_dependencies.sh
RUN ./install_NEO_OCL_driver.sh
RUN usermod -a -G video root

#install additional openvino dependencies
WORKDIR /opt/intel/openvino/deployment_tools/demo
RUN ./demo_security_barrier_camera.sh || exit 0
RUN ./demo_security_barrier_camera -d GPU || exit 0

RUN pip3 install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN pip3 install absl-py numpy onnx pybind11

WORKDIR /mlperf
RUN apt-get install libglib2.0-dev
RUN git clone --recurse-submodules https://github.com/mlperf/inference.git
WORKDIR /mlperf/inference/loadgen
RUN pip3 install wheel && CFLAGS="-std=c++14 -O3" python3 setup.py bdist_wheel
RUN pip3 install --force-reinstall dist/mlperf_loadgen-0.5a0-cp36-cp36m-linux_x86_64.whl
RUN python3 demos/py_demo_single_stream.py

WORKDIR /code
COPY ./gradient ./
RUN pip3 install -r requirement.txt
#WORKDIR /opt/intel/openvino/deployment_tools/tools/model_downloader/
#RUN python3 downloader.py --all
#RUN python3 converter.py --all --mo /opt/intel/openvino/deployment_tools/model_optimizer/mo.py || exit 0


#ARG DATASET_DOWNLOAD_LINK=<Link to dataset project>
#RUN git clone $DATASET_DOWNLOAD_LINK

RUN cat /root/.bashrc > tmp && echo 'source /opt/intel/openvino/bin/setupvars.sh' > /root/.bashrc && \
    cat tmp >> /root/.bashrc && rm tmp

CMD ["/bin/sh"]