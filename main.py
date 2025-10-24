from TFWR import *

xType = [Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin]

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
	#开始检查南瓜是否完整
	full = False
	while not full:
		for i in range(size):
			for j in range(size):
				moves(x + i, y + j)
				if get_entity_type() != Entities.Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
					moves(x, y)
					continue
				elif get_entity_type() == Entities.Pumpkin and get_pos_x() == x and get_pos_y() == y:
					full = True
					moves(x, y)
					continue
	moves(x, y)
	harvest()

while True:
	moves(0, 0)

	for i in range(get_world_size()):
		move(East)
		for j in range(get_world_size()):
			move(North)
			type = xType[get_pos_x()]
			fit(type)
			if type == Entities.Pumpkin:
				checkPumpkin()
			elif can_harvest():
				harvest()
				plant(type)
			if get_water() <= 0.8:
				use_item(Items.Water)