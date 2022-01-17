from constants import *

# Funcoes

def near(value1, value2, units):
	if abs(value1 - value2) < units:
		return True
	return False
	
in_open_spaces = lambda car, open_spaces: (open_spaces[0][0] < car[2] and car[2] < open_spaces[0][1]) or (open_spaces[1][0] < car[3] and car[3] < open_spaces[1][1])
in_inner_square = lambda car, open_spaces: (open_spaces[0][0] < car[2] and car[2] < open_spaces[0][1]) and (open_spaces[1][0] < car[3] and car[3] < open_spaces[1][1])

def verify_directions(car, directions, edges):
	# Cada bloco if ou elif a seguir representa algo do genero:
	#  if coordenada do carro > limite:
	# 	 coordenada do carro = limite para evitar bugs
	# 	 direcao do carro muda para a seguinte na lista
	# 	 imagem do carro vira
	
	x = car[2]
	y = car[3]
		
	if x > edges[0]:
		x = edges[0]
		car[4] = directions[0]
		#car[0] = turn(car[0])
	elif y < edges[1]:
		y = edges[1]
		car[4] = directions[1]
		#car[0] = turn(car[0])
	elif x < edges[2]:
		x = edges[2]
		car[4] = directions[2]
		#car[0] = turn(car[0])
	elif y > edges[3]:
		y = edges[3]
		car[4] = directions[3]
		#car[0] = turn(car[0])
		
	car[2] = x
	car[3] = y
	
def in_track(x, track):
	# ~ print(track[0], "<", x , "<", track[1])
	if track[0] < x and x < track[1]:
		return True
	return False
	
def auto_set_track(x, direction, track_now, directions):
	direction_now = directions.index(direction)
	for i, track in enumerate(tracks):
		if in_track(x, track[direction_now]):
			return i
	return track_now
		
		
def move(car, distance, direction = 0):
	if direction == 0:
		direction = car[4]
		
	if direction == 'up':
		car[3] -= distance
		car[1] = cars_images[(car[0], 'h')]
	elif direction == 'down':
		car[3] += distance
		car[1] = cars_images[(car[0], 'h')]
	elif direction == 'right':
		car[2] += distance
		car[1] = cars_images[(car[0], 'v')]
	elif direction == 'left':
		car[2] -= distance
		car[1] = cars_images[(car[0], 'v')]
		
def move_abs(car, distance, axis):
	if axis == 'x':
		car[2] = car[2] + distance
	elif axis == 'y':
		car[3] = car[3] + distance
		
def move_side(car, relative, distance):
	# relavive = a diferenca entre a track q estamos e a que queremos chegar
	direction = car[4]
	
	if direction == 'up':
		car[2] += distance * relative
	elif direction == 'down':
		car[2] -= distance * relative
	elif direction == 'right':
		car[3] += distance * relative
	elif direction == 'left':
		car[3] -= distance * relative
		
def get_direction(directions, direction_now, bias):
	return directions[(directions.index(direction_now) + bias) % len(directions)]
	
is_horizontal = lambda car: car[4] == 'right' or car[4] == 'left'

def get_sign(num):
	if num < 0: return -1
	elif num > 0: return 1
	else: return 0

def color_combination(color1, color2):
	r, g, b = color1
	r1, g1, b1 = color2
	return ((r1 - r) % 255, (g1 - g) % 255, (b1 - b) % 255)

# Cria um filtro na imagem, subtraindo cada valor do RGB dos pixels da imagem pelo valor no color
def color_filter(surface, color):
	print(color)
	w, h = surface.get_size()
	r, g, b, _ = color
	for x in range(w):
		for y in range(h):
			r1, g1, b1, _1 = surface.get_at((x, y))
			a = surface.get_at((x, y))[3]
			new_color = color_combination((r, g, b), (r1, g1, b1))
			(rn, gn, bn) = new_color
			surface.set_at((x, y), pygame.Color(rn, gn, bn, a))
			
def filter_surfaces(color, *surfaces):
	for surface in surfaces:
		color_filter(surface, pygame.Color(color))
