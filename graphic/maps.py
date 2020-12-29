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


def nam_giua(node1, node2, point):
    if node2[0] == point[0] or node2[1] == point[1]:
        return False
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
def get_ptdt_qua_xe(position, alpha):
    return [math.tan(alpha), -1, position[1] - math.tan(alpha) * position[0]]


def distance(a, b):
    return math.dist(a, b)


def get_khoangcach(dt1, node1, node2, position):
    dt2 = get_ptdt_qua_2diem(node1, node2)
    giaodiem = get_giao_diem_2dt(dt1, dt2)
    if nam_giua(node1, node2, giaodiem):
        return distance(position, giaodiem)
    return 1000000


def min_distance_den_1_le(tap_diem_le, position, alpha):
    list_distance = []
    ptdt_qua_xe = get_ptdt_qua_xe(position, alpha)
    for i in range(0, len(tap_diem_le) - 1):
        khoang_cach = get_khoangcach(
            ptdt_qua_xe, tap_diem_le[i], tap_diem_le[i + 1], position)
        list_distance.append(khoang_cach)
    if list_distance == []:
        return 0
    return min(list_distance)


def linear(a, b):
    pos_a = a
    pos_b = b

    a1 = pos_b[1] - pos_a[1]
    a2 = pos_a[0] - pos_b[0]
    a3 = pos_a[1] * (pos_b[0] - pos_a[0]) - \
        pos_a[0] * (pos_b[1] - pos_a[1])
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
    marginP = []
    lineP = []
    for i in margin_Path:
        marginP.append(i)
    previous = startP
    lineP.append(previous)
    while checkStartEndPoint(previous, marginP):
        for path in marginP:
            if previous in path:
                for point in path:
                    if point != previous:
                        previous = point
                        lineP.append(previous)
                        break
                marginP.remove(path)
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


def side(d, list_points, pos):
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


