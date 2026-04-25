# Census Data Analysis Workflow

## Overview

This repository contains a Python workflow for analysing census data and calculating unemployment rates at ward level. The script demonstrates basic data processing and statistical analysis techniques inspired by course practical exercises. This approach reflects common workflows in GIS and spatial data analysis, where tabular data is processed and analysed to derive meaningful indicators.

## Installation

Create the environment using:
```bash
conda env -f environment.yml
conda activate census-workflow
```

## Dependencies
- pandas
- numpy
- matplotlib
  
## Data

A sample dataset is included for demonstration purposes.

The workflow is based on census-style data containing employment and unemployment figures at ward level.

Users can replace the sample data with real datasets from sources such as:
- NISRA
- ONS
Place the dataset in the `data/` folder before running the script.

## Usage
Run the script using:
```bash
python scripts/census_analysis.py
```
## Output
The script will calculate unemployment rates for each ward and print summary statistics (mean, minimum, and maximum) to the console.


