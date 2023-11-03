from PIL import Image
import numpy as np

HEIGHT = 2304
WIDTH = 5632
PROVINCE_BORDER_RGB = (0, 0, 0)  # it is border, black
PROVINCE_INSIDE_RGB = (255, 255, 255)  # it is inside province, white
grey = (224, 224, 224)  # it is not certain, light grey
SEA_RGB = (153, 204, 255)  # it is sea or water, blue

# Copied from default.map
SEA_PROV_SET = {
    # sea
    1589, 1592, 1593, 1594, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607,
    1608, 1609, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624,
    1625, 1626, 1627, 1628, 1629, 1630, 1631, 1632, 1633, 1634, 1635, 1636, 1637, 1638, 1639, 1640, 1641,
    1643, 1644, 1645, 1646, 1647, 1648, 1649, 1650, 1651, 1652, 1653, 1654, 1655, 1656, 1657, 1658, 1659,
    1660, 1661, 1662, 1664, 1665, 1666, 1667, 1668, 1669, 1670, 1671, 1672, 1673, 1674, 1675, 1676, 1678,
    1679, 1680, 1681, 1682, 1683, 1684, 1685, 1686, 1687, 1688, 1689, 1690, 1691, 1692, 1693, 1694, 1695,
    1696, 1698, 1699, 1700, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1712, 1713, 1714, 1715, 1716,
    1717, 1718, 1719, 1720, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728, 1729, 1730, 1731, 1732, 1736,
    1737, 1738, 1739, 1740, 1741, 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749, 1754, 1757, 1766, 1768,
    1769, 1770, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1782, 1783, 1784, 1785, 1786,
    1787, 1788, 1789, 1790, 1791, 1792, 1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803,
    1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820,
    1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1838, 1839, 1840, 1841, 1842,
    1843, 1846, 1847, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1860, 1862, 1863, 1864, 1866,
    1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883,
    1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900,
    1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917,
    1918, 1919, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936,
    1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953,
    1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970,
    1971, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988,
    1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
    2006, 2007, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023,
    2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040,
    2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057,
    2058, 2059, 2060, 2061, 2062, 2063, 2064, 2518, 2519, 2521, 2522, 2523, 2524, 2526, 2782, 2783, 2784,
    4105, 4106, 4107, 4108, 4109, 4313, 5285, 5286, 5287, 5288, 5289, 5290, 5504, 4284, 4285, 4286, 4287,
    4288, 4289, 4290, 4291, 4292, 4293, 4294, 4295, 4296, 4297, 4298, 4299, 4300, 4301, 4302, 4303, 4304,
    4305, 4306, 4307, 4308, 4309, 4310, 4311, 4312, 4314, 4315, 4316, 4317, 4318, 4319, 4320, 4321, 4322,
    4323, 4324, 4325, 4326, 4327, 4328, 4329, 4330, 4331, 4332, 4333, 4334, 4335, 4336, 4337, 4338, 4339,
    4340, 4341, 4342, 4343, 4344, 4345, 4346, 4347, 4348, 4349, 4350, 4351, 4352, 4353, 4354, 4355, 4356,
    4357, 4358,
    # lake
    1677, 1750, 1751, 1752, 1753, 1756, 1761, 1762, 1763, 1764, 1765, 1920, 1921, 2164, 3307, 3707, 3708,
    3709, 3710, 5283, 3711, 3712, 3713, 3714, 3715, 3716, 3717, 3718, 3975, 3976, 3978, 3979, 3995, 3996,
    4359, 4360, 4361, 4362, 4363, 2646, 4364, 4365, 4366, 4367, 4368, 4369, 4370, 4371, 4372, 4373, 4374,
    4375, 4376, 4377, 4378, 4379, 4380, 4381, 4382, 4383, 4384, 4385, 4386, 4387, 4388, 4389, 4390, 4391,
    4392, 4393, 4394, 4395, 4396, 4397, 4398, 4399, 4400, 4401, 4402, 4403, 4404, 4405, 4406, 4407, 4408,
    4409, 4410, 4411, 4412, 4413, 4414, 4415, 4416, 4417, 4418, 4419, 4420, 4421, 4422, 4423, 5509, 5510
}


