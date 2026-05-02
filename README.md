# Census Data Analysis Workflow

## Overview

This repository contains a Python-based GIS workflow for analysing census data and visualising spatial patterns across Northern Ireland Data Zones. The script integrates tabular census data with spatial boundary data, calculates key socio-economic indicators such as unemployment rates and long-term health conditions, and produces a series of choropleth maps.

In addition, the workflow includes a spatial accessibility analysis, calculating the distance from each Data Zone to the nearest emergency department using geometric centroids and Euclidean distance. The results are visualised through multiple maps, enhanced with cartographic elements including legends, scale bars, north arrows, and gridlines.

The project demonstrates key GIS and spatial data analysis techniques, including data integration, indicator calculation, spatial analysis, and thematic mapping, implemented within a reproducible Python workflow using libraries such as GeoPandas and Matplotlib.
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
  
Data

A sample dataset is included for demonstration purposes. The workflow is based on census-style data containing socio-economic variables, including employment, unemployment, and health indicators, at the Data Zone level.

In addition to the census data, spatial boundary data for Northern Ireland Data Zones and point data representing emergency department locations are required. These datasets are used to perform spatial analysis and generate thematic maps.

Users can replace the sample data with real datasets from sources such as:

NISRA (Northern Ireland Statistics and Research Agency)
ONS (Office for National Statistics)

All datasets should be placed in the data/ directory before running the script.
Usage

To run the workflow, navigate to the project directory and execute:

python scripts/census_analysis.py

This will run the full analysis, generate summary statistics, and produce map outputs saved in the outputs/ directory.

## Output
The script calculates key socio-economic indicators, including unemployment rates and long-term health conditions, for each Data Zone. Summary statistics are printed to the console for each variable, including measures such as the mean, minimum, maximum, and quartiles.

In addition, the script calculates the distance from each Data Zone to the nearest emergency department, expressed in kilometres, and outputs descriptive statistics for this accessibility measure.

The workflow also generates a series of choropleth maps visualising each variable. These include maps of unemployment rates, long-term health conditions, and distance to emergency departments. The maps are saved as high-quality image files in the outputs/ directory for interpretation and reporting.


