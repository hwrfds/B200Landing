import numpy as np

def interpolate_distance(df, weight, altitude, temperature):
    # Pivot to 3D grid
    points = df[["Weight", "PressureAltitude", "OAT"]].values
    distances = df["Distance"].values

    # Build input vector
    input_point = np.array([weight, altitude, temperature])

    # Compute weighted distances to each data point
    diffs = points - input_point
    euclidean = np.linalg.norm(diffs, axis=1)

    # Get nearest 4 neighbors for interpolation
    nearest_idx = np.argsort(euclidean)[:4]
    nearest_points = points[nearest_idx]
    nearest_distances = distances[nearest_idx]

    # Inverse distance weighting
    weights = 1 / (euclidean[nearest_idx] + 1e-6)  # avoid division by zero
    weighted_avg = np.dot(weights, nearest_distances) / np.sum(weights)

    return weighted_avg, df.iloc[nearest_idx]


def get_wind_adjustment(wind_knots, weight):
    if wind_knots == 0:
        return 0
    elif wind_knots > 0:
        return int((wind_knots / 10) * 220)  # Headwind bonus
    else:
        return -int((abs(wind_knots) / 10) * 300)  # Tailwind penalty
