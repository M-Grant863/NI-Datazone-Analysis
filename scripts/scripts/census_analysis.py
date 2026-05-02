import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar

# Load spatial data
boundaries = gpd.read_file("data/DZ2021.shp")

# Load census data
census = pd.read_csv("data/Census_data.csv")

# Load hospital data
hospitals = pd.read_csv("data/emergency departments.csv")

# Convert hospitals to GeoDataFrame
hospitals_gdf = gpd.GeoDataFrame(
    hospitals,
    geometry=gpd.points_from_xy(hospitals["X"], hospitals["Y"]),
    crs="EPSG:27700"
)

# Calculate unemployment rate
census["unemployment_rate"] = (
                                      census["unemployed"] / (census["employed"] + census["unemployed"])
                              ) * 100

# Join census data to boundaries
gdf = boundaries.merge(
    census,
    left_on="DZ2021_cd",
    right_on="DZ_2021_Code"
)


# Distance function
def nearest_distance(point, hospitals):
    return hospitals.distance(point).min()


# Calculate centroid and distance
gdf["centroid"] = gdf.geometry.centroid
gdf["dist_to_hospital"] = gdf["centroid"].apply(
    lambda x: nearest_distance(x, hospitals_gdf)
)

# Convert to km (cleaner for map)
gdf["dist_to_hospital_km"] = (gdf["dist_to_hospital"] / 1000).round(1)

# ---------------------------
# MAP 1: Unemployment
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
# MAP 2: Health conditions
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
# MAP 3: Distance to hospitals (km)
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

# Plot hospitals
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
    "CRS: British National Grid (EPSG:27700)",
    transform=ax.transAxes,
    fontsize=8
)

plt.savefig("outputs/distance_to_emergency_department_map.png", dpi=300, bbox_inches="tight")
plt.show()

# ---------------------------
# Stats output
# ---------------------------
print("Unemployment statistics:")
print(gdf["unemployment_rate"].describe())

print("\nHealth condition statistics:")
print(gdf["PC_LTHC"].describe())

print("\nDistance to ED (km) statistics:")
print(gdf["dist_to_hospital_km"].describe())
