"""
Census GIS Analysis Workflow

This script performs spatial analysis on Northern Ireland Data Zones by
integrating census data with spatial boundary data. It calculates key
socio-economic indicators, including unemployment rate and long-term
health conditions, and assesses healthcare accessibility by measuring
distance to the nearest emergency department.

Outputs:
- Choropleth map of unemployment rate
- Choropleth map of long-term health conditions
- Choropleth map of distance to nearest emergency department
- Summary statistics printed to the console

Dependencies:
- pandas
- geopandas
- matplotlib
- mapclassify
- matplotlib-scalebar
"""

import os

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar


# Create output folder if it does not already exist
os.makedirs("outputs", exist_ok=True)


# Load spatial boundary data
boundaries = gpd.read_file("data/DZ2021.shp")

# Load census data
census = pd.read_csv("data/Census_data.csv")

# Load emergency department data
hospitals = pd.read_csv("data/emergency departments.csv")


# Convert emergency department coordinates into spatial point data
hospitals_gdf = gpd.GeoDataFrame(
    hospitals,
    geometry=gpd.points_from_xy(hospitals["X"], hospitals["Y"]),
    crs="EPSG:27700"
)


# Calculate unemployment rate as a percentage of the economically active population
census["unemployment_rate"] = (
    census["unemployed"] / (census["employed"] + census["unemployed"])
) * 100


# Join census data to Data Zone boundaries using a common identifier
gdf = boundaries.merge(
    census,
    left_on="DZ2021_cd",
    right_on="DZ_2021_Code"
)


# Ensure both spatial datasets use the same coordinate reference system
assert gdf.crs == hospitals_gdf.crs, "CRS mismatch between boundary and hospital data"


def nearest_distance(point, hospitals):
    """
    Calculate the shortest Euclidean distance from a Data Zone centroid
    to the nearest emergency department.

    Parameters
    ----------
    point : shapely.geometry.Point
        Centroid of a Data Zone polygon.
    hospitals : geopandas.GeoDataFrame
        Emergency department point locations.

    Returns
    -------
    float
        Distance to the nearest emergency department in metres.
    """
    return hospitals.distance(point).min()


# Calculate centroid and nearest emergency department distance
gdf["centroid"] = gdf.geometry.centroid
gdf["dist_to_hospital"] = gdf["centroid"].apply(
    lambda x: nearest_distance(x, hospitals_gdf)
)

# Convert distance from metres to kilometres for readability
gdf["dist_to_hospital_km"] = (gdf["dist_to_hospital"] / 1000).round(1)

# Remove temporary centroid column
gdf = gdf.drop(columns="centroid")


# ---------------------------
# MAP 1: Unemployment rate
# ---------------------------
fig, ax = plt.subplots(figsize=(10, 8))

gdf.plot(
    column="unemployment_rate",
    ax=ax,
    legend=True,
    legend_kwds={
        "title": "Unemployment (%)",
        "loc": "upper left",
        "frameon": True
    },
    cmap="OrRd",
    edgecolor="black",
    linewidth=0.2,
    scheme="quantiles"
)

ax.set_title("Unemployment Rate by Data Zone", fontsize=14)
ax.set_axis_on()
ax.grid(True, linestyle="--", linewidth=0.3, alpha=0.5)

scalebar = ScaleBar(1, units="m", location="lower right")
ax.add_artist(scalebar)

ax.annotate(
    "N",
    xy=(0.9, 0.9),
    xytext=(0.9, 0.8),
    arrowprops=dict(facecolor="black", width=3, headwidth=10),
    ha="center",
    va="center",
    xycoords=ax.transAxes
)

ax.text(
    0.01, 0.01,
    "CRS: British National Grid (EPSG:27700)",
    transform=ax.transAxes,
    fontsize=8
)

plt.savefig("outputs/unemployment_map.png", dpi=300, bbox_inches="tight")
plt.show()


# ---------------------------
# MAP 2: Long-term health conditions
# ---------------------------
fig, ax = plt.subplots(figsize=(10, 8))

gdf.plot(
    column="PC_LTHC",
    ax=ax,
    legend=True,
    legend_kwds={
        "title": "Long-term health conditions (%)",
        "loc": "upper left",
        "frameon": True
    },
    cmap="OrRd",
    edgecolor="black",
    linewidth=0.2,
    scheme="quantiles"
)

ax.set_title("Long-term Health Conditions by Data Zone", fontsize=14)
ax.set_axis_on()
ax.grid(True, linestyle="--", linewidth=0.3, alpha=0.5)

scalebar = ScaleBar(1, units="m", location="lower right")
ax.add_artist(scalebar)

ax.annotate(
    "N",
    xy=(0.9, 0.9),
    xytext=(0.9, 0.8),
    arrowprops=dict(facecolor="black", width=3, headwidth=10),
    ha="center",
    va="center",
    xycoords=ax.transAxes
)

ax.text(
    0.01, 0.01,
    "CRS: British National Grid (EPSG:27700)",
    transform=ax.transAxes,
    fontsize=8
)

plt.savefig("outputs/health_conditions_map.png", dpi=300, bbox_inches="tight")
plt.show()


# ---------------------------
# MAP 3: Distance to nearest emergency department
# ---------------------------
fig, ax = plt.subplots(figsize=(10, 8))

gdf.plot(
    column="dist_to_hospital_km",
    ax=ax,
    legend=True,
    legend_kwds={
        "title": "Distance to ED (km)",
        "loc": "upper left",
        "frameon": True
    },
    cmap="viridis",
    edgecolor="black",
    linewidth=0.2,
    scheme="quantiles"
)

# Overlay emergency department locations as red points
hospitals_gdf.plot(
    ax=ax,
    color="red",
    markersize=25
)

ax.set_title("Distance to Nearest Emergency Department by Data Zone", fontsize=14)
ax.set_axis_on()
ax.grid(True, linestyle="--", linewidth=0.3, alpha=0.5)

scalebar = ScaleBar(1, units="m", location="lower right")
ax.add_artist(scalebar)

ax.annotate(
    "N",
    xy=(0.9, 0.9),
    xytext=(0.9, 0.8),
    arrowprops=dict(facecolor="black", width=3, headwidth=10),
    ha="center",
    va="center",
    xycoords=ax.transAxes
)

ax.text(
    0.01, 0.01,
    "CRS: British National Grid (EPSG:27700)\nRed points = Emergency departments",
    transform=ax.transAxes,
    fontsize=8
)

plt.savefig(
    "outputs/distance_to_emergency_department_map.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# ---------------------------
# Summary statistics
# ---------------------------
print("Unemployment statistics:")
print(gdf["unemployment_rate"].describe())

print("\nHealth condition statistics:")
print(gdf["PC_LTHC"].describe())

print("\nDistance to ED (km) statistics:")
print(gdf["dist_to_hospital_km"].describe())
