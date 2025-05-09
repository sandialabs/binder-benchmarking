import sys
import os
import timeit

# Import custom libraries which may not be on path...
# ---------------------------------------------------

# Allow user to specify additional folder to add to path (libs)
current_directory = os.getcwd()  # Get the current working directory
print(f"The current working directory is: {current_directory}")
print("Running script name : ", sys.argv[0])
N = len(sys.argv)
print("Number of input arguments : ", N)

if N == 2:
    folder_to_add = sys.argv[1]
    print("adding path: ", folder_to_add)
    sys.path.append(folder_to_add)
elif N != 1:
    raise ValueError("Expecting one path or less")

# Flake8 doesn't detect usage from __main__. Is there a better way?
import rk4_integration_nanobind  # noqa: F401, E402
import rk4_integration_pybind11  # noqa: F401, E402

# Define local functions for benchmarking
# ---------------------------------------------------


def benchmark_rk4_integration_nanobind(num_steps):
    setup_code = """
from __main__ import rk4_integration_nanobind
"""
    test_code = """
rk4_integration_nanobind.rk4_integration(0.0, 0.0, (20.0 - 0.0) / {}, 20.0)
""".format(
        num_steps
    )

    time = timeit.timeit(stmt=test_code, setup=setup_code, number=1000) / 1000
    return time


def benchmark_rk4_integration_pybind11(num_steps):
    setup_code = """
from __main__ import rk4_integration_pybind11
"""
    test_code = """
rk4_integration_pybind11.rk4_integration(0.0, 0.0, (20.0 - 0.0) / {}, 20.0)
""".format(
        num_steps
    )

    time = timeit.timeit(stmt=test_code, setup=setup_code, number=1000) / 1000
    return time


def benchmark_rk4_integration_single_step_nanobind(num_steps):
    setup_code = """
from __main__ import rk4_integration_nanobind
"""
    test_code = """
x = 0.0
y = 0.0
h = (20.0 - 0.0) / {}
for _ in range({}):
    y = rk4_integration_nanobind.rk4_integration_single_step(x, y, h)
    x += h
""".format(
        num_steps, num_steps
    )

    time = timeit.timeit(stmt=test_code, setup=setup_code, number=1)
    return time


def benchmark_rk4_integration_single_step_pybind11(num_steps):
    setup_code = """
from __main__ import rk4_integration_pybind11
"""
    test_code = """
x = 0.0
y = 0.0
h = (20.0 - 0.0) / {}
for _ in range({}):
    y = rk4_integration_pybind11.rk4_integration_single_step(x, y, h)
    x += h
""".format(
        num_steps, num_steps
    )

    time = timeit.timeit(stmt=test_code, setup=setup_code, number=1)
    return time


# Run benchmarks
# ---------------------------------------------------

num_steps_list = [1000, 10000, 100000, 1000000]

print("Running Python benchmarks: ")
print(
    "Ordering: pybind11_Cloop, pybind11_pythonloop, nanobind_Cloop, nanobind_pythonloop"
)
function_list = (
    "benchmark_rk4_integration_pybind11",
    "benchmark_rk4_integration_single_step_pybind11",
    "benchmark_rk4_integration_nanobind",
    "benchmark_rk4_integration_single_step_nanobind",
)
print("BENCHMARK TABLE: rk4_python")
print(
    "BENCHMARK HEADER: propagationCycles, "
    + ", ".join(f"{value}" for value in function_list)
)
for num_steps in num_steps_list:
    for i in range(10):
        time1 = benchmark_rk4_integration_pybind11(num_steps)
        time2 = benchmark_rk4_integration_single_step_pybind11(num_steps)
        time3 = benchmark_rk4_integration_nanobind(num_steps)
        time4 = benchmark_rk4_integration_single_step_nanobind(num_steps)

        # Print results:
        # print("Number of steps: {}".format(num_steps))
        # print("{:.6e} , {:.6e} , {:.6e} , {:.6e}".format(time1,time2,time3,time4))
        print(
            f"BENCHMARK: {num_steps:7d}, "
            + ", ".join(f"{value:.5e}" for value in (time1, time2, time3, time4))
        )
