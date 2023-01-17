import collections


def moduels_list2dict(moduels):
    moduels_dict = collections.OrderedDict()
    heads = moduels.pop(0)  # ['ID', 'TYPE', 'NAME', 'STATUS', 'TAG', 'INCLUDE', 'DESCRIPTION']
    for i, head in enumerate(heads):
        content = [f'{x[i]}' for x in moduels]
        moduels_dict[head] = content

    return moduels_dict

