import itertools
import math
import os
import sys

import numpy as np
import pygame
import xlrd
from fuzzy_base import get_pos

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from fuzzy_base.dijkstra import get_path

from graphic.loader import load_image

PI = math.pi

# Map filenames.
MAP_NAVS = []  # mảng tọa độ (x, y) của các điểm trung tâm
LINE_NAVS = []

FINISH_INDEX = 0

# mảng các vị trí của đèn giao thông (số thứ tự điểm trong chuỗi điểm đường đi - là số thứ tự điểm, k phải tọa độ)
TRAFFIC_LAMP_POS = []
# mảng thông tin chi tiết của đèn tín hiệu: tọa độ x, y, hướng của đèn, index
TRAFFIC_LAMP_COORDINATES = []

pos = dict()
margin = dict()
listPoint = []

margin_path = []
left_margin_point = []
right_margin_point = []


class Map(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y, map_number):
        pygame.sprite.Sprite.__init__(self)

        self.map_number = map_number
        image_temp = "map" + str(map_number) + ".png"
        self.get_map_navs()
        self.image = load_image(image_temp)
        self.rect = self.image.get_rect()
        self.rect_w = self.rect.size[0]
        self.rect_h = self.rect.size[1]
        self.image = pygame.transform.scale(
            self.image, (int(self.rect_w * 6), int(self.rect_h * 6))
        )
        self.x = init_x
        self.y = init_y
        blue = 230, 30, 30
        print("POS: ", pos)
        print("------------------------------------------------------------")
        print("LISTPOINT: ", listPoint)
        print("------------------------------------------------------------")
        print("MARGIN: ", margin)
        print("------------------------------------------------------------")
        margin_path = draw_margin(listPoint, margin, pos)
        print("MARGIN PATH: ", margin_path)
        print("------------------------------------------------------------")

        left_margin_point, right_margin_point = getMarginPoint(
            margin, margin_path, listPoint, pos
        )
        print("LEFT MARGIN POINT: ", left_margin_point)
        print("------------------------------------------------------------")
        print("RIGHT MARGIN POINT: ", right_margin_point)
        print("------------------------------------------------------------")
        pygame.draw.lines(self.image, blue, False, left_margin_point, 5)
        pygame.draw.lines(self.image, blue, False, right_margin_point, 5)

    # Realign the map

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x + 800, self.y - cam_y + 500

    def get_map_navs(self):
        with xlrd.open_workbook("../media/toa-do.xlsx") as book:
            # listP, dis = get_path(82, 37)
            listP, dis = get_path(get_pos.start_point, get_pos.end_point)
            sheet = book.sheet_by_index(0)
            for pointid in listP:
                listPoint.append(pointid)
                for row_num in range(sheet.nrows):
                    row_value = sheet.row_values(row_num)
                    if row_value[0] == pointid:
                        # both center & margin point
                        pos[int(row_value[0])] = (
                            int(row_value[1]) * 6,
                            int(row_value[2]) * 6,
                        )
                        pos[int(row_value[3])] = (
                            int(row_value[4]) * 6,
                            int(row_value[5]) * 6,
                        )
                        pos[int(row_value[6])] = (
                            int(row_value[7]) * 6,
                            int(row_value[8]) * 6,
                        )
                        if row_value[9] != "":
                            pos[int(row_value[9])] = (
                                int(row_value[10]) * 6,
                                int(row_value[11]) * 6,
                            )
                            pos[int(row_value[12])] = (
                                int(row_value[13]) * 6,
                                int(row_value[14]) * 6,
                            )

                        # margin point
                        margin[int(row_value[0])] = [
                            int(row_value[3]),
                            int(row_value[6]),
                        ]
                        if row_value[9] != "":
                            margin[int(row_value[0])].extend(
                                [int(row_value[9]), int(row_value[12])]
                            )

                        MAP_NAVS.append(
                            (
                                int(row_value[1]) * 6,
                                int(row_value[2]) * 6,
                                int(row_value[0]),
                            )
                        )

                        # center line point
                        LINE_NAVS.append(
                            (int(row_value[1]) * 6, int(row_value[2]) * 6))

            sheet = book.sheet_by_index(1)
            i = 0.0
            j = 0
            for pointid in listPoint:
                for row_num in range(sheet.nrows):
                    row_value = sheet.row_values(row_num)
                    if row_value[5] == pointid:
                        # TRAFFIC_LAMP_POS.append(int(row_value[5]))
                        TRAFFIC_LAMP_POS.append(
                            listPoint.index(int(row_value[5])))
                        TRAFFIC_LAMP_COORDINATES.append(
                            (
                                int(row_value[1]) * 6,
                                int(row_value[2]) * 6,
                                int(row_value[3]),
                                i,
                            )
                        )
                        i = i + 1.0
                    j = j + 1
            print("TRAFFIC LAMP POS: ", TRAFFIC_LAMP_COORDINATES)
            print("------------------------------------------------------------")


