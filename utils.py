def interpolate_distance(df, weight, altitude, temperature):
    subset = df[
        (df["PressureAltitude"] == altitude) &
        (df["OAT"] == temperature)
    ]

    if subset.empty:
        return 0, []  # No matching data at all

    # Get two closest weight entries for interpolation
    closest = subset.iloc[(subset["Weight"] - weight).abs().argsort()[:2]]

    if len(closest) < 2:
        return closest["Distance"].values[0], closest  # Fallback to single point

    x = closest["Weight"].values
    y = closest["Distance"].values

    # Linear interpolation formula
    interpolated = y[0] + (weight - x[0]) * (y[1] - y[0]) / (x[1] - x[0])
    return interpolated, closest


def get_wind_adjustment(wind_knots, weight):
    # Only head/tailwind from OEM reference (approximation)
    if wind_knots == 0:
        return 0
    elif wind_knots > 0:
        # Headwind adjustment: ~220 ft per 10 kt
        return int((wind_knots / 10) * 220)
    else:
        # Tailwind penalty: ~300 ft per 10 kt
        return -int((abs(wind_knots) / 10) * 300)
