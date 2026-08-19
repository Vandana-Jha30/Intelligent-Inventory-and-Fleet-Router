import math


EARTH_RADIUS_KM = 6371.0


def calculate_distance(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float
) -> float:

    lat1 = math.radians(latitude_1)
    lon1 = math.radians(longitude_1)

    lat2 = math.radians(latitude_2)
    lon2 = math.radians(longitude_2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return EARTH_RADIUS_KM * c