from fuzzy_dependency.fz_dependency import *
from rule.read_rule import read_rule_speed_lamp, read_rule_speed_stone

class Lamp_speed_Deductive:
    def __init__(self):
        self.rules = read_rule_speed_lamp()

    def cal_argument(self, lightstatus, deviation, distance):
        for rule in self.rules:
            if lightstatus[0] == rule[0] and distance[0] == rule[1] and deviation[0] == rule[2]:
                depens = [lightstatus[1], distance[1], deviation[1]]
                min_arg = min(depens)
                label = rule[3]
                new_argument = None
                if label == 'stop':
                    if min_arg == 1:
                        new_argument = 0.0
                    elif 0 < min_arg < 1:
                        new_argument = (0.05 - 0.05 * min_arg) / 2
                if label == 'slower':
                    if min_arg == 1:
                        new_argument =  0.25
                    elif 0 < min_arg < 1:
                        new_argument = ((0.25 * min_arg + 0.0) + (0.5 - 0.25 * min_arg)) / 2
                if label == 'slow':
                    if min_arg == 1:
                        new_argument = 0.6
                    elif 0 < min_arg < 1:
                        new_argument = ((0.3 * min_arg + 0.3) + (0.8 - 0.2 * min_arg)) / 2
                if label == 'medium':
                    if min_arg == 1:
                        new_argument = 0.95
                    elif 0 < min_arg < 1:
                        new_argument = ((0.2 * min_arg + 0.7) + 1) / 2
                # print('gia tri', new_argument, 'label_speed', label, 'do_thuoc speed', min_arg, 'depen', depens)
                return [new_argument, label, min_arg]
        return [0.95, 'medium', 1]
        # return [0, 'stop', 1]

    def speed_lamp_infe(self, lightstatus, deviation, distance):
        lightstatuses = cal_lamp_depen(lightstatus)
        deviations = cal_deviation_depen(deviation)
        distances = cal_distance_depen(distance)
        speed_total = 0
        weight_total = 0
        for lightstatus in lightstatuses:
            for distance in distances:
                for deviation in deviations:
                    argument = self.cal_argument(lightstatus, deviation, distance)
                    speed, wei = argument[0], argument[2]
                    speed_total += speed * wei
                    weight_total += wei
        return round(speed_total / weight_total, 3)

# a = Lamp_speed_Deductive()
# print(a.speed_lamp_infe(0.3, 0.35, 40))

class Stone_speed_Deductive:
    def __init__(self):
        self.rules = read_rule_speed_stone()

    def cal_argument(self, deviation, distance):
        for rule in self.rules:
            if distance[0] == rule[0] and deviation[0] == rule[1]:
                depens = [distance[1], deviation[1]]
                min_arg = round(min(depens), 4)
                label = rule[2]
                if label == 'stop':
                    if min_arg == 1:
                        new_argument = 0.0
                    elif 0 < min_arg < 1:
                        new_argument = (0.05 - 0.05 * min_arg) / 2
                if label == 'slower':
                    if min_arg == 1:
                        new_argument =  0.25
                    elif 0 < min_arg < 1:
                        new_argument = ((0.25 * min_arg + 0.0) + (0.5 - 0.25 * min_arg)) / 2
                if label == 'slow':
                    if min_arg == 1:
                        new_argument = 0.6
                    elif 0 < min_arg < 1:
                        new_argument = ((0.3 * min_arg + 0.3) + (0.8 - 0.2 * min_arg)) / 2
                if label == 'medium':
                    if min_arg == 1:
                        new_argument = 0.95
                    elif 0 < min_arg < 1:
                        new_argument = ((0.2 * min_arg + 0.7) + 1) / 2
                # print(new_argument)
                # print(label)
                # print(min_arg)
                return [new_argument, label, min_arg]

        return [0.95, 'medium', 1]
        # return [0, 'stop', 1]

    def speed_stone_infe(self, deviation, distance):
        deviations = cal_deviation_depen(deviation)
        distances = cal_distance_depen(distance)
        speed_total = 0
        weight_total = 0
        for distance in distances:
            for deviation in deviations:
                argument = self.cal_argument(deviation, distance)
                speed, wei = argument[0], argument[2]
                speed_total += speed * wei
                weight_total += wei
        return round(speed_total / weight_total, 3)

# b = Stone_speed_Deductive()
# print(b.speed_stone_infe(0.5, 45))