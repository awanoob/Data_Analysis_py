import math
import numpy as np

from pyproj import Proj, Transformer

def wgs84_to_utm(lat:np.ndarray, lon:np.ndarray) -> np.ndarray:
    # 根据经度自动选择合适的UTM坐标系
    utm_zone = np.floor((lon + 180) / 6).astype(int) + 1
    unique_zones = np.unique(utm_zone)

    easting = np.zeros_like(lat)
    northing = np.zeros_like(lon)

    for zone in unique_zones:
        mask = utm_zone == zone
        utm_proj_str = f"+proj=utm +zone={zone} +datum=WGS84"
        transformer = Transformer.from_crs("EPSG:4326", utm_proj_str)
        easting[mask], northing[mask] = transformer.transform(lat[mask], lon[mask])

    return easting, northing, utm_zone



def proj_TM(latitude: np.ndarray, longitude: np.ndarray) -> np.ndarray:
    # WGS84椭球参数
    a = 6378137
    f = 1 / 298.2572236
    # 常量
    b0 = 0
    fn = 0
    fe = 500000
    sf = 1
    PI = math.pi  # Pi
    DEG2RAD = PI / 180  # Degrees to radians
    # MAX_LAT = (PI * 89.99) / 180  # Maximum latitude
    # MAX_DELTA_LONG = (PI * 90) / 180  # Maximum longitude delta

    longitude = longitude * DEG2RAD
    latitude = latitude * DEG2RAD

    ZoneWide = 6 * DEG2RAD  # 6度带
    ProjNo = math.floor(longitude[math.floor(longitude.size / 2)] / ZoneWide)
    l0 = ProjNo * ZoneWide + ZoneWide / 2

    # xy = [0, 0]
    c = c2 = c3 = c5 = c7 = 0
    dlam = eta = eta2 = eta3 = eta4 = 0
    s = sn = t = tan2 = tan3 = tan4 = tan5 = tan6 = 0
    t1 = t2 = t3 = t4 = t5 = t6 = t7 = t8 = t9 = 0
    # tmd = tmdo = temp_Origin = temp_Long = 0
    tmd = tmdo = 0

    TranMerc_es = 2 * f - f * f
    TranMerc_ebs = (1 / (1 - TranMerc_es)) - 1
    TranMerc_b = a * (1 - f)
    tn = (a - TranMerc_b) / (a + TranMerc_b)
    tn2 = tn * tn
    tn3 = tn2 * tn
    tn4 = tn3 * tn
    tn5 = tn4 * tn
    TranMerc_ap = a * (1.e0 - tn + 5.e0 * (tn2 - tn3) / 4.e0 + 81.e0 * (tn4 - tn5) / 64.e0)
    TranMerc_bp = 3.e0 * a * (tn - tn2 + 7.e0 * (tn3 - tn4) / 8.e0 + 55.e0 * tn5 / 64.e0) / 2.e0
    TranMerc_cp = 15.e0 * a * (tn2 - tn3 + 3.e0 * (tn4 - tn5) / 4.e0) / 16.0
    TranMerc_dp = 35.e0 * a * (tn3 - tn4 + 11.e0 * tn5 / 16.e0) / 48.e0
    TranMerc_ep = 315.e0 * a * (tn4 - tn5) / 512.e0

    # if (latitude < -MAX_LAT) or (latitude > MAX_LAT):
    #     return False

    # if longitude > PI:
    #     longitude -= (2 * PI)

    # if (longitude < (l0 - MAX_DELTA_LONG)) or (longitude > (l0 + MAX_DELTA_LONG)):
    #     if longitude < 0:
    #         temp_Long = longitude + 2 * PI
    #     else:
    #         temp_Long = longitude
    #     if l0 < 0:
    #         temp_Origin = l0 + 2 * PI
    #     else:
    #         temp_Origin = l0
    #     if (temp_Long < (temp_Origin - MAX_DELTA_LONG)) or (temp_Long > (temp_Origin + MAX_DELTA_LONG)):
    #         return False

    dlam = longitude - l0

    # if abs(dlam) > (9.0 * PI / 180):
    #     return False

    # if dlam > PI:
    #     dlam -= (2 * PI)
    # if dlam < -PI:
    #     dlam += (2 * PI)
    # if abs(dlam) < 2.e-10:
    #     dlam = 0.0

    s = np.sin(latitude)
    c = np.cos(latitude)
    c2 = c * c
    c3 = c2 * c
    c5 = c3 * c2
    c7 = c5 * c2
    t = np.tan(latitude)
    tan2 = t * t
    tan3 = tan2 * t
    tan4 = tan3 * t
    tan5 = tan4 * t
    tan6 = tan5 * t
    eta = TranMerc_ebs * c2
    eta2 = eta * eta
    eta3 = eta2 * eta
    eta4 = eta3 * eta

    sn = a / np.sqrt(1.e0 - TranMerc_es * np.power(np.sin(latitude), 2.0))

    tmd = TranMerc_ap * latitude - TranMerc_bp * np.sin(2.e0 * latitude) + TranMerc_cp * np.sin(4.e0 * latitude) - TranMerc_dp * np.sin(6.e0 * latitude) + TranMerc_ep * np.sin(8.e0 * latitude)
    tmdo = TranMerc_ap * b0 - TranMerc_bp * np.sin(2.e0 * b0) + TranMerc_cp * np.sin(4.e0 * b0) - TranMerc_dp * np.sin(6.e0 * b0) + TranMerc_ep * np.sin(8.e0 * b0)

    t1 = (tmd - tmdo) * sf
    t2 = sn * s * c * sf / 2.e0
    t3 = sn * s * c3 * sf * (5.e0 - tan2 + 9.e0 * eta + 4.e0 * eta2) / 24.e0
    t4 = sn * s * c5 * sf * (61.e0 - 58.e0 * tan2 + tan4 + 270.e0 * eta - 330.e0 * tan2 * eta + 445.e0 * eta2 + 324.e0 * eta3 - 680.e0 * tan2 * eta2 + 88.e0 * eta4 - 600.e0 * tan2 * eta3 - 192.e0 * tan2 * eta4) / 720.e0
    t5 = sn * s * c7 * sf * (1385.e0 - 3111.e0 * tan2 + 543.e0 * tan4 - tan6) / 40320.e0

    # 北向坐标
    northing = fn + t1 + np.power(dlam, 2.e0) * t2 + np.power(dlam, 4.e0) * t3 + np.power(dlam, 6.e0) * t4 + np.power(dlam, 8.e0) * t5

    t6 = sn * c * sf
    t7 = sn * c3 * sf * (1.e0 - tan2 + eta) / 6.e0
    t8 = sn * c5 * sf * (5.e0 - 18.e0 * tan2 + tan4 + 14.e0 * eta - 58.e0 * tan2 * eta + 13.e0 * eta2 + 4.e0 * eta3 - 64.e0 * tan2 * eta2 - 24.e0 * tan2 * eta3) / 120.e0
    t9 = sn * c7 * sf * (61.e0 - 479.e0 * tan2 + 179.e0 * tan4 - tan6) / 5040.e0

    # 东向坐标
    easting = fe + dlam * t6 + np.power(dlam, 3.e0) * t7 + np.power(dlam, 5.e0) * t8 + np.power(dlam, 7.e0) * t9

    return easting, northing


def get_distance(e, n, alt, ve, vn):
    pass




__all__ = ['wgs84_to_utm', 'proj_TM', 'get_distance']
