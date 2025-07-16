import numpy as np

def interpolate_distance(df, weight, altitude, temperature):
    # Round inputs down to nearest OEM steps
    w_vals = sorted(df["Weight"].unique())
    pa_vals = sorted(df["PressureAltitude"].unique())
    oat_vals = sorted(df["OAT"].unique())

    def find_bounds(val, grid):
        lower = max([v for v in grid if v <= val])
        upper = min([v for v in grid if v >= val])
        return lower, upper

    w0, w1 = find_bounds(weight, w_vals)
    pa0, pa1 = find_bounds(altitude, pa_vals)
    oat0, oat1 = find_bounds(temperature, oat_vals)

    # Get distances from all 8 corners
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
                    return 0, []  # Invalid combo—prevent crash
                cube_points.append(match.iloc[0]["Distance"])

    # Normalize interpolation factors
    xd = (weight - w0) / (w1 - w0) if w1 != w0 else 0
    yd = (altitude - pa0) / (pa1 - pa0) if pa1 != pa0 else 0
    zd = (temperature - oat0) / (oat1 - oat0) if oat1 != oat0 else 0

    # Trilinear interpolation formula
    def lerp(a, b, t): return a + (b - a) * t

    i = lambda a,b,c,d,e,f,g,h: lerp(
        lerp(lerp(a, b, xd), lerp(c, d, xd), yd),
        lerp(lerp(e, f, xd), lerp(g, h, xd), yd),
        zd
    )

    interpolated = i(*cube_points)
    return interpolated, cube_points
