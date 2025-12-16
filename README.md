# Millikan-Automator

[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md) [![Chinese](https://img.shields.io/badge/Language-中文-gray.svg)](README_CN.md)

**Note: This project is a modified version based on the original repository by [ricktjwong](https://github.com/ricktjwong/millikan).**

### Key Modifications
- **Documentation**: Added Chinese documentation (`README_CN.md`).
- **Code Adjustments**: Updated file paths for better compatibility.
- **Feature Enhancements**: Added trajectory visualization in `transform.py` to inspect particle movements.
- **Parameter Tuning**: Adjusted parameters in `extract.py` and `transform.py` for specific experimental conditions (e.g., voltage settings, detection thresholds).

## Recognising charged oil drops in Millikan's oil drop experiment

Millikan's oil drop experiment involves the measurement of several terminal velocities of oil droplets at various conditions to be able to eventually deduce its charge. One would usually look through the microscope, keeping track of one oil droplet at a time, and record its velocity from observation the change in position over time.

This process is time consuming and tedious. These Python scripts were written to:

1. Recognise the oil droplets through the microscope.
2. Calculate velocities of oil droplets through the microscope.

These were implemented using [trackpy](https://github.com/soft-matter/trackpy), a Python implementation of the Crocker-Grier algorithm which helps with particle tracking across frames.

## Prerequisites

- Python 3.6 or higher
- Libraries: `trackpy`, `numpy`, `pandas`, `matplotlib`, `pims`, `slicerator`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/UbiStaff/Millikan-Automator.git
   cd Millikan-Automator
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv millikan_env
   source millikan_env/bin/activate
   # On Windows use: millikan_env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install trackpy numpy pandas matplotlib pims slicerator
   ```

## Usage

### 1. Extract Data
Run `python/extract.py` to read the sample MOV file from `test_video`. This script recognises the oil droplets, tracks them, and extracts the important data into a CSV file at `csvs/extract.csv`.

> **Note:** This might take a while as processing is done on most frames in the video.

```bash
python python/extract.py
```

### 2. Transform Data
After extraction is done, run `python/transform.py`. This filters the oil droplets which did not change direction upon the removal of the electric field, calculates useful fields such as velocity, and saves the result into `csvs/transformed.csv`.

```bash
python python/transform.py
```
