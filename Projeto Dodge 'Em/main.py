import pygame
import random
from itertools import product
from time import perf_counter

from functions import *
from constants import *

def reset():
	global y_car
	y_car = ['yellow car', y_car_img, 460, screen_size[0] - track_width[0]/2, "right"]
	global b_car
	b_car = ['blue car', b_car_img, 300, screen_size[0] - track_width[0]/2, "left"]
	global y_track_now
	y_track_now = 3
	global b_track_now
	b_track_now = 3
	global coins
	coins = combinations.copy()
	global front_speed
	front_speed = 0.3
	global explosion_i
	explosion_i = 1
	global turn_coins_caught
	turn_coins_caught = 0
	global t0
	t0 = perf_counter()
			
	# Nota: Eu sei que nao se deve utilizar variaveis globais, mas como torna o meu codigo muito mais simples, decidi utiliza-las na mesma

def main():
	level = level_i_o
	language = language_i_o
	
	l_l = [level, language]
	
	running = True
	
	while running:
		
		in_menu = True
		in_game = True
		in_options = False
		in_controls = False
		
		button_int = 0
		options_button = 0
		
		# Variaveis dos Carros
		global y_track_now
		y_track_now = 3
		global b_track_now
		b_track_now = 3
		
		y_locked_track = 3
		
		# Speeds
		global front_speed
		front_speed = 0.35
		double_speed = False
		side_speed = 0.35
		side_movement = False
		
		pass_manesage_move = False
		
		# Explosion
		explosion = False
		global explosion_i
		explosion_i = 1

		# Cada carro tem o seguite formato: car = [name, img, x, y, direction]
		global y_car
		y_car = ['yellow car', y_car_img, 460, screen_size[0] - track_width[0]/2, "right"]
		global b_car
		b_car = ['blue car', b_car_img, 300, screen_size[0] - track_width[0]/2, "left"]

		# Moedas
		global coins
		coins = combinations.copy()

		coins_caught = 0
		global turn_coins_caught
		turn_coins_caught = 0
		total_coins = 64
		celebration = False
		
		two_cars = False

		lives = 3
							
		# Teclado
		esc_key = False
		enter_key = False
		left_key = False
		right_key = False
		up_key = False
		down_key = False
		keys = [left_key, right_key, up_key, down_key]
		opposites = {left_key: right_key, up_key: down_key, right_key: left_key, down_key: up_key}
			
		global t0
		t0 = perf_counter()
		
		# Loop do jogo
		while in_game:
			# O jogo esta a correr
		
			
			# 1. Lidar com eventos (teclado) ---------------------------------------------------------------------------
			esc_key = False
			enter_key = False
			 
			for ev in pygame.event.get():
				if ev.type == pygame.QUIT:
					running = False
					in_game = False
				elif ev.type == pygame.KEYDOWN:
					if ev.key == pygame.K_ESCAPE:
						esc_key = True
					if ev.key == pygame.K_SPACE:
						double_speed = True
					if ev.key == pygame.K_LEFT:
						left_key = True
					elif ev.key == pygame.K_RIGHT:
						right_key = True
					elif ev.key == pygame.K_UP:
						up_key = True
					elif ev.key == pygame.K_DOWN:
						down_key = True
					elif ev.key == pygame.K_RETURN:
						enter_key = True
						
				elif ev.type == pygame.KEYUP:
					if ev.key == pygame.K_SPACE:
						double_speed = False
					if ev.key == pygame.K_LEFT:
						left_key = False
						side_movement = False
					elif ev.key == pygame.K_RIGHT:
						right_key = False
						side_movement = False
					elif ev.key == pygame.K_UP:
						up_key = False
						side_movement = False
					elif ev.key == pygame.K_DOWN:
						down_key = False
						side_movement = False
			
			
			# 2. Logica do jogo (fisica, etc) --------------------------------------------------------------------------
			dt = clock.tick()
			
			t1 = perf_counter()
			if t1-t0 >= init_time:
				if side_movement:
					if y_car[4] == "up" or y_car[4] == "down":
						move(y_car, (front_speed/1.55) * dt)
					elif y_car[4] == "left" or y_car[4] == "right":
						move(y_car, front_speed * dt)
					
				else:
					move(y_car, front_speed * dt * (int(double_speed) + 1))
					
				move(b_car, front_speed * dt)
				
			else:
				move(y_car, 0)
				move(b_car, 0)
			
			# If car in the inner square
			if in_inner_square(y_car, open_spaces):
				y_track_now = 0
				if y_car[4] == "up":
					y_car[2] = tracks_center[y_track_now][0]
				elif y_car[4] == "left":
					y_car[3] = tracks_center[y_track_now][1]
				elif y_car[4] == "down":
					y_car[2] = tracks_center[y_track_now][2]
				elif y_car[4] == "right":
					y_car[3] = tracks_center[y_track_now][3]
				
			
			# In the free moving space
			# If car in open areas
			elif in_open_spaces(y_car, open_spaces) and not in_menu and not in_options and not in_controls:
					
				if left_key == True and not is_horizontal(y_car):
					side_movement = True
					move_abs(y_car, -side_speed * dt, 'x')
				
				if right_key == True and not is_horizontal(y_car):
					side_movement = True
					move_abs(y_car, side_speed * dt, 'x')
					
				if up_key == True and is_horizontal(y_car):
					side_movement = True
					move_abs(y_car, -side_speed * dt, 'y')
					
				if down_key == True and is_horizontal(y_car):
					side_movement = True
					move_abs(y_car, side_speed * dt, 'y')
					
					
					
			# In the tracks
			else:
				y_locked_track = y_track_now
				if y_car[4] == "up":
					y_track_now = auto_set_track(y_car[2], "up", y_track_now, y_directions)
					y_car[2] = tracks_center[y_track_now][0]
				elif y_car[4] == "left":
					y_track_now = auto_set_track(y_car[3], "left", y_track_now, y_directions)
					y_car[3] = tracks_center[y_track_now][1]
				elif y_car[4] == "down":
					y_track_now = auto_set_track(y_car[2], "down", y_track_now, y_directions)
					y_car[2] = tracks_center[y_track_now][2]
				elif y_car[4] == "right":
					y_track_now = auto_set_track(y_car[3], "right", y_track_now, y_directions)
					y_car[3] = tracks_center[y_track_now][3]
					
				verify_directions(y_car, y_directions, tracks_center[y_track_now])
			
			
			# Explosion
			if near(y_car[2], b_car[2], 40) and near(y_car[3], b_car[3], 40):
				explosion = True
			
			# Lives
			if (lives == 0 or esc_key) and not in_menu and not in_options and not in_controls:
				in_game = False
			
			# Coins
			for coin in coins:
				if near(y_car[2], coin[0], 20) and near(y_car[3], coin[1], 20):
					coins.remove(coin)
					if not in_menu and not in_options and not in_controls: coins_caught += 1
					turn_coins_caught += 1
					# O jogador apanhou todas a moedas
					if turn_coins_caught == total_coins:
						reset()
						celebration = True
						print(level)
						if level >= 3 and not in_menu and not in_options and not in_controls: two_cars = True
						else: two_cars = False
			
			# "Inteligencia" Carro Azul
			if not level == 1:
				if b_track_now != y_locked_track and in_open_spaces(b_car, b_open_spaces):
					move_side(b_car, get_sign(b_track_now - y_locked_track), (side_speed/2)*dt)
					
				else:
					if b_car[4] == "down":
						b_track_now = auto_set_track(b_car[2], "down", b_track_now, b_directions)
						b_car[2] = tracks_center[b_track_now][0]
					elif b_car[4] == "right":
						b_track_now = auto_set_track(b_car[3], "right", b_track_now, b_directions)
						b_car[3] = tracks_center[b_track_now][1]
					elif b_car[4] == "up":
						b_track_now = auto_set_track(b_car[2], "up", b_track_now, b_directions)
						b_car[2] = tracks_center[b_track_now][2]
					elif b_car[4] == "left":
						b_track_now = auto_set_track(b_car[3], "left", b_track_now, b_directions)
						b_car[3] = tracks_center[b_track_now][3]
						
					verify_directions(b_car, b_directions, tracks_center[b_track_now])
			
			else:
				verify_directions(b_car, b_directions, tracks_center[b_track_now])
				
				
			# Two Cars
			if two_cars:
				b_car_2 = ['blue car 2', b_car_img, screen_size[0] - 25 - b_car[2], screen_size[1] + 50 - b_car[3], "left"] 
				if near(y_car[2], b_car_2[2], 40) and near(y_car[3], b_car_2[3], 40):
					b_car[2] = b_car_2[2]
					b_car[3] = b_car_2[3]
					explosion = True




			# 3. Desenhar no ecra --------------------------------------------------------------------------------------
			screen.blit(background, background.get_rect())
				
			for coin in coins:
				pygame.draw.rect(screen, pygame.Color(coin_color), (coin[0], coin[1] + 8, 20, 7))
			
			if not in_menu and not in_options and not in_controls:
				coins_str = "%03d" % coins_caught
				num1 = pygame.image.load("numeros/" + coins_str[-3] + ".png") #1o digito
				num2 = pygame.image.load("numeros/" + coins_str[-2] + ".png") #2o digito
				num3 = pygame.image.load("numeros/" + coins_str[-1] + ".png") #3o digito
				screen.blit(num1, (500, 20))
				screen.blit(num2, (570, 20))
				screen.blit(num3, (640, 20))
				
				lives_img = pygame.image.load("lives/" + str(lives) + ".png")
				screen.blit(lives_img, (200, 20))
			
			if explosion:
				front_speed = 0 
				
				b_explosion_img = pygame.image.load("explosao/momento" + str(explosion_i) + "_2.png")
				b_explosion_img.set_colorkey((0, 255, 0))
				y_explosion_img = pygame.image.load("explosao/momento" + str(explosion_i) + "_1.png")
				y_explosion_img.set_colorkey((0, 255, 0))
				screen.blit(b_explosion_img, (b_car[2]-60, b_car[3]-5))
				screen.blit(y_explosion_img, (y_car[2]-20, y_car[3]-5))
				if not in_menu and not in_options and not in_controls: 
					pygame.display.flip()
					
				if not in_menu and not in_options:
					pygame.time.delay(100)
				
				num_frames = 4 if not in_menu and not in_options and not in_controls else 5
				
				if explosion_i == num_frames:
					if not in_menu and not in_options: pygame.time.delay(200)
					explosion = False
					if lives > 0 and not in_menu and not in_options and not in_controls:
						lives -= 1
					reset()
					
				explosion_i += 1
			
			else:
				screen.blit(y_car[1], (y_car[2], y_car[3]))
				screen.blit(b_car[1], (b_car[2], b_car[3]))
				if two_cars:
					screen.blit(b_car[1], (screen_size[0] - 25 - b_car[2], screen_size[1] + 50 - b_car[3]))
					
			if celebration == True:
				screen.blit(background_white, background_white.get_rect())
				screen.blit(y_car[1], (y_car[2], y_car[3]))
				screen.blit(b_car[1], (b_car[2], b_car[3]))
				pygame.display.flip()
				pygame.time.wait(600)
				celebration = False
				
			# 4. Menu --------------------------------------------------------------------------------------------------
			if in_menu:
				# O jogo esta no menu
				for button in buttons_dict[language]:
					screen.blit(button, button.get_rect())
					
				level_img = level_img_list[level - 1]
				screen.blit(level_img, level_img.get_rect())
				
				screen.blit(menu, menu.get_rect())
				
				screen.blit(buttons_dict[language][button_int], buttons_dict[language][button_int].get_rect())
				
				if down_key: 
					button_int = (button_int + 1) % 4
					down_key = False
				elif up_key: 
					button_int = (button_int - 1) % 4
					up_key = False
				
				if button_int == 0: #PLAY ou JOGAR
					if enter_key:
						in_menu = False
						reset()
					
				elif button_int == 1: #LEVEL ou NIVEL
					screen.blit(level_img, level_img.get_rect())
					if enter_key:
						level = (level) % 3 + 1
						print(level)
						l_l = [level, language]
					
				elif button_int == 2: #OPTIONS ou OPCOES
					if enter_key:
						in_options = True
						in_menu = False
						enter_key = False
					
				elif button_int == 3: #QUIT ou SAIR
					if enter_key:
						in_game = False
						running = False
				
			if in_options:
				screen.blit(languages_img[language], languages_img[language].get_rect())
				screen.blit(controls[language], controls[language].get_rect())
				screen.blit(menu, menu.get_rect())
				
				if down_key: 
					options_button = (options_button + 1) % 2
					down_key = False
				elif up_key: 
					options_button = (options_button - 1) % 2
					up_key = False
				
				if options_button == 0: #LANGUAGE ou LINGUA
					screen.blit(languages_img[language], languages_img[language].get_rect())
					if enter_key:
						language = languages[(languages.index(language) + 1) % len(language)]
						l_l = [level, language]
					
				elif options_button == 1: #LEVEL ou NIVEL
					screen.blit(controls[language], controls[language].get_rect())
					if enter_key:
						in_controls = True
						in_options = False
				
				if esc_key:
					in_menu = True
					in_options = False
					options_button = 0
					
			if in_controls:
				screen.blit(controls_panel[language], controls_panel[language].get_rect())
		
				if esc_key:
					in_options = True
					in_controls = False
				
			
			pygame.display.flip()
			
	with open("settings.txt", "w") as settings:
		settings.write(str(l_l[0]))
		settings.write("\n")
		settings.write(l_l[1])

	
	pygame.quit()

if __name__ == "__main__":
    main()

