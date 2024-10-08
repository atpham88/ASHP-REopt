#! /usr/bin/env sh

############## Run scripts ##############
#########################################
python input_processing.py
julia run_all_ASHP_REopt.jl

