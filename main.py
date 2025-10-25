from TFWR import *

entityToItem = {Entities.Pumpkin:Items.Pumpkin, Entities.Tree:Items.Wood, Entities.Bush:Items.Wood,
                Entities.Grass:Items.Hay, Entities.Carrot:Items.Carrot}

xType = [Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin,Entities.Pumpkin,
         Entities.Pumpkin, Entities.Pumpkin, Entities.Carrot,Entities.Carrot,
         Entities.Tree, Entities.Tree, Entities.Tree,Entities.Tree]

def calculateType():
    allTypes = [Entities.Carrot, Entities.Tree, Entities.Grass, Entities.Pumpkin]
    def num(entity):
        return num_items(entityToItem[entity])
    def sort(allTypes):
        a = list(allTypes)  # 复制，避免修改原列表
        n = len(a)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if num(a[j]) < num(a[min_idx]):
                    min_idx = j
            if min_idx != i:
                a[i], a[min_idx] = a[min_idx], a[i]
        return a
    sorted_allTypes = sort(allTypes)
    world_size = get_world_size()

    topOne = sorted_allTypes[0]
    topTwo = sorted_allTypes[1]
    topThree = sorted_allTypes[2]

    end1 = world_size / 2
    end2 = end1 + world_size / 4
    end3 = end2 + world_size / 8

    for i in range(end1):
        xType[i] = topOne

    for i in range(end1, end2):
        xType[i] = topTwo

    for i in range(end2, end3):
        xType[i] = topThree

    quick_print(xType)


def fit(types):
    if (types == Entities.Carrot or types == Entities.Pumpkin) and get_ground_type() != Grounds.Soil:
        till()
    elif (types != Entities.Carrot and types != Entities.Pumpkin) and get_ground_type() == Grounds.Soil:
        till()

def moves(x, y):
    while get_pos_x() > x:
        move(West)
    while get_pos_y() > y:
        move(South)
    while get_pos_x() < x:
        move(East)
    while get_pos_y() < y:
        move(North)

def checkPumpkin():
    #定位
    x = get_pos_x()
    y = get_pos_y()
    #确定左边界
    if xType[x - 1] == Entities.Pumpkin and x != 0:
        return
    #确定右边不为其他植物
    if xType[x + 1] != Entities.Pumpkin:
        return
    size = 0  # 距离计数
    while x + size < len(xType) and xType[x + size] == Entities.Pumpkin:
        size += 1
    #确定下边界
    if (y % size) != 0:
        return
    #预种一遍
    for i in range(size):
        for j in range(size):
            if i % 2 == 0:
                moves(x + i, y + j)
            else:
                moves(x + i, y + (size - 1 - j))

            harvest()
            fit(Entities.Pumpkin)
            plant(Entities.Pumpkin)

    #检查一遍
    xt = []

    for i in range(size):
        for j in range(size):
            tox = x + i
            if i % 2 == 0:
                toy = y + j
            else:
                toy = y + (size - 1 - j)

            moves(tox, toy)

            if get_entity_type() != Entities.Pumpkin or not can_harvest():
                xt.append((tox, toy))

    #开始检查南瓜是否完整
    full = False
    while not full:
        full = True
        for i in xt:
            badx = i[0]
            bady = i[1]
            moves(badx, bady)
            if get_entity_type() != Entities.Pumpkin:
                harvest()
                fit(Entities.Pumpkin)
                plant(Entities.Pumpkin)
                full = False
                continue
            elif not can_harvest():
                full = False
                continue
            elif get_entity_type() == Entities.Pumpkin and can_harvest():
                xt.remove(i)
                continue
    moves(x, y)
    harvest()

def checkTree():
    x = get_pos_x()
    y = get_pos_y()
    if can_harvest():
        harvest()
    entity = get_entity_type()
    if entity != Entities.Tree or entity != Entities.Grass or entity != Entities.Carrot:
        harvest()
    if x % 2 == 0:
        if y % 2 == 0:
            plant(Entities.Tree)
        else:
            fit(Entities.Grass)
            plant(Entities.Grass)
    else:
        if y % 2 == 1:
            plant(Entities.Tree)
        else:
            fit(Entities.Carrot)
            plant(Entities.Carrot)


while True:
    moves(0, 0)
    #calculateType()

    for i in range(get_world_size()):
        for j in range(get_world_size()):
            type = xType[get_pos_x()]
            fit(type)
            if type == Entities.Pumpkin:
                checkPumpkin()
            elif type == Entities.Tree:
                checkTree()
            else:
                harvest()
                plant(type)
            if get_water() <= 0.8:
                use_item(Items.Water)

            move(North)
        move(East)