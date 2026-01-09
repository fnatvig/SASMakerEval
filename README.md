# SASMaker Evaluation

This repository contains code for reproducing some of the results in the paper: 

SASMaker: A Framework for Generating Synthetic IEC 61850 Traffic from Diverse Substation Setups (submitted to CIGRE Paris Session 2026)

## Overview 

The purpose of this repository is to support reproducibility of the machine-learning experiments used to evaluate datasets generated with SASMaker. It includes scripts for data preprocessing, model training, and evaluation, as well as fixed random seeds and configuration files corresponding to the reported results.

This repository does **not** contain the SASMaker framework itself. SASMaker is maintained in a separate repository and is used here only as a data source.

## Repository scope

Included:

Included:
- Pre-generated PCAP files used in the evaluation
  - One dataset generated using SASMaker
  - A reference dataset from Biswas et al. (see full reference in `main/data/denial_of_service_reference/README.md`)
- Feature extraction code operating on the provided PCAPs
- Machine-learning training and evaluation scripts
- Experiment configurations and fixed random seeds

Excluded:
- The SASMaker framework and all dataset generation components
- Power-system or IEC 61850 traffic simulation code
- PCAP parsing utilities or raw packet decoding logic

## Dependencies

All Python dependencies required to reproduce the experiments are listed in `main/requirements.txt`.


## Reproducing the results

Step-by-step instructions for reproducing the reported results are provided in the `main/` subfolder.