class Map(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        pygame.sprite.Sprite.__init__(self)
        image_temp = "map.png"

        # dict các tọa độ (x, y) của các điểm trên bản đồ
        self.pos = dict()
        # margin :dict các index điểm kề của điểm giữa đường a = [b, c]
        self.margin = dict()
        # listPoint :list các điểm giữa đường theo thứ tự xuất phát => kết thúc
        self.listPoint = []
        # margin_path :list các cạnh
        self.margin_path = []
        # left_margin_point :list các điểm bên lề trái (theo thứ tự xuất phát => kết thúc)
        self.left_margin_point = []
        # right_margin_point :list các điểm bên lề phải (theo thứ tự xuất phát => kết thúc)
        self.right_margin_point = []
        # left_dist: độ lệch trái tại 1 thời điểm
        self.left_dist = 0
        # position: tọa độ xe hiện tại
        self.position = (0, 0)
        # alpha: góc lệnh của xe hiện tại (radian)
        self.alpha = 0.0

        self.image = load_image(image_temp)
        self.rect = self.image.get_rect()
        self.rect_w = self.rect.size[0]
        self.rect_h = self.rect.size[1]
        self.image = pygame.transform.scale(
            self.image, (int(self.rect_w * 6), int(self.rect_h * 6))
        )

        # khởi tạo các giá trị tọa độ ban đầu
        self.get_map_navs()
        # tính toán ra các tập cạnh
        self.draw_margin()
        # tách tập cạnh thành 2 tập điểm lề trái và lề phải
        self.getMarginPoint()

        self.x = init_x
        self.y = init_y
        blue = 230, 30, 30
        pygame.draw.lines(self.image, blue, False, self.left_margin_point, 5)
        pygame.draw.lines(self.image, blue, False, self.right_margin_point, 5)

        print("TỌA ĐỘ TẤT CẢ CÁC ĐIỂM: ", self.pos)
        print("------------------------------------------------------------")
        print("LIST ĐIỂM ĐƯỜNG ĐI: ", self.listPoint)
        print("------------------------------------------------------------")
        print("TẬP ĐIỂM KỀ: ", self.margin)
        print("------------------------------------------------------------")
        print("TẬP CẠNH: ", self.margin_path)
        print("------------------------------------------------------------")

    # Realign the map

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x + 800, self.y - cam_y + 500

    # lấy ra điểm xuất phát và góc ban đầu của xe - radian (hợp với trục Ox)

    def getInitProp(self):
        a = self.listPoint[0]
        b = self.listPoint[1]
        alpha = math.atan2(self.pos[b][1] - self.pos[a]
                           [1], self.pos[b][0] - self.pos[a][0])
        return self.pos[a], alpha

    # set vị trí tọa độ và góc (dự phòng)
    def setPosAlpha(self, position, alpha):
        self.position = position
        self.alpha = alpha
        return

    # get vị trí tọa độ và góc (dự phòng)
    def getPosAlpha(self):
        return self.position, self.alpha

    def get_map_navs(self):
        with xlrd.open_workbook("../media/toa-do.xlsx") as book:
            # listP, dis = get_path(82, 37)
            self.listPoint, self.dis = get_path(
                get_pos.start_point, get_pos.end_point)
            sheet = book.sheet_by_index(0)
            for pointid in self.listPoint:
                for row_num in range(sheet.nrows):
                    row_value = sheet.row_values(row_num)
                    if row_value[0] == pointid:
                        # both center & self.margin point
                        self.pos[int(row_value[0])] = (
                            int(row_value[1]) * 6,
                            int(row_value[2]) * 6,
                        )
                        self.pos[int(row_value[3])] = (
                            int(row_value[4]) * 6,
                            int(row_value[5]) * 6,
                        )
                        self.pos[int(row_value[6])] = (
                            int(row_value[7]) * 6,
                            int(row_value[8]) * 6,
                        )
                        if row_value[9] != "":
                            self.pos[int(row_value[9])] = (
                                int(row_value[10]) * 6,
                                int(row_value[11]) * 6,
                            )
                            self.pos[int(row_value[12])] = (
                                int(row_value[13]) * 6,
                                int(row_value[14]) * 6,
                            )

                        # margin point
                        self.margin[int(row_value[0])] = [
                            int(row_value[3]),
                            int(row_value[6]),
                        ]
                        if row_value[9] != "":
                            self.margin[int(row_value[0])].extend(
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
            for pointid in self.listPoint:
                for row_num in range(sheet.nrows):
                    row_value = sheet.row_values(row_num)
                    if row_value[5] == pointid:
                        # TRAFFIC_LAMP_POS.append(int(row_value[5]))
                        TRAFFIC_LAMP_POS.append(
                            self.listPoint.index(int(row_value[5])))
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

    # tính độ lệch tới lề trái tại 1 thời điểm position: tuple, alpha: float
    def do_lech_trai(self, position, alpha):
        distance_left = min_distance_den_1_le(
            self.left_margin_point, position, alpha)
        distance_right = min_distance_den_1_le(
            self.right_margin_point, position, alpha)
        if distance_left == distance_right == 0:
            self.left_dist = 0.0
        else:
            self.left_dist = distance_left / (distance_left + distance_right)
        return self.left_dist

    def draw_margin(self):
        self.margin_path = []
        cent_lines = []
        for i in range(len(self.listPoint) - 1):
            # print("check {} - {}".format(self.listPoint[i], self.listPoint[i + 1]))
            cent_lines.append((self.listPoint[i], self.listPoint[i + 1]))
            pos_1 = self.pos[self.listPoint[i]]
            pos_2 = self.pos[self.listPoint[i + 1]]
            A = [pos_1, pos_2]
            self.margin_path = list(set(self.margin_path))

            # check cat
            for item in self.margin_path:
                B1 = self.pos[item[0]]
                B2 = self.pos[item[1]]
                if is_intersected(A, [B1, B2]):
                    self.margin_path.remove(item)

            # print("pos: {}".format(A))
            d = linear(pos_1, pos_2)
            margin_1 = self.margin[self.listPoint[i]]
            # print("margin1: {}".format(margin_1))
            margin_2 = self.margin[self.listPoint[i + 1]]
            # print("margin2: {}".format(margin_2))
            margin_1p, margin_1n = side(d, margin_1, self.pos)
            # print("margin1p: {}, margin1n: {}".format(margin_1p, margin_1n))
            margin_2p, margin_2n = side(d, margin_2, self.pos)
            # print("margin2p: {}, margin2n: {}".format(margin_2p, margin_2n))
            margin_p = list(itertools.product(margin_1p, margin_2p))
            margin_p.extend(itertools.combinations(margin_1p, 2))
            margin_p.extend(itertools.combinations(margin_2p, 2))

            margin_n = list(itertools.product(margin_1n, margin_2n))
            margin_n.extend(itertools.combinations(margin_1n, 2))
            margin_n.extend(itertools.combinations(margin_2n, 2))

            margin_p_with_dist = [
                (item, dist_point_point(self.pos[item[0]], self.pos[item[1]])) for item in margin_p
            ]
            margin_n_with_dist = [
                (item, dist_point_point(self.pos[item[0]], self.pos[item[1]])) for item in margin_n
            ]

            margin_p_with_dist.sort(key=lambda x: x[1])
            margin_n_with_dist.sort(key=lambda x: x[1])
            # print("margin_p_with_dist: {}, margin_n_with_dist: {}".format(
            #     margin_p_with_dist, margin_n_with_dist))

            num_point = len(margin_1p) + len(margin_2p)
            # print("num_point: {}".format(num_point))
            able_draw_p = [item[0]
                           for item in margin_p_with_dist[: num_point - 1]]
            self.margin_path.extend(able_draw_p)
            able_draw_n = [item[0]
                           for item in margin_n_with_dist[: num_point - 1]]
            self.margin_path.extend(able_draw_n)

            if len(self.margin[self.listPoint[i]]) == 4:
                for j in range(3):
                    able_draw = (self.margin[self.listPoint[i]][j],
                                 self.margin[self.listPoint[i]][j + 1])
                    B = [self.pos[able_draw[0]], self.pos[able_draw[1]]]
                    if is_intersected(A, B) == False:
                        self.margin_path.append(able_draw)

        # last check
        pairs = list(itertools.product(cent_lines, self.margin_path))
        # print(pairs)
        for pair in pairs:
            # print("pair : {}".format(pair))
            margin_line = pair[1]
            cent_line = pair[0]

            A = [self.pos[cent_line[0]], self.pos[cent_line[1]]]
            B = [self.pos[margin_line[0]], self.pos[margin_line[1]]]
            # print("{} - {}".format(A, B))
            flag = is_intersected(A, B)

            if is_intersected(A, B):
                # print("is_intersected: {}". format(flag))
                # print(margin_line)
                self.margin_path.remove(margin_line)

        return list(set(self.margin_path))

    def softLeftRight(self, list1, list2):
        a = b = (0, 0)
        current_index = self.listPoint[0]
        target_index = self.listPoint[1]
        next_ = None
        list_margin = []
        for index, obj in enumerate(self.listPoint):
            if index < len(self.listPoint) - 1:
                next_ = self.listPoint[index + 1]
                if not check4ways(next_, self.margin):
                    current_index = obj
                    target_index = next_
                    break

        current = self.pos[current_index]
        target = self.pos[target_index]

        if self.margin[target_index][0] in list1:
            a = self.pos[self.margin[target_index][0]]
            b = self.pos[self.margin[target_index][1]]
        else:
            a = self.pos[self.margin[target_index][1]]
            b = self.pos[self.margin[target_index][0]]
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

    def getMarginPoint(self):
        # listP: list các điểm xuất hiện 1 lần trong tập cạnh
        listP = []
        for subpath in self.margin_path:
            for point in subpath:
                if checkStartEndPoint(point, self.margin_path):
                    listP.append(point)
        start = getStartPoint(listP, self.margin)
        margin_point_index_1 = getMarginLine(start[0], self.margin_path)
        margin_point_index_2 = getMarginLine(start[1], self.margin_path)
        left_point_index, right_point_index = self.softLeftRight(
            margin_point_index_1, margin_point_index_2)
        self.left_margin_point = converIndexToNavs(left_point_index, self.pos)
        self.right_margin_point = converIndexToNavs(
            right_point_index, self.pos)
        print("ID ĐIỂM LỀ TRÁI: ", left_point_index)
        print("------------------------------------------------------------")
        print("ID ĐIỂM LỀ PHẢI: ", right_point_index)
        print("------------------------------------------------------------")
        return self.left_margin_point, self.right_margin_point
