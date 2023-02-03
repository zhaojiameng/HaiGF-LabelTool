"""
象限判定
"""


def quad_decide(decide_point, x, y):
    if decide_point[1] == 0 and decide_point[0] != 0:
        if max(x) < decide_point[0]:
            quad = 0
        else:
            quad = 1
    elif decide_point[1] == 0 and decide_point[0] == 0:
        quad = 0
    else:
        if max(x) < decide_point[0] and max(y) < decide_point[1]:
            quad = 0
        elif max(x) < decide_point[0] and min(y) > decide_point[1]:
            quad = 2
        elif min(x) > decide_point[0] and max(y) < decide_point[1]:
            quad = 1
        elif min(x) > decide_point[0] and min(y) > decide_point[1]:
            quad = 3
        else:
            raise TypeError(f'Labels crossing modals are forbidden.')

    return quad
