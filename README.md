# Raster Reprojection Workflow

## Overview
This repository contains a Python workflow for reprojecting raster datasets into a specified coordinate reference system (CRS). The script uses the Rasterio library to transform raster data while maintaining spatial integrity.

## Installation

Create the environment using:
```bash
conda env create -f environment.yml
conda activate raster-workflow
```

## Dependencies

- rasterio
- numpy
- matplotlib

## Data

The input raster data is not included due to file size.

You can use:
- Course-provided datasets  
- Or any GeoTIFF raster file  

Place your input file in the `data/` folder.

## Usage

Run the script using:
```bash
python scripts/raster_processing.py
```
