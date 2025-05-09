clear;
clc;
addpath('mennui')

p = [1.1150423452941689E+06, -4.8438122981491517E+06, 3.9835202164462707E+06];
% Return argument
g = clibArray('clib.mennui.Double',3);
clib.mennui.geodetic.gravitation_ecef(p,g)

gamma = [-1.7170260919766687E+00, 7.4588665943134185E+00, -6.1541304311837033E+00];
assert(max(abs(g.double - gamma))<1e-14);
disp("success.")