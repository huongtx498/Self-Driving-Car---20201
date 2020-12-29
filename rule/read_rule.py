import csv

def read_csv(file):
    out = []
    with open(file) as file:
        data = csv.reader(file)
        for row in data:
            out.append(row)
    return out[1:]

def read_rule_deviation():
    data = read_csv('../rule/rules-deviation.csv')
    deviation_rule = []
    Deviation = []
    Steering = []
    for row in data:
        Deviation.append(row[0])
        Steering.append(row[1])
    for i in range(len(data)):
        deviation_rule.append((Deviation[i], Steering[i]))
    return deviation_rule

def read_rule_speed_lamp():
    speed_lamp_rule = []
    data = read_csv('../rule/rules-speed1.csv')
    LightStatus = [row[0] for row in data]
    Distance = [row[1] for row in data]
    Deviation = [row[2] for row in data]
    Speed = [row[3] for row in data]

    for i in range(len(data)):
        speed_lamp_rule.append((LightStatus[i], Distance[i], Deviation[i], Speed[i]))

    return speed_lamp_rule

def read_rule_speed_stone():
    speed_stone_rule = []
    data = read_csv('../rule/rules-speed2.csv')
    Distance = [row[0] for row in data]
    Deviation = [row[1] for row in data]
    Speed = [row[2] for row in data]

    for i in range(len(data)):
        speed_stone_rule.append((Distance[i], Deviation[i], Speed[i]))
    return speed_stone_rule