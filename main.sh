#!/bin/bash

# Trace and scan
./prefix_trace.sh

# Extract route info
./collect_route.sh

# Extract feature info
./collect_feature.sh