def he_so_goc(alpha):
    return math.tan(alpha)


def get_ptdt(P, Q):
    # [1,2], [3,4] => ax + by = c
    a = Q[1] - P[1]
    b = P[0] - Q[0]
    c = a * (P[0]) + b * (P[1])
    return a, b, c


def get_ptdt_qua_xe(pos, alpha):
    k = he_so_goc(alpha)
    a, b, c = (
        k,
        -1,
        k * pos[0] - pos[1],
    )  # ax + by = c, ptdt qua tam xa va tao voi truc Ox 1 goc
    return -b, a, -(-b * pos[0] + a * pos[1])


def get_giao_diem(arr1, arr2):
    # [4,3,32], [4,-2,12] => [x, y]
    import numpy as np

    a = np.array([[arr1[0], arr1[1]], [arr2[0], arr2[1]]])
    b = np.array([arr1[2], arr2[2]])
    try:
        return np.linalg.solve(a, b)
    except:
        return None


def distance(a, b):
    return math.dist(a, b)


# [1,2,3], {1: [33,44], ...}
def min_distance_den_1_tap_canh(tap_canh, listPoint, pos):
    list_distance = []
    tam_xe, alpha = getInitProp(listPoint, pos)
    ptdt_qua_xe = get_ptdt_qua_xe(tam_xe, alpha)
    for i in range(len(tap_canh) - 2):
        toa_do_cur = tap_canh[i]
        toan_do_next = tap_canh[i + 1]
        ptdt = get_ptdt(toa_do_cur, toan_do_next)
        giao_diem = get_giao_diem(ptdt, ptdt_qua_xe)
        if giao_diem is not None:
            list_distance.append(distance(tam_xe, giao_diem))
        else:
            list_distance.append(999999999)
    return min(list_distance)


def do_lech_trai(tap_canh_trai, tap_canh_phai, listPoint, pos):
    distance_left = min_distance_den_1_tap_canh(tap_canh_trai, listPoint, pos)
    distance_right = min_distance_den_1_tap_canh(tap_canh_phai, listPoint, pos)
    return distance_left / (distance_left + distance_right)


