from . import mm_quadrant_decide


def modal_update(modals, modals_new, decide_point, p_x, p_y):
    """

    :param modals: list ['vis', 'ir', ...]  # 全部
    :param modals_new: list ['vis', 'ir', ...] # 当前选中的
    :param decide_point:
    :param p_x:
    :param p_y:
    :return:
    """

    if modals_new is None:
        quad = mm_quadrant_decide.quad_decide(decide_point, p_x, p_y)
        modal = modals[quad]
    else:
        if len(modals_new) == 1:
            modal = modals_new[0]
        elif len(modals_new) == 2:
            if max(p_x) < decide_point[0]:
                modal = modals_new[0]
            else:
                modal = modals_new[1]
        else:
            quad = mm_quadrant_decide.quad_decide(decide_point, p_x, p_y)
            modal = modals_new[quad]

    return modal
