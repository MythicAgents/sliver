FROM itsafeaturemythic/mythic_python_base:latest as builder

RUN apt-get update
RUN apt-get install -y git gnupg software-properties-common

WORKDIR /Mythic/

RUN git clone --depth 1 https://github.com/grpc/grpc
RUN cd grpc && git submodule update --init
RUN cd grpc && pip install -r requirements.txt
RUN cd grpc && pip uninstall -y protobuf
RUN cd grpc && pip install protobuf==3.20.*
RUN cd grpc && GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True GRPC_PYTHON_BUILD_WITH_CYTHON=1 pip install .
RUN cd grpc && python setup.py bdist_wheel --dist-dir=/grpc_wheel

COPY ["requirements.txt", "requirements.txt"]
RUN python3 -m pip wheel --wheel-dir /other_wheels -r requirements.txt

###########################################################
###########################################################

FROM itsafeaturemythic/mythic_python_base:latest

COPY --from=builder /other_wheels /other_wheels
COPY --from=builder /grpc_wheel /grpc_wheel

RUN pip install --no-cache /other_wheels/*
RUN pip install --no-cache /grpc_wheel/*
