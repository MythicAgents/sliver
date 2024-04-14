# TODO: figure out if the devcontainer can simply point to the Dockerfile within Payload_Type (but not start main.py?)
FROM itsafeaturemythic/mythic_python_go:latest

RUN apt-get update
RUN apt-get install -y git gnupg software-properties-common openssh-client

WORKDIR /Mythic/

RUN git clone --depth 1 https://github.com/grpc/grpc
RUN cd grpc && git submodule update --init
RUN cd grpc && pip install -r requirements.txt
RUN cd grpc && pip uninstall -y protobuf
RUN cd grpc && pip install protobuf==3.20.*
RUN cd grpc && GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True GRPC_PYTHON_BUILD_WITH_CYTHON=1 pip install .

# RUN pip install sliver-py
RUN git clone --depth 1 https://github.com/spenceradolph/sliver-py.git
RUN cd sliver-py && git submodule update --init
RUN pip install -e sliver-py

RUN pip install mythic_container==v0.4.18
RUN pip install tabulate
