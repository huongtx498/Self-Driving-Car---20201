import math

# deviation
def deviation_veleft(x):
    if 0 <= x <= 0.25:
        return 1.0
    if 0.25 < x < 0.4:
        return (0.4 - x) / 0.15
    return 0.0

def deviation_veright(x):
    if 0.75 <= x <= 1.0:
        return 1.0
    if 0.6 < x < 0.75:
        return (x - 0.6) / 0.15
    return 0.0

def deviation_left(x):
    if 0.25 <= x <= 0.4:
        return (x - 0.25) / 0.15
    if 0.4 < x <= 0.5:
        return (0.5 - x) / 0.1
    return 0.0

def deviation_midle(x):
    if 0.4 <= x <= 0.5:
        return (x - 0.4) / 0.1
    if 0.5 < x <= 0.6:
        return (0.6 - x) / 0.1
    return 0.0

def deviation_right(x):
    if 0.5 <= x <= 0.6:
        return (x - 0.5) / 0.1
    if 0.6 < x <= 0.75:
        return (0.75 - x) / 0.15
    return 0.0


# lamp dependency
def lamp_less_red(time):
    if time >= 0.9:
        return 1.0
    if 0.8 <= time <= 0.9:
        return (time - 0.8) / 0.1
    return 0.0

def lamp_red(time):
    if 0.6 <= time <= 0.7:
        return (time - 0.6) / 0.1
    if 0.7 <= time <= 0.8:
        return 1
    if 0.8 < time <= 0.9:
        return (0.9 - time) / 0.1
    return 0.0

def lamp_less_green(time):
    if 0.3 <= time <= 0.4:
        return (time - 0.3) / 0.1
    if 0.4 <= time <= 0.5:
        return (0.5 - time) / 0.1
    return 0.0

def lamp_green(time):
    if time <= 0.2:
        return 1.0
    if 0.2 <= time <= 0.4:
        return (0.4 - time) / 0.2
    return 0.0

def lamp_yellow(time):
    if 0.45 <= time <= 0.55:
        return (time - 0.45) / 0.1
    if 0.55 <= time <= 0.65:
        return (0.65 - time) / 0.1
    return 0.0

#distance
def distance_near(x):
    if 0.0 <= x <= 10.0:
        return 1.0
    if 10.0 < x <= 40.0:
        return (40.0 - x) / 30.0
    return 0.0

def distance_medium(x):
    if 10.0 <= x <= 25.0:
        return (x - 10.0) / 15.0
    if 25.0 < x <= 50.0:
        return 1
    if 50.0 < x <= 75.0:
        return (75.0 - x) / 25.0
    return 0.0

def distance_far(x):
    if 50.0 <= x < 75.0:
        return (x - 50.0) / 25.0
    if x >= 75.0:
        return 1
    return 0.0

# calculate dependency
def cal_deviation_depen(x):
    deviation  = []
    if deviation_left(x) > 0:
        deviation.append(('left', deviation_left(x)))
    if deviation_midle(x) > 0:
        deviation.append(('midle', deviation_midle(x)))
    if deviation_right(x) > 0:
        deviation.append(('right', deviation_right(x)))
    if deviation_veleft(x) > 0:
        deviation.append(('farleft', deviation_veleft(x)))
    if deviation_veright(x) > 0:
        deviation.append(('farright', deviation_veright(x)))
    return deviation

def cal_lamp_depen(x):
    lamp = []
    if lamp_red(x) > 0:
        lamp.append(('red', lamp_red(x)))
    if lamp_green(x) > 0:
        lamp.append(('green', lamp_green(x)))
    if lamp_yellow(x) > 0:
        lamp.append(('yellow', lamp_yellow(x)))
    if lamp_less_red(x) > 0:
        lamp.append(('less_red', lamp_less_red(x)))
    if lamp_less_green(x) > 0:
        lamp.append(('less_green', lamp_less_green(x)))
    return lamp

def cal_distance_depen(x):
    distance = []
    if distance_far(x) > 0:
        distance.append(('far', distance_far(x)))
    if distance_near(x) > 0:
        distance.append(('near', distance_near(x)))
    if distance_medium(x) > 0:
        distance.append(('medium', distance_medium(x)))
    return distance