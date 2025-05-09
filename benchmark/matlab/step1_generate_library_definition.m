%% Setup
clear;
this_tic = tic;
printcomment = @(varargin)fprintf('%-60s %5.1fs\n', sprintf(varargin{:}), ...
                                  toc(this_tic));
clear this_tic;
clc;

%% Generate Library Definition
printcomment("generating library definition...")
% Main header file
hFile = fullfile("..","..","matlab","src","mennui.hpp");
% Include path for header files
iPath = [fullfile("..","..","build","matlab","src")]; % "mennui_Export.h"

libFile = fullfile("..","..","build","bin","Release","mennui.lib");

AdditionalCompilerFlags = "/O2 /GL /std:c++17 /Zi /MP /Ob2";
AdditionalLinkerFlags = " /LTCG";

% Matlab changed where "additional compiler flags" go circa '22? Surprise!
MATLAB_VER_BUILD_NO_ARGS = 'R2022a';

if isMATLABReleaseOlderThan(MATLAB_VER_BUILD_NO_ARGS)
    clibgen.generateLibraryDefinition(hFile, IncludePath=iPath, Libraries=libFile, OverwriteExistingDefinitionFiles=true, Verbose=true)
else
    clibgen.generateLibraryDefinition(hFile, IncludePath=iPath, Libraries=libFile, OverwriteExistingDefinitionFiles=true, Verbose=true, AdditionalCompilerFlags=AdditionalCompilerFlags, AdditionalLinkerFlags=AdditionalLinkerFlags)
end

%% Build Interface
printcomment("building interface...")

% Build the interface with specified compiler flags
if isMATLABReleaseOlderThan(MATLAB_VER_BUILD_NO_ARGS)
    build(definemennui, CompilerFlags=AdditionalCompilerFlags, LinkerFlags=AdditionalLinkerFlags)
else
    build(definemennui)
end

addpath('mennui')

printcomment("   done.")