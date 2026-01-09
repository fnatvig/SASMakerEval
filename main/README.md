# Reproducing the machine-learning evaluation

This directory contains the scripts and instructions required to reproduce the machine-learning evaluation results reported in the paper:

**SASMaker: A Framework for Generating Synthetic IEC 61850 Traffic from Diverse Substation Setups** *(submitted to CIGRE Paris Session 2026)*

The evaluation operates on pre-extracted feature files derived from PCAP data. PCAP files are included for reference and traceability only and are not used directly by the evaluation scripts.

## Prerequisites

- Python 3.10.11

## Environment setup

Create and activate the Python virtual environment using the provided setup scripts.

### Linux / macOS
```bash
chmod +x setup_venv_linux.sh
./setup_venv_linux.sh
source venv/bin/activate
```

### Windows (PowerShell)
```ps
.\setup_venv_win.bat
.\venv\Scripts\Activate.ps1
```

The scripts create a virtual environment and install all required dependencies listed in `requirements.txt`.

## Running the evaluation

Two evaluation scripts are provided, corresponding to different levels of methodological completeness and execution time.

### Long evaluation (feature construction included)

The script `test_long.py` reproduces the full evaluation pipeline starting from raw feature files located in the `data/denial_of_service_reference/xlsx/` and `data/denial_of_service_SASMaker/xlsx` directories. In addition to model training and evaluation, this script constructs the eleven advanced features described in Table 1 of the paper.

This option is intended for readers who wish to inspect or verify the feature-construction process.

To run the long evaluation:

```bash
python test_long.py
```

### Short evaluation (pre-constructed features)

The script `test_short.py` reproduces the reported results using pre-constructed feature files in which the advanced features are already included.

This option is intended for readers who wish to reproduce the reported results with minimal execution time.

To run the short evaluation:

```bash
python test_short.py
```


