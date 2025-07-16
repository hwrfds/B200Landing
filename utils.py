import numpy as np

def interpolate_distance(df, weight, altitude, temperature):
    # Extract unique sorted grid points
    w_vals = sorted(df["Weight"].unique())
    pa_vals = sorted(df["PressureAltitude"].unique())
    oat_vals = sorted(df["OAT"].unique())

    def find_bounds(val, grid):
        lower = max([v for v in grid if v <= val])
        upper = min([v for v in grid if v >= val])
        return lower, upper

    # Find bounding box
    w0, w1 = find_bounds(weight, w_vals)
    pa0, pa1 = find_bounds(altitude, pa_vals)
    oat0, oat1 = find_bounds(temperature, oat_vals)

    # Pull all 8 bounding cube values
    cube_points = []
    for w in (w0, w1):
        for pa in (pa0, pa1):
            for oat in (oat0, oat1):
                match = df[
                    (df["Weight"] == w) &
                    (df["PressureAltitude"] == pa) &
                    (df["OAT"] == oat)
                ]
                if match.empty:
                    return 0, []  # Safety fallback
                cube_points.append(match.iloc[0]["Distance"])

    # Normalize interpolation factors
    xd = (weight - w0) / (w1 - w0) if w1 != w0 else 0
    yd = (altitude - pa0) / (pa1 - pa0) if pa1 != pa0 else 0
    zd = (temperature - oat0) / (oat1 - oat0) if oat1 != oat0 else 0

    # Lerp helper
    def lerp(a, b, t): return a + (b - a) * t

    # Trilinear interpolation
    interpolated = lerp(
        lerp(lerp(cube_points[0], cube_points[1], xd),
             lerp(cube_points[2], cube_points[3], xd), yd),
        lerp(lerp(cube_points[4], cube_points[5], xd),
             lerp(cube_points[6], cube_points[7], xd), yd),
        zd
    )

    return interpolated, cube_points


def get_wind_adjustment(wind_knots, weight):
    if wind_knots == 0:
        return 0
    elif wind_knots > 0:
        return int((wind_knots / 10) * 220)  # Headwind reduction
    else:
        return -int((abs(wind_knots) / 10) * 300)  # Tailwind penalty
