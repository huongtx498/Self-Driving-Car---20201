# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import math
import numpy as np
RIGHT = [(2250, 1968), (2292, 1830), (2316, 1788),
         (2262, 1770), (1848, 1638), (2076, 1710)]
LEFT = [(2202, 1968), (2250, 1824), (1830, 1686), (2058, 1758)]
position = (2280, 1800)
alpha = 2.316666


def nam_giua(node1, node2, point):
    k1 = (node1[0] - point[0]) / (node2[0] - point[0])
    k2 = (node1[1] - point[1]) / (node2[1] - point[1])
    if round(k1, 1) == round(k2, 1) and k1 < 0:
        return True
    return False


def get_giao_diem_2dt(dt1, dt2):
    if dt2[0] == dt1[0] * dt2[1] / dt1[1]:
        return (0, 0)
    x = (dt1[2] * dt2[1] / dt1[1] - dt2[2]) / \
        (dt2[0] - dt1[0] * dt2[1] / dt1[1])
    y = (dt1[0] * x + dt1[2]) / ((-1) * dt1[1])
    return (x, y)


def get_ptdt_qua_2diem(point1, point2):
    if point2[0] == point1[0]:
        return None
    a = (point2[1] - point1[1]) / (point2[0] - point1[0])
    b = point1[1] - a * point1[0]
    return [a, -1, b]


# ax + by + c = 0
def get_ptdt_qua_xe(position, point1, point2):
    vtpt = (point2[0] - point1[0], point2[1] - point1[1])
    return [vtpt[0], vtpt[1], (-1) * vtpt[0] * position[0] - vtpt[1] * position[1]]


def distance(a, b):
    return math.dist(a, b)


def get_khoangcach(dt1, node1, node2, position):
    dt2 = get_ptdt_qua_2diem(node1, node2)
    print("ptdt qua 2 diem:", dt2)
    giaodiem = get_giao_diem_2dt(dt1, dt2)
    print("nam_giua({}, {}, {})".format(node1, node2, giaodiem))
    if nam_giua(node1, node2, giaodiem):
        return distance(position, giaodiem)
    return min([distance(position, node1), distance(position, node2)])


def min_distance_den_1_le(tap_diem_le, position):
    list_distance = []
    for i in range(0, len(tap_diem_le) - 1):
        ptdt_qua_xe = get_ptdt_qua_xe(
            position, tap_diem_le[i], tap_diem_le[i + 1])
        print("pttd qua xe: ", ptdt_qua_xe)
        khoang_cach = get_khoangcach(
            ptdt_qua_xe, tap_diem_le[i], tap_diem_le[i + 1], position)
        list_distance.append(khoang_cach)
    if list_distance == []:
        return 0
    return min(list_distance)


def do_lech_trai(position):
    distance_left = min_distance_den_1_le(
        LEFT, position)
    distance_right = min_distance_den_1_le(
        RIGHT, position)
    print("left:", distance_left)
    print("right:", distance_right)
    if distance_left == distance_right == 0:
        left_dist = 0.0
    else:
        left_dist = distance_left / (distance_left + distance_right)
    return left_dist


print(do_lech_trai(position))
