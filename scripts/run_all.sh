#!/bin/bash

# Run the first script
echo "Running clang benchmark..."
./scripts/runbenchmarks_clang.sh

# Run next script
echo "Running gcc benchmark..."
./scripts/runbenchmarks_gcc.sh

# Run next script
echo "Running pureClib clang script..."
./scripts/runbenchmarks_pureClib_clang.sh


# Run next script
echo "Running pureClib gcc script..."
./scripts/runbenchmarks_pureClib_gcc.sh

echo "   All scripts completed."
echo "done."
exit 0
