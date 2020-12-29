import math
import numpy as np
import itertools

PI = math.pi

# pos = {
#     1: (164, 179),
#     20: (183, 230),
#     19: (201, 284),
#     2: (291, 147),
#     3: (357, 132),
#     21: (314, 182),
#     5: (321, 255),
#     4: (401, 212),
#     10: (471, 95),
#     12: (482, 38),
#     25: (521, 48),
#     13: (561, 32),
#     11: (549, 71),
#     22: (530, 119),
#     15: (494, 176),
#     16: (573, 165),
# }

# margin = {20: [1, 19], 21: [2, 3, 4, 5], 22: [10, 11, 16, 15], 25: [12, 13]}

# path = [20, 21, 22, 25]

pos = {34: (1380, 1518), 124: (1398, 1494), 214: (1362, 1542), 33: (1674, 1608), 123: (1704, 1590), 213: (
    1662, 1578), 281: (1644, 1626), 309: (1692, 1644), 69: (1578, 1932), 159: (1596, 1938), 249: (1554, 1926)}
path = [34, 33, 69]
margin = {34: [124, 214], 33: [123, 213, 281, 309], 69: [159, 249]}
path_result: [(124, 213), (214, 281), (123, 213), (123, 309),
              (309, 159), (281, 249), (123, 213)]
# ID ĐIỂM LỀ TRÁI:  [124, 213]
# ID ĐIỂM LỀ PHẢI:  [214, 281, 249]

margin_path = []
left_margin_point = []
right_margin_point = []


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
print("MARGIN PATH: ", margin_path)
print("------------------------------------------------------------")
left_margin_point, right_margin_point = getMarginPoint(
    margin, margin_path, path, pos)


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


def getInitProp(listPoint, pos):
    a = listPoint[0]
    b = listPoint[1]
    alpha = math.atan2(pos[b][1] - pos[a][1], pos[b][0] - pos[a][0])
    return pos[a], alpha
