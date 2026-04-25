import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# Load spatial data
boundaries = gpd.read_file("data/DZ2021.shp")

# Load census data
census = pd.read_csv("data/Census_data.csv")


# Check columns (important)
print(boundaries.columns)
print(census.columns)


# Calculate unemployment rate
census["unemployment_rate"] = (
    census["unemployed"] / (census["employed"] + census["unemployed"])
) * 100


# Join data (UPDATE column names here)
gdf = boundaries.merge(
    census,
    left_on="DZ2021_cd",  
    right_on="DZ2021_cd"
)


# Plot map
fig, ax = plt.subplots(figsize=(10, 8))

gdf.plot(
    column="unemployment_rate",
    ax=ax,
    legend=True,
    cmap="OrRd",
    scheme="quantiles",
    edgecolor="black",
    linewidth=0.2
)

ax.set_title("Unemployment Rate by Data Zone")
ax.axis("off")

plt.tight_layout()
plt.savefig("outputs/unemployment_map.png")
plt.show()
