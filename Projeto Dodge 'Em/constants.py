import pygame
from itertools import product
from time import perf_counter

with open("settings.txt", "r") as settings:
	settings_str = settings.read()
	settings_list = settings_str.split("\n")
	num = settings_list[0]
	try:
		level_i_o = int(settings_list[0])
		language_i_o = settings_list[1]
	except ValueError:
		level_i_o = 1
		language_i_o = "pt"


#Constantes do Jogo
clock = pygame.time.Clock()

screen_size = (800, 600)
car_size = (24, 32)
center = (400, 338)

init_time = 1

screen = pygame.display.set_mode(screen_size)

pygame.init()

# Imagens 
menu = pygame.image.load("menu/menu.png")
background = pygame.image.load("jogo/fundo.jpg")
background_white = pygame.image.load("jogo/fundo_branco.jpg")

coin_color = (188, 46, 48)

y_car_img = pygame.image.load("jogo/carro_amarelo.png")
y_car_img.set_colorkey((0, 255, 0))
b_car_img = pygame.image.load("jogo/carro_azul.png")
b_car_img.set_colorkey((0, 255, 0))	

turn = lambda x: pygame.transform.rotate(x, 90)
y_vertical = turn(y_car_img)
y_horizontal = y_car_img
b_vertical = turn(b_car_img)
b_horizontal = b_car_img	

cars_images = {('yellow car', 'h'): y_horizontal, ('yellow car', 'v'): y_vertical, ('blue car', 'h'): b_horizontal, ('blue car', 'v'): b_vertical}

# Constantes dos Carros e Pistas
y_directions = ('up', 'left', 'down', 'right')
b_directions = ('down', 'right', 'up', 'left')

track_width = (57, 80)

				
tracks_center = tuple((center[0] + 97 + track_width[1] * x, center[1] - 72 - track_width[0] * x, center[0] - 122 - track_width[1] * x, center[1] + 47 + track_width[0] * x) 
				for x in list(range(4)))

# Cada track tem (coordenada do inicio da largura, coordenada do fim da largura), para cada lado
tracks = tuple(tuple(((line + 1 - track_width[1]/2, line + track_width[1]/2) if i % 2 == 0 else (line + 1 - track_width[0]/2, line + track_width[0]/2)) for  i, line in enumerate(track)) for track in tracks_center)
				
open_spaces = ((tracks_center[0][2]+42, tracks_center[0][0]-18), (tracks_center[0][1]+18, tracks_center[0][3] - 5))
b_open_extra = 20
b_open_spaces = ((open_spaces[0][0] + b_open_extra, open_spaces[0][1] - b_open_extra), (open_spaces[1][0], open_spaces[1][1]))
inner_square = open_spaces

#Moedas
vertical = [line for track in tracks_center for i, line in enumerate(track) if i % 2 == 0]	
horizontal = [line for track in tracks_center for i, line in enumerate(track) if i % 2 == 1]
combinations =  list(product(vertical, horizontal))

#Menu
languages = ["pt", "en"]
buttons_dict_raw = {"pt": ["jogar.png", "nivel.png", "opcoes.png", "sair.png"], "en": ["play.png", "level.png", "options.png", "quit.png"]}
buttons_dict = {lng: [pygame.image.load("menu/" + el) for el in lst] for lng, lst in buttons_dict_raw.items()}

level_img_list = [pygame.image.load("menu/" + str(vv + 1) + ".png") for vv in range(3)]
languages_img = {lng: pygame.image.load("menu/" + lng + ".png") for lng in languages}
controls = {"pt": pygame.image.load("menu/controlos.png"), "en": pygame.image.load("menu/controls.png")}
controls_panel = {"pt": pygame.image.load("menu/controlos_menu.png"), "en": pygame.image.load("menu/controls_menu.png")}