def draw_margin(listPoint, margin, pos):
    margin_path = []
    cent_lines = []
    for i in range(len(listPoint) - 1):
        # print("check {} - {}".format(listPoint[i], listPoint[i + 1]))
        cent_lines.append((listPoint[i], listPoint[i + 1]))
        pos_1 = pos[listPoint[i]]
        pos_2 = pos[listPoint[i + 1]]
        A = [pos_1, pos_2]
        margin_path = list(set(margin_path))

        # check cat
        for item in margin_path:
            B1 = pos[item[0]]
            B2 = pos[item[1]]
            if is_intersected(A, [B1, B2]):
                margin_path.remove(item)

        # print("pos: {}".format(A))
        d = linear(pos_1, pos_2)
        margin_1 = margin[listPoint[i]]
        # print("margin1: {}".format(margin_1))
        margin_2 = margin[listPoint[i + 1]]
        # print("margin2: {}".format(margin_2))
        margin_1p, margin_1n = side(d, margin_1)
        # print("margin1p: {}, margin1n: {}".format(margin_1p, margin_1n))
        margin_2p, margin_2n = side(d, margin_2)
        # print("margin2p: {}, margin2n: {}".format(margin_2p, margin_2n))
        margin_p = list(itertools.product(margin_1p, margin_2p))
        margin_p.extend(itertools.combinations(margin_1p, 2))
        margin_p.extend(itertools.combinations(margin_2p, 2))

        margin_n = list(itertools.product(margin_1n, margin_2n))
        margin_n.extend(itertools.combinations(margin_1n, 2))
        margin_n.extend(itertools.combinations(margin_2n, 2))

        margin_p_with_dist = [
            (item, dist_point_point(pos[item[0]], pos[item[1]])) for item in margin_p
        ]
        margin_n_with_dist = [
            (item, dist_point_point(pos[item[0]], pos[item[1]])) for item in margin_n
        ]

        margin_p_with_dist.sort(key=lambda x: x[1])
        margin_n_with_dist.sort(key=lambda x: x[1])
        # print("margin_p_with_dist: {}, margin_n_with_dist: {}".format(
        #     margin_p_with_dist, margin_n_with_dist))

        num_point = len(margin_1p) + len(margin_2p)
        # print("num_point: {}".format(num_point))
        able_draw_p = [item[0] for item in margin_p_with_dist[: num_point - 1]]
        margin_path.extend(able_draw_p)
        able_draw_n = [item[0] for item in margin_n_with_dist[: num_point - 1]]
        margin_path.extend(able_draw_n)

        if len(margin[listPoint[i]]) == 4:
            for j in range(3):
                able_draw = (margin[listPoint[i]][j],
                             margin[listPoint[i]][j + 1])
                B = [pos[able_draw[0]], pos[able_draw[1]]]
                if is_intersected(A, B) == False:
                    margin_path.append(able_draw)

    # last check
    pairs = list(itertools.product(cent_lines, margin_path))
    # print(pairs)
    for pair in pairs:
        # print("pair : {}".format(pair))
        margin_line = pair[1]
        cent_line = pair[0]

        A = [pos[cent_line[0]], pos[cent_line[1]]]
        B = [pos[margin_line[0]], pos[margin_line[1]]]
        # print("{} - {}".format(A, B))
        flag = is_intersected(A, B)

        if is_intersected(A, B):
            # print("is_intersected: {}". format(flag))
            # print(margin_line)
            margin_path.remove(margin_line)

    return list(set(margin_path))


def linear(a, b):
    pos_a = a
    pos_b = b

    a1 = pos_b[1] - pos_a[1]
    a2 = pos_a[0] - pos_b[0]
    a3 = pos_a[1] * (pos_b[0] - pos_a[0]) - pos_a[0] * (pos_b[1] - pos_a[1])
    return a1, a2, a3


def dist_point_linear(a, B):
    pos_a = a
    return abs(B[0] * pos_a[0] + B[1] * pos_a[1] + B[2]) / math.sqrt(
        B[0] ** 2 + B[1] ** 2
    )


def intersect_point(dA, dB):
    a = np.array([[dA[0], dA[1]], [dB[0], dB[1]]])
    b = np.array([-dA[2], -dB[2]])
    try:
        return np.linalg.solve(a, b)
    except:
        return None


