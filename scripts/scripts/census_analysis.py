import pandas as pd


def load_data(file_path):
    """
    Load census dataset from CSV file.
    """
    return pd.read_csv(file_path)


def calculate_unemployment_rate(df):
    """
    Calculate unemployment rate as a percentage.
    """
    df["unemployment_rate"] = df["unemployed"] / (df["employed"] + df["unemployed"]) * 100
    return df


def summary_statistics(df):
    """
    Print summary statistics of unemployment rate.
    """
    print("Mean:", df["unemployment_rate"].mean())
    print("Min:", df["unemployment_rate"].min())
    print("Max:", df["unemployment_rate"].max())


if __name__ == "__main__":
    data = load_data("data/sample_data.csv")
    data = calculate_unemployment_rate(data)
    summary_statistics(data)
