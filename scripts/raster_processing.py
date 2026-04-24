import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling


def reproject_raster(input_path, output_path, dst_crs):
    """
    Reproject a raster dataset to a target coordinate reference system.

    Parameters
    ----------
    input_path : str
        Path to input raster file.
    output_path : str
        Path to save the output raster.
    dst_crs : str
        Target CRS (e.g., 'EPSG:2157').

    Returns
    -------
    None
    """

    # Open source raster
    with rio.open(input_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds
        )

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Create output raster
        with rio.open(output_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rio.band(src, i),
                    destination=rio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest
                )


if __name__ == "__main__":
    # Example usage
    reproject_raster(
        "data/input.tif",
        "outputs/reprojected.tif",
        "EPSG:2157"
    )
