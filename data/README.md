## Data

The datasets used in this project are not included in the repository due to file size and licensing considerations.

This workflow is based on census-style data combined with spatial boundary data for Northern Ireland Data Zones, along with point data representing emergency department locations.

---

## Data Sources

To reproduce the workflow, users should obtain the following datasets:

* Census data (e.g. employment, unemployment, and health indicators)
* Data Zone boundary shapefiles (Northern Ireland)
* Emergency department location data (point coordinates)

These datasets may be obtained from:

* Course practical materials
* Official sources such as NISRA (Northern Ireland Statistics and Research Agency)
* ONS (Office for National Statistics)

---

## Instructions

Place all input datasets in this `data/` directory before running the script. The expected file structure is:

* `DZ2021.shp` (Data Zone boundaries)
* `Census_data.csv` (socio-economic data)
* `emergency departments.csv` (hospital locations)

Ensure that all datasets use the same coordinate reference system (British National Grid, EPSG:27700) to allow accurate spatial analysis.

If file paths differ, they may need to be updated within the script before execution.
