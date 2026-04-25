import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar

# Load spatial data
boundaries = gpd.read_file("data/DZ2021.shp")

# Load census data
census = pd.read_csv("data/Census_data.csv")

# Check columns
print(boundaries.columns)
print(census.columns)

# Calculate unemployment rate
census["unemployment_rate"] = (
    census["unemployed"] / (census["employed"] + census["unemployed"])
) * 100

# Join census data to Data Zone boundaries
gdf = boundaries.merge(
    census,
    left_on="DZ2021_cd",
    right_on="DZ_2021_Code"
)

# Plot map
fig, ax = plt.subplots(figsize=(10, 8))

gdf.plot(
    column="unemployment_rate",
    ax=ax,
    legend=True,
    legend_kwds={
        "title": "Unemployment (%)",
        "loc": "lower left",
        "frameon": True
    },
    cmap="OrRd",
    edgecolor="black",
    linewidth=0.2,
    scheme="quantiles"
)

# Title
ax.set_title("Unemployment Rate by Data Zone", fontsize=14)

# Grid lines
ax.set_axis_on()
ax.grid(True, color="grey", linestyle="--", linewidth=0.3, alpha=0.5)

# Scale bar
scalebar = ScaleBar(
    1,
    units="m",
    location="lower right",
    box_alpha=0.3
)
ax.add_artist(scalebar)

# North arrow
ax.annotate(
    "N",
    xy=(0.9, 0.9),
    xytext=(0.9, 0.8),
    arrowprops=dict(facecolor="black", width=3, headwidth=10),
    ha="center",
    va="center",
    fontsize=12,
    xycoords=ax.transAxes
)

# CRS note
ax.text(
    0.01, 0.01,
    "CRS: British National Grid (EPSG:27700)",
    transform=ax.transAxes,
    fontsize=8
)

# Save and show map
plt.savefig("outputs/unemployment_map.png", dpi=300, bbox_inches="tight")
plt.show()
