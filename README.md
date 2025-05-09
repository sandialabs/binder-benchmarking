# Binder Benchmarking
Example benchmarking an external code base for binder performance.

 [[TOC]]

## Quick Start
Run benchmarks, for example on Windows
```shell title="build and run benchmarks" linenums="1"
.\scripts\run_all.bat > output_msvc.txt
```
or Linux
```shell title="build and run benchmarks" linenums="1"
./scripts/run_all.sh > output_rhel.txt
```

Optionally install run in docker image
```shell title="build and run docker container" linenums="1"
docker build . -t rhel_sandbox
docker run -it -v ".:/app/binder_LDRD" rhel_sandbox
```

Included scripts both build and run benchmarks. Scripts are included in the ```scripts``` folder, but should be run from the root folder.

In general, we use conan to acquire dependencies and pip to install python packages.

## Organiziation

 * ```scripts``` scripts for building and running benchmarks
 * ```benchmark``` custom code for benchmarking:
 * ```benchmark\exe``` stand-alone application for benchmarking strictly compiled code (no
   scripting languages).
 * ```benchmark\python``` Benchmark python wrappers for ennui
 * ```benchmark\matlab``` Benchmark MATLAB wrapper for ennui
 * ```benchmark\pureClib``` Benchmark python wrappers for a C library not using Eigen
 * ```benchmark\MemoryBenchmarks``` Memory benchmarks
 * ```ennui``` source code to-be benchmarked
 * ```src``` additional code extending ennui for benchmarking purposes. C-loops, etc.
 * ```python``` custom binders for pybind11 and nanobind. Replaces ```ennui\python``` (ignored).
 * ```matlab``` custom binder. Replaces ```ennui\matlab``` (ignored).

## Development hints

For debugging purposes, it may be helpful to verify python module may be built.
```
cmake --preset conan-default -DPYTHON_MODULE=true
```
Once `pre-commit` is installed install the git-hook scripts
```
pre-commit install
```
(optionally) run against all files
```
pre-commit run --all-files
```
Note, only checks files tracked (staged) by git.
