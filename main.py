while True:
	for i in range(get_world_size()):
		move(East)
		for j in range(get_world_size()):
			move(North)
			if can_harvest():
				harvest()
				plant(Entities.Bush)