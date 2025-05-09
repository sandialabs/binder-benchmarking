%% Time Benchmark
%
% Time compiled code
%
%% Setup
clear;
this_tic = tic;
printcomment = @(varargin)fprintf('%-60s %5.1fs\n', sprintf(varargin{:}), ...
                                  toc(this_tic));
clear this_tic;

clc;
addpath('mennui')

%% Example data
prior = struct(...
    'position', [1.115042345294169e06, -4.843812298149152e06, 3.983520216446271e06],...
    'velocity', [1.700252783993267e00, 5.799253612971604e00, -7.143100966293305e00],...
    'attitude', [...
    -1.689390579588263e-01,-4.453768089569571e-01,-8.792605374627603e-01;...
    8.000355898459490e-01, -5.830041132072308e-01, 1.415954058693114e-01;...
    -5.756758199506289e-01, -6.795187282384265e-01, 4.548094637289362e-01],...
    'specific_force', [-2.351012554013630e00, 1.857770394070348e00, 1.940270045514844e01],...
    'angular_rate', [6.941949163919531e00, -3.383664771751461e00, 7.607424972048551e00],...
    'dt', 1.000000000000000e-03);


posterior = struct(...
    'position', [1.115042346984841e06, -4.843812292346284e06, 3.983520209304588e06],...
    'velocity', [1.681091028114939e00, 5.806482921506987e00, -7.140263743663021e00],...
    'attitude', [...
    -1.753142992423087e-01,-4.501584286525450e-01,-8.755696920258544e-01; ...
    7.960624873695160e-01, -5.880875442140073e-01, 1.429599823146225e-01; ...
    -5.792662709706455e-01, -6.719452577802820e-01, 4.614543941305069e-01]);

%% Repackage arguments
p = prior.position;
v = prior.velocity;
a = prior.attitude;
sf = prior.specific_force;
dtheta = prior.angular_rate;
dt = prior.dt;

% Get gravity
g = clibArray('clib.mennui.Double',3);
clib.mennui.geodetic.gravitation_ecef(p,g)

% Return argument
p_post = clibArray('clib.mennui.Double',3);
v_post = clibArray('clib.mennui.Double',3);
a_post = clibArray('clib.mennui.Double',9);

%% Time
warmup_cycles = 25;
propagation_cycles_list = [10, 100, 1000, 10000]; % List of propagation cycles to test

% Generators producing function handles to perform fixed number of propagation cycles
%
% Loop in MATLAB
gen_fctn_mat_loop = @(cycles) @() matlab_loop(cycles, p, v, a, g, sf, dtheta, dt, p_post, v_post, a_post);
% Loop in C
gen_fctn_c_loop = @(cycles) @() clib.mennui.mechanization.ecef.propagation_test(p, v, a.', sf, dtheta, dt, p_post, v_post, a_post, cycles);


for i = 1:length(propagation_cycles_list)
    for n = 1:10
        propagation_cycles = propagation_cycles_list(i);
        
        fprintf('Testing with propagation_cycles = %d\n', propagation_cycles);
        
        % Time MATLAB loop
        fctn = gen_fctn_mat_loop(propagation_cycles);
        time_and_print(fctn, "Matlab loop", propagation_cycles, warmup_cycles, printcomment);
        
        % Time C loop
        fctn = gen_fctn_c_loop(propagation_cycles);
        time_and_print(fctn, "C loop", propagation_cycles, warmup_cycles, printcomment);
    end
end

%% Validate results
% Validate results against prior data. Ensures return arguments make sense.
fctn = gen_fctn_mat_loop(1);
fctn();
% Don't validate C loop > 1 step. :)
validate(p_post,v_post,a_post,posterior, printcomment)


%% Utility Functions

function warmup_base(numwarmups,fctn)
    % warmup function
    for n = 1:numwarmups
        fctn();
    end
end

function matlab_loop(propagationCycles,p,v,a,g,sf,dtheta,dt,p_post,v_post,a_post)
    % loop in matlab. no argument checking for speed...
    for n = 1:propagationCycles
        clib.mennui.mechanization.ecef.fwd_pva_S03(p,v,a.',g,sf,dtheta,dt,p_post,v_post,a_post);
    end
end

function t = time_and_print(fctn,title,propagation_cycles,warmup_cycles,printcomment)
    % Time function and print results
    arguments
        % function to test
        fctn function_handle
        % text label for printing
        title string
        % number of propagation cycles in loop
        propagation_cycles {mustBePositive, mustBeInteger}
        % number of warmup cycles before timing
        warmup_cycles {mustBePositive, mustBeInteger}
        printcomment function_handle
    end
    
    printcomment(title)
    printcomment("   warmup")

    warmup_base(warmup_cycles,fctn)
    printcomment("   timeit: %d propagation cycles",propagation_cycles)
    t = timeit(fctn,0);
    printcomment("   result: %.5e sec.",t)
end

function validate(position,velocity,attitude,expected,printcomment)
    arguments
        position clib.array.mennui.Double
        velocity clib.array.mennui.Double
        attitude clib.array.mennui.Double
        expected struct
        printcomment function_handle
    end

    % Validate return arguments
    printcomment("Check results:")
    assert(max(abs(position.double - expected.position))<1e-9)
    assert(max(abs(velocity.double - expected.velocity))<1e-14)
    assert(max(abs(reshape(attitude.double,3,3) - expected.attitude),[],'all')<1e-14)
    printcomment('   success.')
end