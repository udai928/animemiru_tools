#-*- coding:utf-8 -*-

# TODO classのlistでもイイカンジにソートできるようにする
def unique(list_x):
    list_unique = []
    for x in list_x:
        if x not in list_unique:
            list_unique.append(x)
    return list_unique