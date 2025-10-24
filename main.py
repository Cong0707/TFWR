from TFWR import *

while True:
	for i in range(get_world_size()):
		move(East)
		for j in range(get_world_size()):
			move(North)
			if can_harvest():
				harvest()
				if i == 0:
					plant(Entities.Bush)
				elif i == 1:
					plant(Entities.Carrot)
			if get_water() <= 0.8:
				use_item(Items.Water)