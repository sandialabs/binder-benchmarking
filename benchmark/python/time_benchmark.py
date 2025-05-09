# A short script to perform timing on the python code
import sys
import os
from timeit import timeit
from collections import OrderedDict
import numpy as np
from pyennui.mechanization.ecef import fwd_pva_S03 as nanobind_propagation
from pyennui.geodetic import gravitation_ecef as nanobind_gravitation_ecef
from pyennui.mechanization.ecef import (
    propagation_test as nanobind_repeated_propagation,
)  # implementation that loops on C side.

from pyennui_pybind11.mechanization.ecef import fwd_pva_S03 as pybind11_propagation
from pyennui_pybind11.geodetic import gravitation_ecef as pybind11_gravitation_ecef
from pyennui_pybind11.mechanization.ecef import (
    propagation_test as pybind11_repeated_propagation,
)  # implementation that loops on C side.

# Pure-python implementation
sys.path.append(os.path.join(".", "ennui", "python", "reference"))

# import pure_ennui
from pure_ennui.mechanization.ecef import fwd_pva_S03 as numpy_propagation


WhiteHouse_mean_prop = {
    "prior": {
        "position": np.array(
            [1.115042345294169e06, -4.843812298149152e06, 3.983520216446271e06]
        ),
        "velocity": np.array(
            [1.700252783993267e00, 5.799253612971604e00, -7.143100966293305e00]
        ),
        "attitude": np.matrix(
            [
                [
                    -1.689390579588263e-01,
                    -4.453768089569571e-01,
                    -8.792605374627603e-01,
                ],
                [8.000355898459490e-01, -5.830041132072308e-01, 1.415954058693114e-01],
                [-5.756758199506289e-01, -6.795187282384265e-01, 4.548094637289362e-01],
            ]
        ),
    },
    "specific_force": np.array(
        [-2.351012554013630e00, 1.857770394070348e00, 1.940270045514844e01]
    ),
    "angular_rate": np.array(
        [6.941949163919531e00, -3.383664771751461e00, 7.607424972048551e00]
    ),
    "dt": 1.000000000000000e-03,
    "posterior": {
        "position": np.array(
            [1.115042346984841e06, -4.843812292346284e06, 3.983520209304588e06]
        ),
        "velocity": np.array(
            [1.681091028114939e00, 5.806482921506987e00, -7.140263743663021e00]
        ),
        "attitude": np.matrix(
            [
                [
                    -1.753142992423087e-01,
                    -4.501584286525450e-01,
                    -8.755696920258544e-01,
                ],
                [7.960624873695160e-01, -5.880875442140073e-01, 1.429599823146225e-01],
                [-5.792662709706455e-01, -6.719452577802820e-01, 4.614543941305069e-01],
            ]
        ),
    },
}

# Pre-allocate output
posterior = {
    "position": np.empty((3)),
    "velocity": np.empty((3)),
    "attitude": np.empty((3, 3)),
}


# Pure-python nanobind
def nanobind_python_loop(propagationCycles):
    for _ in range(propagationCycles):
        gamma = nanobind_gravitation_ecef(WhiteHouse_mean_prop["prior"]["position"])
        nanobind_propagation(
            WhiteHouse_mean_prop["prior"]["position"],
            WhiteHouse_mean_prop["prior"]["velocity"],
            WhiteHouse_mean_prop["prior"]["attitude"],
            gamma,
            WhiteHouse_mean_prop["specific_force"],
            WhiteHouse_mean_prop["angular_rate"],
            WhiteHouse_mean_prop["dt"],
            posterior["position"],
            posterior["velocity"],
            posterior["attitude"],
        )


# C-side loop nanobind
def nanobind_C_loop(propagationCycles):
    nanobind_repeated_propagation(
        WhiteHouse_mean_prop["prior"]["position"],
        WhiteHouse_mean_prop["prior"]["velocity"],
        WhiteHouse_mean_prop["prior"]["attitude"],
        WhiteHouse_mean_prop["specific_force"],
        WhiteHouse_mean_prop["angular_rate"],
        WhiteHouse_mean_prop["dt"],
        posterior["position"],
        posterior["velocity"],
        posterior["attitude"],
        propagationCycles,
    )


# Pure-python pybind11
def pybind11_python_loop(propagationCycles):
    for _ in range(propagationCycles):
        gamma = pybind11_gravitation_ecef(WhiteHouse_mean_prop["prior"]["position"])
        pybind11_propagation(
            WhiteHouse_mean_prop["prior"]["position"],
            WhiteHouse_mean_prop["prior"]["velocity"],
            WhiteHouse_mean_prop["prior"]["attitude"],
            gamma,
            WhiteHouse_mean_prop["specific_force"],
            WhiteHouse_mean_prop["angular_rate"],
            WhiteHouse_mean_prop["dt"],
            posterior["position"],
            posterior["velocity"],
            posterior["attitude"],
        )


