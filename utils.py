def interpolate_distance(df, weight, altitude, temperature):
    # Filter dataframe for closest matching PA and temp
    subset = df[
        (df["PressureAltitude"] == altitude) &
        (df["OAT"] == temperature)
    ]
    # Interpolate distance based on weight
    closest = subset.iloc[(subset["Weight"] - weight).abs().argsort()[:2]]
    x = closest["Weight"]
    y = closest["Distance"]
    interpolated = y.iloc[0] + (weight - x.iloc[0]) * (y.iloc[1] - y.iloc[0]) / (x.iloc[1] - x.iloc[0])
    return interpolated

def get_wind_adjustment(wind_knots, weight):
    # Chart-based headwind correction only
    wind = max(min(wind_knots, 30), -30)
    if wind == 0:
        return 0
    if wind > 0:
        return int(220 * (wind / 10))  # Headwind: up to ~660 ft reduction
    else:
        return -int(300 * (abs(wind) / 10))  # Tailwind: up to ~900 ft penalty
