from TFWR import *

xType = [Entities.Grass, Entities.Carrot, Entities.Carrot, Entities.Carrot, Entities.Bush, Entities.Bush]

def fit(types):
    if types == Entities.Carrot and get_ground_type() != Grounds.Soil:
        till()
    elif types != Entities.Carrot and get_ground_type() == Grounds.Soil:
        till()

while True:
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

    for i in range(get_world_size()):
        move(East)
        for j in range(get_world_size()):
            move(North)
            x = get_pos_x()
            y = get_pos_y()
            if can_harvest():
                harvest()
                type = xType[x]
                fit(type)
                plant(type)
            if get_water() <= 0.8:
                use_item(Items.Water)