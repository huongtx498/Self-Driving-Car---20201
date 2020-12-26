import math
import numpy as np
import itertools

# pos = {1: (164, 179), 20: (183, 230), 19: (201, 284), 2: (291, 147), 3: (357, 132), 21: (314, 182), 5: (321, 255), 4: (401, 212),
#        10: (471, 95), 12: (482, 38), 25: (521, 48), 13: (561, 32), 11: (549, 71), 22: (530, 119), 15: (494, 176), 16: (573, 165)}

# margin = {20: [1, 19], 21: [2, 3, 4, 5], 22: [10, 11, 16, 15], 25: [12, 13]}

# path = [20, 21, 22, 25]


pos = {3: (2328, 2688), 93: (2358, 2664), 183: (2328, 2736), 4: (2022, 2598), 94: (2064, 2568), 184: (2040, 2646), 272: (1986, 2628),
       300: (2010, 2550), 18: (1848, 2538), 108: (1860, 2508), 198: (1824, 2574), 19: (1602, 2460), 109: (1614, 2430), 199: (1566, 2496), 20: (1416, 2406), 110: (1458, 2376), 200: (1434, 2454), 277: (1380, 2436), 305: (1404, 2358), 17: (1374, 2538), 107: (1398, 2538), 197: (1350, 2532)}

margin = {3: [93, 183], 4: [94, 184, 272, 300], 18: [108, 198],
          19: [109, 199], 20: [110, 200, 277, 305], 17: [107, 197]}

path = [3, 4, 18, 19, 20, 17]

margin_path = []
margin_point1 = []
margin_point2 = []


def draw_margin(path, margin, pos):
    margin_path = []
    cent_lines = []
    for i in range(len(path) - 1):
        # print("check {} - {}".format(path[i], path[i + 1]))
        cent_lines.append((path[i], path[i + 1]))
        pos_1 = pos[path[i]]
        pos_2 = pos[path[i + 1]]
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
        margin_1 = margin[path[i]]
        # print("margin1: {}".format(margin_1))
        margin_2 = margin[path[i + 1]]
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

        margin_p_with_dist = [(item, dist_point_point(
            pos[item[0]], pos[item[1]])) for item in margin_p]
        margin_n_with_dist = [(item, dist_point_point(
            pos[item[0]], pos[item[1]])) for item in margin_n]

        margin_p_with_dist.sort(key=lambda x: x[1])
        margin_n_with_dist.sort(key=lambda x: x[1])
        # print("margin_p_with_dist: {}, margin_n_with_dist: {}".format(
        #     margin_p_with_dist, margin_n_with_dist))

        num_point = len(margin_1p) + len(margin_2p)
        # print("num_point: {}".format(num_point))
        able_draw_p = [item[0] for item in margin_p_with_dist[:num_point - 1]]
        margin_path.extend(able_draw_p)
        able_draw_n = [item[0] for item in margin_n_with_dist[:num_point - 1]]
        margin_path.extend(able_draw_n)

        if len(margin[path[i]]) == 4:
            for j in range(3):
                able_draw = (margin[path[i]][j], margin[path[i]][j + 1])
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
    return abs(B[0] * pos_a[0] + B[1] * pos_a[1] + B[2]) / math.sqrt(B[0]**2 + B[1]**2)


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
    return math.sqrt((pos_a[0] - pos_b[0])**2 + (pos_a[1] - pos_b[1])**2)


def is_intersected(A, B):
    A_0 = A[0]
    A_1 = A[1]
    B_0 = B[0]
    B_1 = B[1]

    dA = linear(A_0, A_1)
    dB = linear(B_0, B_1)
    x = intersect_point(dA, dB)

    dist_a = dist_point_point(x, A_0) + dist_point_point(x, A_1)
    dist_b = dist_point_point(x, B_0) + dist_point_point(x, B_1)

    eps = 0.1
    if (abs(dist_point_point(A_0, A_1) - dist_a) < eps) and (abs(dist_point_point(B_0, B_1) - dist_b) < eps):
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


def getMarginPoint(margin, margin_path):
    listP = []
    for path in margin_path:
        for point in path:
            if checkStartEndPoint(point, margin_path):
                listP.append(point)
    start = getStartPoint(listP, margin)
    margin_point1 = getMarginLine(start[0], margin_path)
    margin_point2 = getMarginLine(start[1], margin_path)
    return margin_point1, margin_point2


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


margin_path = draw_margin(path, margin, pos)
margin_point1, margin_point2 = getMarginPoint(margin, margin_path)
print(margin_point1)
print(margin_point2)
