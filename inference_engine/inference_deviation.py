from fuzzy_dependency.fz_dependency import *
from rule.read_rule import read_rule_deviation

class DeviationDeductive:
    def __init__(self):
        self.rules = read_rule_deviation()


    def cal_arguments(self, deviation):
        for rule in self.rules:
            if deviation[0] == rule[0]:
                min_arg = round(deviation[1], 10)
                label = rule[1]
                new_arguments = []
                if label == 'hardright':
                    if min_arg == 1:
                        new_arguments.append(1.75/2)
                    elif 0 < min_arg <1:
                        new_arguments.append(0.15 * min_arg + 0.6)
                if label == 'right':
                    if min_arg == 1:
                        new_arguments.append(0.6)
                    elif 0 < min_arg <1:
                        new_arguments.append(0.1 * min_arg + 0.5)
                        new_arguments.append((0.75 - 0.15 * min_arg))
                if label == 'straight':
                    if min_arg == 1:
                        new_arguments.append(0.5)
                    elif 0 <= min_arg <1:
                        new_arguments.append(0.1 * min_arg + 0.4)
                        new_arguments.append((0.6 - 0.1 * min_arg))
                if label == 'left':
                    if min_arg == 1:
                        new_arguments.append(0.4)
                    elif 0 <= min_arg <1:
                        new_arguments.append(0.15 * min_arg + 0.25)
                        new_arguments.append((0.5 - 0.1 * min_arg))
                if label == 'hardleft':
                    if min_arg == 1:
                        new_arguments.append(0.25/2)
                    elif 0 < min_arg <1:
                        new_arguments.append(0.4 - 0.15 * min_arg)
                # print('gia tri', sum(new_arguments)/len(new_arguments), 're sang', label, 'do thuoc', min_arg)
                return [sum(new_arguments)/len(new_arguments), label, min_arg]
        return [0.5, 'straight', 1]

    def steering_infe(self, deviation):
        deviation_depens = cal_deviation_depen(deviation)
        devi_total = 0
        weight_total = 0
        for deviation_depen in deviation_depens:
            arguments = self.cal_arguments(deviation_depen)
            devi, weight = arguments[0], arguments[2]
            devi_total += devi * weight
            weight_total += weight
        return round(devi_total / weight_total, 3)


# a = DeviationDeductive()
# print(a.steering_infe(deviation=0))