# C-side loop pybind11
def pybind11_C_loop(propagationCycles):
    pybind11_repeated_propagation(
        WhiteHouse_mean_prop["prior"]["position"],
        WhiteHouse_mean_prop["prior"]["velocity"],
        WhiteHouse_mean_prop["prior"]["attitude"],
        WhiteHouse_mean_prop["specific_force"],
        WhiteHouse_mean_prop["angular_rate"],
        WhiteHouse_mean_prop["dt"],
        posterior["position"],
        posterior["velocity"],
        posterior["attitude"],
        propagationCycles,
    )


# Naive Numpy/Python implementation
def numpy_python_loop(propagationCycles):
    for _ in range(propagationCycles):
        gamma = pybind11_gravitation_ecef(WhiteHouse_mean_prop["prior"]["position"])
        # not really good to have a mix of generating results from different types.
        # However, no time and this is what is used in the example
        position, velocity, attitude = numpy_propagation(
            WhiteHouse_mean_prop["prior"]["position"],
            WhiteHouse_mean_prop["prior"]["velocity"],
            WhiteHouse_mean_prop["prior"]["attitude"],
            gamma,
            WhiteHouse_mean_prop["specific_force"],
            WhiteHouse_mean_prop["angular_rate"],
            WhiteHouse_mean_prop["dt"],
        )


def warmup_base(numwarmups, func, propagationCycles):
    for _ in range(numwarmups):
        func(propagationCycles)


def main():
    # Define warmup and benchmark iterations
    warmup_cycles = 25
    benchmark_cycles = 1000
    propagation_cycle_values = [10, 100, 1000, 10000]

    function_list = [
        "nanobind_python_loop",
        "nanobind_C_loop",
        "pybind11_python_loop",
        "pybind11_C_loop",
        "numpy_python_loop",
    ]
    print("BENCHMARK TABLE: ennui_python")
    print(
        "BENCHMARK HEADER: propagationCycles, "
        + ", ".join(f"{value}" for value in function_list)
    )

    # Run benchmarks and collect results
    for propagationCycles in propagation_cycle_values:
        for _ in range(10):
            results = OrderedDict.fromkeys(function_list)
            # print(f"\nRunning benchmarks for Propagation cycles: {propagationCycles}")

            # print("Starting Nanobind Python Loop")
            warmup_base(warmup_cycles, nanobind_python_loop, propagationCycles)
            results["nanobind_python_loop"] = (
                timeit(
                    lambda: nanobind_python_loop(propagationCycles),
                    number=benchmark_cycles,
                )
                / benchmark_cycles
            )

            # print("Starting Nanobind C Loop")
            warmup_base(warmup_cycles, nanobind_C_loop, propagationCycles)
            results["nanobind_C_loop"] = (
                timeit(
                    lambda: nanobind_C_loop(propagationCycles), number=benchmark_cycles
                )
                / benchmark_cycles
            )

            # print("Starting Pybind11 Python Loop")
            warmup_base(warmup_cycles, pybind11_python_loop, propagationCycles)
            results["pybind11_python_loop"] = (
                timeit(
                    lambda: pybind11_python_loop(propagationCycles),
                    number=benchmark_cycles,
                )
                / benchmark_cycles
            )

            # print("Starting Pybind11 C Loop")
            warmup_base(warmup_cycles, pybind11_C_loop, propagationCycles)
            results["pybind11_C_loop"] = (
                timeit(
                    lambda: pybind11_C_loop(propagationCycles), number=benchmark_cycles
                )
                / benchmark_cycles
            )

            # print("Starting Numpy Python Loop")
            warmup_base(warmup_cycles, numpy_python_loop, propagationCycles)
            # RUN FEWER TIMES : python is much slower
            results["numpy_python_loop"] = timeit(
                lambda: numpy_python_loop(propagationCycles),
                number=int(0.01 * benchmark_cycles),
            ) / int(0.01 * benchmark_cycles)

            # Check populated everything...
            assert len(results.keys()) == len(
                function_list
            ), "results do not match function_list, did you add a function?"
            for key, val in list(results.items()):
                assert val is not None, "Missing values for function: " + key

            # # Print results
            # for name, result in results.items():
            #     print(f"{name:<25}: {result:.6e}")

            # Print results as row
            print(
                f"BENCHMARK: {propagationCycles:6d}, "
                + ", ".join(f"{value:.5e}" for value in results.values())
            )


if __name__ == "__main__":
    main()
