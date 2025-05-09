#FROM redhat/ubi9
#FROM cee-gitlab.sandia.gov:4567/innersource/docker/ubi9:latest
FROM quay.io/pypa/manylinux_2_34_x86_64

RUN yum update -y
RUN yum install -y python3-devel llvm-toolset cmake pip gdb valgrind nano
RUN pip install --no-input numpy conan pyperf
RUN pip install --no-input --target=/usr/lib/python3.9/site-packages pybind11 nanobind

RUN conan remote list
RUN conan profile detect

WORKDIR /app/binder_LDRD/
