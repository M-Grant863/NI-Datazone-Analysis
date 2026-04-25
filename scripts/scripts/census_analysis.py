import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def load_spatial_data(shapefile_path):
    """
    Load ward or census boundary data from a shapefile.

    Parameters
    ----------
    shapefile_path : str
        Path to the input shapefile.

    Returns
    -------
    GeoDataFrame
        Spatial boundary data.
    """
    return gpd.read_file(shapefile_path)


def load_census_data(csv_path):
    """
    Load census attribute data from a CSV file.
    """
    return pd.read_csv(csv_path)


def calculate_unemployment_rate(df):
    """
    Calculate unemployment rate as a percentage of the economically active population.
    """
    df["unemployment_rate"] = (
        df["unemployed"] / (df["employed"] + df["unemployed"])
    ) * 100
    return df


def join_census_to_boundaries(boundaries, census, boundary_id, census_id):
    """
    Join census data to spatial boundary data using a common ID field.
    """
    return boundaries.merge(census, left_on=boundary_id, right_on=census_id)


def plot_unemployment_map(gdf, output_path):
    """
    Create a choropleth map showing unemployment rate.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    gdf.plot(
        column="unemployment_rate",
        ax=ax,
        legend=True,
        scheme="Quantiles",
        cmap="OrRd",
        edgecolor="black",
        linewidth=0.2
    )

    ax.set_title("Unemployment Rate by Ward", fontsize=14)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()


if __name__ == "__main__":

    boundaries = load_spatial_data("data/wards.shp")
    census = load_census_data("data/sample_data.csv")

    census = calculate_unemployment_rate(census)

    joined_data = join_census_to_boundaries(
        boundaries,
        census,
        boundary_id="ward",
        census_id="ward"
    )

    plot_unemployment_map(
        joined_data,
        "outputs/unemployment_map.png"
    )