def produce_background(rgbid_set, input_f='../original/provinces.bmp', output_f='temp.bmp'):
    #          up
    #          |
    # left -- curr - right
    #         |
    #        down

    images = Image.open(input_f)
    img_array = np.array(images)
    shape = img_array.shape
    print(img_array.shape)
    height = shape[0]
    width = shape[1]
    dst = np.zeros((height, width, 3))  # it is used to store results

    left = PROVINCE_INSIDE_RGB
    up = PROVINCE_INSIDE_RGB
    down = PROVINCE_INSIDE_RGB

    for h in range(0, height):
        for w in range(0, width):
            # 1. Get the current point
            (r, g, b) = img_array[h, w]

            # if (r, g, b) == SEA_1:
            #     continue

            # 2. Find the point around the current point
            if h == 0:
                down = tuple(img_array[h + 1, w])
            elif h == height - 1:
                up = tuple(img_array[h - 1, w])
            else:
                up = tuple(img_array[h + 1, w])
                down = tuple(img_array[h - 1, w])

            if w < width - 1:
                right = tuple(img_array[h, w + 1])
            else:
                right = PROVINCE_INSIDE_RGB

            # 3. Match the pattern to determine it is border or provinces
            if (left == (r, g, b)) & (right == (r, g, b)) & (up == (r, g, b)) & ((r, g, b) == down):
                dst[h, w] = PROVINCE_INSIDE_RGB
            elif (left == (r, g, b)) & ((r, g, b) != right) & (up == (r, g, b)):
                #   w
                # w,w(*),b
                #   ?
                dst[h, w] = PROVINCE_BORDER_RGB
            elif (up == (r, g, b)) & ((r, g, b) != down) & (left == (r, g, b)):
                #   w
                # w w(*)?
                #   b
                dst[h, w] = PROVINCE_BORDER_RGB
            elif (left == (r, g, b)) & (right != (r, g, b)) & (up == (r, g, b)) & ((r, g, b) == down):
                #   w
                # w w(*) b
                #   w
                dst[h, w] = PROVINCE_BORDER_RGB
            else:
                # Not sure if it is border or provinces
                dst[h, w] = grey

            # (it is bug...)
            left = (r, g, b)

    # this step is for sea and lake
    for h in range(0, height):
        for w in range(0, width):
            (r, g, b) = img_array[h, w]
            rgb_str = "%s_%s_%s" % (str(r), str(g), str(b))
            if rgb_str not in rgbid_set:
                dst[h, w] = SEA_RGB
    print("Transformation is done, output to " + output_f)
    dst_img = Image.fromarray(np.uint8(dst))
    dst_img.save(output_f, "bmp")


def fetch_province_rgb_and_position(pos_file='../original/positions.txt',
                                    rgb_file='../original/definition.csv',
                                    area_file='../original/area.txt'):
    """
    Output format is a dict, which key is provinceId, int, and values is a dict with following values:
        province_id, province_name, province_name_cn, color_rgb, position_x, position_y,
        culture, area, region, super_region, continent, terrain

    Source files is :
        RGB          - original/definition.csv
        Position     - original/positions.txt
        Area         - original/area.txt
        Region       - original/region.txt
        Superregion  - original/superregion.txt

    """
    import csv

    prov_data = dict()

    with open(rgb_file, encoding='iso-8859-1') as f:
        f_csv = csv.reader(f, delimiter=';')
        headers = next(f_csv)
        for row in f_csv:
            prov = {"r": row[1],
                    "g": row[2],
                    "b": row[3],
                    "rgb": "%s_%s_%s" % (row[1], row[2], row[3]),
                    "name": row[4],
                    }
            prov_data[int(row[0])] = prov
    print(prov_data[236])  # check London data

    """
    #Uppland
    1={
        position={
            2919.500 2028.000 2923.000 2034.000 2911.000 2042.000 2922.500 2028.000 2926.000 2026.000 2923.000 2033.000 2915.000 2036.000 
        }
        rotation={
            4.974 0.000 0.000 -2.356 0.000 0.000 0.000 
        }
        height={
            0.000 0.000 0.800 0.000 0.000 0.000 0.000 
        }
    }
    """
    with open(pos_file, encoding='iso-8859-1') as f:
        row = f.readline()
        while row:
            if row.find("#") != -1:  # 跳过首行
                row = f.readline()
                prov_id = int(row.split("=")[0])
                f.readline()
                row = f.readline().strip()  # 跳过两行
                pos_x = row.split(' ')[4]
                pos_y = row.split(' ')[5]
                prov_data[prov_id]["pos_x"] = pos_x
                prov_data[prov_id]["pos_y"] = pos_y
                pass
            else:
                row = f.readline()
    print(prov_data[236])  # check London data

    """
    british_coasts_area = {
        1877 1878 1881 1882 1919
    }
    """
    with open(area_file, encoding='utf-8') as f:
        row = f.readline()
        while row:
            if row.find("=") != -1:  # 跳过首行
                area = row.split("=")[0].strip()
                row = f.readline()
                while row.find("#") != -1:
                    row = f.readline()
                prov_ids = row.strip().split(' ')
                for pid in prov_ids:
                    try:
                        i = int(pid)
                        prov_data[i]['area'] = area
                    except:
                        pass

                # break
            if row.find("}") != -1:
                pass
            if row.find("#") != -1:
                pass
            row = f.readline()
    print(prov_data[236])  # check London data
    return prov_data
    # rgb_set = set()


def fetch_province_rgb(input_f='../original/provinces.bmp'):
    images = Image.open(input_f)
    img_array = np.array(images)
    shape = img_array.shape
    print(img_array.shape)
    height = shape[0]
    width = shape[1]
    for h in range(0, height):
        for w in range(0, width):
            (r, g, b) = img_array[h, w]
            ss = "%s_%s_%s" % (str(r), str(g), str(b))
            # print(ss)

            if (r, g, b) == (33, 120, 64):  # This is london 's rgb
                # these are all the position of london
                print("---------------- %d - %d - %d" % (w, h, 2304 - h))


# fetch_province_rgb()

if __name__ == "__main__":
    print("Hello MT")
    prov_data = fetch_province_rgb_and_position()
    print("Collect %d provinces data." % len(prov_data))
    rgb_set = set()
    for p in prov_data:
        if p not in SEA_PROV_SET:
            rgb_set.add(prov_data[p]['rgb'])
    print(len(rgb_set))
    # fetch_province_rgb(1850, 2330)
    # fetch_province_rgb(1950, 2330)
    # fetch_province_rgb(1950, 2130)
    produce_background(rgb_set)