def dist_point_point(a, b):
    pos_a = a
    pos_b = b

    return math.sqrt((pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2)


def is_intersected(A, B):
    A_0 = A[0]
    A_1 = A[1]
    B_0 = B[0]
    B_1 = B[1]

    dA = linear(A_0, A_1)
    dB = linear(B_0, B_1)
    x = intersect_point(dA, dB)

    if x is None:
        return False

    dist_a = dist_point_point(x, A_0) + dist_point_point(x, A_1)
    dist_b = dist_point_point(x, B_0) + dist_point_point(x, B_1)

    eps = 0.1
    if (abs(dist_point_point(A_0, A_1) - dist_a) < eps) and (
        abs(dist_point_point(B_0, B_1) - dist_b) < eps
    ):
        return True
    else:
        return False


def checkStartEndPoint(x, listP):
    count = 0
    for point in listP:
        if x in point:
            count += 1
    if count == 1:
        return True
    return False


def getStartPoint(listP, marginP):
    start = []
    for point in marginP:
        for i in marginP[point]:
            if i in listP:
                start.append(i)
        if len(start) > 1:
            return start
    return start


def getMarginLine(startP, margin_Path):
    lineP = []
    previous = startP
    lineP.append(previous)
    while checkStartEndPoint(previous, margin_Path):
        for path in margin_Path:
            if previous in path:
                for point in path:
                    if point != previous:
                        previous = point
                        lineP.append(previous)
                        break
                margin_Path.remove(path)
                break
    return lineP


def converIndexToNavs(listIndex, pos):
    navs = []
    for index in listIndex:
        navs.append(pos[index])
    return navs


def check4ways(index, margin):
    if len(margin[index]) > 2:
        return True
    return False


def softLeftRight(list1, list2, path, margin, pos):
    a = b = (0, 0)
    current_index = path[0]
    target_index = path[1]
    next_ = None
    l = len(path)
    for index, obj in enumerate(path):
        if index < len(path) - 1:
            next_ = path[index + 1]
            if not check4ways(next_, margin):
                current_index = obj
                target_index = next_
                break

    current = pos[current_index]
    target = pos[target_index]

    if margin[target_index][0] in list1:
        a = pos[margin[target_index][0]]
        b = pos[margin[target_index][1]]
    else:
        a = pos[margin[target_index][1]]
        b = pos[margin[target_index][0]]
    t_c = math.atan2(target[1] - current[1], target[0] - current[0])
    a_c = math.atan2(a[1] - current[1], a[0] - current[0])
    b_c = math.atan2(b[1] - current[1], b[0] - current[0])
    if a_c * b_c < 0 and (t_c > PI / 2 or t_c < -PI / 2):
        if a_c > b_c:
            return list2, list1
        return list1, list2
    if a_c > b_c:
        return list1, list2
    return list2, list1


# lấy ra tập điểm trái và phải của lề (trả về  theo thứ tự trái, phải)


def getMarginPoint(margin, margin_path, path, pos):
    listP = []
    for subpath in margin_path:
        for point in subpath:
            if checkStartEndPoint(point, margin_path):
                listP.append(point)
    start = getStartPoint(listP, margin)
    margin_point_index_1 = getMarginLine(start[0], margin_path)
    margin_point_index_2 = getMarginLine(start[1], margin_path)
    left_point_index, right_point_index = softLeftRight(
        margin_point_index_1, margin_point_index_2, path, margin, pos
    )
    left_margin_point = converIndexToNavs(left_point_index, pos)
    right_margin_point = converIndexToNavs(right_point_index, pos)
    print("MARGIN LEFT POINT: ", left_point_index)
    print("------------------------------------------------------------")
    print("MARGIN RIGHT POINT: ", right_point_index)
    print("------------------------------------------------------------")
    return left_margin_point, right_margin_point


# lấy ra điểm xuất phát và góc ban đầu của xe (hợp với trục Ox)


def getInitProp(listPoint, pos):
    a = listPoint[0]
    b = listPoint[1]
    alpha = math.atan2(pos[b][1] - pos[a][1], pos[b][0] - pos[a][0])
    return pos[a], alpha


def side(d, list_points):
    positives = []
    negatives = []
    for p in list_points:
        point = pos[p]
        fx = d[0] * point[0] + d[1] * point[1] + d[2]
        # print("point: {}, pos: {}, fx: {}".format(p, point, fx))
        if fx >= 0:
            positives.append(p)
        else:
            negatives.append(p)
    return positives, negatives
