#A short script to perform timing on the python code 

from timeit import timeit
import numpy as np
from pyennui.geodetic import gravitation_ecef as nanobind_gravitation_ecef
from pyennui.mechanization.ecef import propagation_test as nanobind_repeated_propagation #implementation that loops on C side.

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
propagationCycles = 1000


#C-side loop nanobind
def nanobind_C_loop():
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
            propagationCycles
        )


def warmup_base(numwarmups,func):
    for _ in range(numwarmups):
        func()
    
import timeit
def main():
        
    # Define warmup and benchmark iterations
    warmup_cycles = 1
    benchmark_cycles = 1    

    warmup_base(warmup_cycles,nanobind_C_loop)
    timeit.timeit(nanobind_C_loop,number=benchmark_cycles)
    
    
if __name__ == '__main__':
    main()
