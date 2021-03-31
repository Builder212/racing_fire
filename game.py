import pygame, time, random, pickle, sys

class racing_fire:
	def __init__(self, x=350, y=600):
		pygame.init()

		#display
		pygame.display.set_caption('Racing Fire')
		self.screen = pygame.display.set_mode((x, y))
		self.display_width, self.display_height = x, y
		self.x, self.y = self.display_width*0.45, self.display_height*0.8

		#in game loop variables
		self.running, self.menu, self.game, self.end, self.options = True, True, False, False, False

		#music
		try:
			self.soundtrack = pygame.mixer.music.load("music/racing_fire.mp3")
		except:
			self.soundtrack = pygame.mixer.music.load("music/racing_fire.ogg")

		try:
			with open('data/music.dat', 'rb') as file:
				self.music = pickle.load(file)
		except:
			self.music = 0
			with open('data/music.dat', 'wb') as file:
				pickle.dump(self.music, file)

		#game variables
		self.x_change, self.speed, self.distance, self.y_val = 0, 1, 0, 0

		#font type
		self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

		#grass terrain
		self.grass_terrain = pygame.image.load("textures/scenery/road/grass_background.png").convert_alpha()
		self.drive = pygame.image.load("textures/scenery/road/road_background.png").convert_alpha()
		self.pothole = pygame.image.load("textures/scenery/road/pothole.png").convert_alpha()

		#ice terrain
		self.snow_terrain = pygame.image.load("textures/scenery/ice/snow_background.png").convert_alpha()
		self.ice_road = pygame.image.load("textures/scenery/ice/ice_road_background.png").convert_alpha()
		self.snow_pile = pygame.image.load("textures/scenery/ice/snow_pile.png").convert_alpha()

		#jungle terrain
		self.jungle_terrain = pygame.image.load("textures/scenery/jungle/heavy_grass_background.png").convert_alpha()
		self.dirt_road = pygame.image.load("textures/scenery/jungle/dirt_road_background.png").convert_alpha()
		self.rocks = pygame.image.load("textures/scenery/jungle/rocks.png").convert_alpha()

		#defualt world
		try:
			with open('data/world.dat', 'rb') as file:
				self.world = pickle.load(file)
		except:
			self.world = 0
			with open('data/world.dat', 'wb') as file:
				pickle.dump(self.world, file)

		if self.world == 0:
			self.terrain = self.grass_terrain
			self.road = self.drive
			self.obstacle = self.pothole
		elif self.world == 1:
			self.terrain = self.snow_terrain
			self.road = self.ice_road
			self.obstacle = self.snow_pile
		elif self.world == 2:
			self.terrain = self.jungle_terrain
			self.road = self.dirt_road
			self.obstacle = self.rocks
		else:
			print("Your world.dat file has invalid data.")
			pygame.quit()
			sys.exit()

		#highscore
		try:
			with open('data/highscore.dat', 'rb') as file:
				self.highscore = pickle.load(file)
		except:
			self.highscore = 0
			with open('data/highscore.dat', 'wb') as file:
				pickle.dump(self.highscore, file)

		self.highscore_string = str(self.highscore)
		self.high_score_render = self.font.render(self.highscore_string, True, (255, 255, 255))

		#main menu
		self.start_clicked = pygame.image.load("textures/main_menu/start_selected.png").convert_alpha()
		self.exit_clicked = pygame.image.load("textures/main_menu/exit_selected.png").convert_alpha()
		self.options_clicked = pygame.image.load("textures/main_menu/settings_selected.png").convert_alpha()
		self.menu_background = pygame.image.load("textures/main_menu/menu_background.png").convert_alpha()

		#death screen
		self.menu_clicked = pygame.image.load("textures/exit_menu/back_selected.png").convert_alpha()
		self.death_screen = pygame.image.load("textures/exit_menu/exit_background.png").convert_alpha()

		#settings menu
		self.music_off = pygame.image.load("textures/settings_menu/off_hover.png").convert_alpha()
		self.music_on = pygame.image.load("textures/settings_menu/on_hover.png").convert_alpha()
		self.off_selected = pygame.image.load("textures/settings_menu/off_selected.png").convert_alpha()
		self.on_selected = pygame.image.load("textures/settings_menu/on_selected.png").convert_alpha()
		self.options_exit = pygame.image.load("textures/settings_menu/back_selected.png").convert_alpha()
		self.background_hover = pygame.image.load("textures/settings_menu/hover_background.png").convert_alpha()
		self.selected_background = pygame.image.load("textures/settings_menu/selected_background.png").convert_alpha()
		self.selected_car = pygame.image.load("textures/settings_menu/select_car.png").convert_alpha()
		self.hover_car = pygame.image.load("textures/settings_menu/hover_car.png").convert_alpha()
		self.options_screen = pygame.image.load("textures/settings_menu/settings_background.png").convert_alpha()
		self.more_car_hover = pygame.image.load("textures/settings_menu/more_cars_hover.png").convert_alpha()
		self.more_background_hover = pygame.image.load("textures/settings_menu/more_background_hover.png").convert_alpha()

		#car
		self.firebird = pygame.image.load("textures/cars/firebird.png").convert_alpha()
		self.car1 = pygame.image.load("textures/cars/car-1.png").convert_alpha()
		self.car2 = pygame.image.load("textures/cars/car-2.png").convert_alpha()
		self.car4 = pygame.image.load("textures/cars/car-4.png").convert_alpha()
		self.car5 = pygame.image.load("textures/cars/car-5.png").convert_alpha()
		self.car7 = pygame.image.load("textures/cars/car-7.png").convert_alpha()

		try:
			with open('data/car.dat', 'rb') as file:
				self.car_choice = pickle.load(file)
		except:
			self.car_choice = 0
			with open('data/car.dat', 'wb') as file:
				pickle.dump(self.car_choice, file)

		if self.car_choice == 0:
			self.car = self.firebird
		elif self.car_choice == 1:
			self.car = self.car4
		elif self.car_choice == 2:
			self.car = self.car7
		elif self.car_choice == 3:
			self.car = self.car5
		elif self.car_choice == 4:
			self.car = self.car2
		elif self.car_choice == 5:
			self.car = self.car1
		else:
			print("Your car.dat file has invalid data.")
			pygame.quit()
			sys.exit()

		self.car_hitbox = (self.x, self.y, self.car.get_rect().width, self.car.get_rect().height)

		#obstacle
		self.obstacle_side, self.obstacle_angle = random.randrange(30, 100), random.randrange(0, 360)
		self.obstacle_startx, self.obstacle_starty = random.randrange(25, (self.display_width-25-self.obstacle_side)), -10
		self.obstacle_hitbox = ((self.obstacle_side/2), self.obstacle_startx, self.obstacle_starty)

		self.intro = pygame.image.load("textures/intro/intro.png").convert_alpha()

		self.screen.blit(self.intro, (0,0))
		pygame.display.update()
		pygame.time.wait(5000)

	def main_menu_setup(self):
		self.screen.blits(blit_sequence = ((self.menu_background, (0,0)), (self.high_score_render, (218, 569))))
		pygame.display.update()

	def initial_load(self):
		self.screen.blits(blit_sequence = ((self.terrain, (0,0)), (self.road, (25,0))))

	def move_car(self, x, y):
		self.screen.blit(self.car, (int(x), int(y)))

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.x_change = -.3
				elif event.key == pygame.K_RIGHT:
					self.x_change = .3
				else:
					pass
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					self.x_change = 0
				else:
					pass
			else:
				pass

	def car_onscreen(self):
		if 0 < self.x + self.x_change < 300:
			self.x += self.x_change
		else:
			pass

	def scrolling_road(self):
		y = self.y_val % self.road.get_rect().height
		self.screen.blits(blit_sequence = ((self.terrain, (0, int(y-self.terrain.get_rect().height))), (self.road, (25, int(y-self.road.get_rect().height)))))
		if y < 814:
			self.screen.blits(blit_sequence = ((self.terrain, (0, int(y))), (self.road, (25, int(y)))))
		else:
			pass
		self.y_val += self.speed

	def obstacles(self):
		self.resized_obstacle = pygame.transform.scale(self.obstacle, (self.obstacle_side, self.obstacle_side))
		self.rotated_obstacle = pygame.transform.rotate(self.resized_obstacle, self.obstacle_angle)
		self.screen.blit(self.resized_obstacle, (int(self.obstacle_startx), int(self.obstacle_starty)))
		self.obstacle_starty += self.speed

	def obstacle_onscreen(self):
		if self.obstacle_starty > self.display_height:
			self.obstacle_starty = 0 - self.obstacle_side
			self.obstacle_side, self.obstacle_angle = random.randrange(50, 70), random.randrange(0, 360)
			self.obstacle_startx = random.randrange(25, (self.display_width-25-self.obstacle_side))
		else:
			pass

	def crash(self):
		self.game, self.end = False, True
		self.screen.blit(self.death_screen, (0,0))

		if int(self.distance) >= self.highscore:
			self.highscore = int(self.distance)
			with open('data/highscore.dat', 'wb') as file:
				pickle.dump(self.highscore, file)
		else:
			pass

		self.highscore_string = str(self.highscore)
		self.high_score_render = self.font.render(self.highscore_string, True, (255, 255, 255))
		self.distance_render = self.font.render(str(int(self.distance)), True, (255, 255, 255))
		pygame.display.update()

	def end_screen(self):
		self.screen.blits(blit_sequence = ((self.death_screen, (0,0)), (self.high_score_render, (220, 568)), (self.distance_render, (212, 281))))
		pygame.display.update()

		while self.end == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				else:
					pass

				if 85 <= pygame.mouse.get_pos()[0] <= 261:
					if 505 <= pygame.mouse.get_pos()[1] <= 552:
						self.screen.blit(self.menu_clicked, (85, 505))
						pygame.display.update()
					else:
						self.screen.blit(self.death_screen, (0,0))
						self.screen.blit(self.high_score_render, (220, 568))
						self.screen.blit(self.distance_render, (212, 281))
						pygame.display.update()
				else:
					pass

				if pygame.mouse.get_pressed()[0] == 1: # menu
					if 85 <= pygame.mouse.get_pos()[0] <= 261:
						if 505 <= pygame.mouse.get_pos()[1] <= 552:
							self.end = False
							self.menu = True
						else:
							pass
					else:
						pass
				else:
					pass

	def is_collision(self):
		self.car_hitbox = (self.x, self.y, 51, 111)
		self.obstacle_hitbox = ((self.obstacle_side/2), self.obstacle_startx, self.obstacle_starty)
		if self.car_hitbox[1] < (self.obstacle_hitbox[2]-self.obstacle_hitbox[0]+60) < (self.car_hitbox[1]+self.car_hitbox[3]):
			if self.car_hitbox[0] < self.obstacle_hitbox[1] < (self.car_hitbox[0]+self.car_hitbox[2]) or self.car_hitbox[0] < (self.obstacle_hitbox[1]+self.obstacle_hitbox[0]) < (self.car_hitbox[0]+self.car_hitbox[2]):
				self.crash()
			else:
				pass
		else:
			pass

	def set_speed(self):
		if self.distance >= 10 and self.distance % 5 == 0:
			self.speed += (self.distance // 10)
		else:
			pass

	def gameplay(self):
		self.obstacle_side, self.obstacle_angle = random.randrange(30, 100), random.randrange(0, 360)
		self.obstacle_startx, self.obstacle_starty = random.randrange(25, (self.display_width-25-self.obstacle_side)), -10
		self.obstacle_hitbox = ((self.obstacle_side/2), self.obstacle_startx, self.obstacle_starty)

		self.speed = .3
		self.distance = 0
		self.initial_load()

		while self.game == True:
			self.distance += 0.0001
			self.score_render = self.font.render(str(int(self.distance)), True, (255, 255, 255))
			self.events()
			self.car_onscreen()
			self.scrolling_road()
			self.obstacles()
			self.move_car(self.x, self.y)
			self.is_collision()
			self.screen.blit(self.score_render, (155, 10))
			pygame.display.update()
			self.obstacle_onscreen()
			self.set_speed()

	def main_menu(self):
		self.main_menu_setup()
		self.options = False

		is_hover = 0
		is_hover_last = 0

		while self.menu == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if 35 <= pygame.mouse.get_pos()[0] <= 315:
					if 216 <= pygame.mouse.get_pos()[1] <= 306: #start
						self.screen.blit(self.start_clicked, (38, 221))
						pygame.display.update()
					elif 336 <= pygame.mouse.get_pos()[1] <= 426:
						if 35 <= pygame.mouse.get_pos()[0] <= 160: #settings
							self.screen.blit(self.options_clicked, (36, 312))
							pygame.display.update()
						elif 190 <= pygame.mouse.get_pos()[0] <= 315: #exit
							self.screen.blit(self.exit_clicked, (193, 312))
							pygame.display.update()
							is_hover = 1
					else:
						is_hover = 0

				if is_hover_last == 1 and is_hover == 0:
					self.main_menu_setup()

				if pygame.mouse.get_pressed()[0] == 1:
					if 35 <= pygame.mouse.get_pos()[0] <= 315:
						if 216 <= pygame.mouse.get_pos()[1] <= 306: #start
							self.menu = False
							self.game = True
							self.end = False
							time.sleep(0.1)
						elif 336 <= pygame.mouse.get_pos()[1] <= 426:
							if 35 <= pygame.mouse.get_pos()[0] <= 160: #settings
								self.options_menu()
							elif 190 <= pygame.mouse.get_pos()[0] <= 315: #exit
								sys.exit()

			is_hover_last = is_hover

	def options_menu(self):
		self.options = True
		self.menu = False
		self.screen.blit(self.options_screen, (0,0))

		if self.world == 0:
			self.screen.blit(self.selected_background, (13, 143))
		elif self.world == 1:
			self.screen.blit(self.selected_background, (126, 143))
		elif self.world == 2:
			self.screen.blit(self.selected_background, (238, 143))
		else:
			pass

		if self.car_choice == 0:
			self.screen.blit(self.selected_car, (10, 275))
		elif self.car_choice == 1:
			self.screen.blit(self.selected_car, (63, 275))
		elif self.car_choice == 2:
			self.screen.blit(self.selected_car, (118, 275))
		elif self.car_choice == 3:
			self.screen.blit(self.selected_car, (174, 275))
		elif self.car_choice == 4:
			self.screen.blit(self.selected_car, (230, 275))
		elif self.car_choice == 5:
			self.screen.blit(self.selected_car, (284, 275))
		else:
			pass

		pygame.display.update()
		while self.options == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				else:
					pass

				if 85 <= pygame.mouse.get_pos()[1] <= 130:
					if 207 <= pygame.mouse.get_pos()[0] <= 258: #yes
						self.screen.blit(self.music_on, (207, 85))
						pygame.display.update()
					elif 269 <= pygame.mouse.get_pos()[0] <= 321: #no
						self.screen.blit(self.music_off, (269, 85))
						pygame.display.update()
					else:
						pass

				elif 542 <= pygame.mouse.get_pos()[1] <= 590:
					if 82 <= pygame.mouse.get_pos()[0] <= 259: #exit
						self.screen.blit(self.options_exit, (83, 540))
						pygame.display.update()
					else:
						pass

				elif 392 <= pygame.mouse.get_pos()[1] <= 414:
					if 11 <= pygame.mouse.get_pos()[0] <= 229:
						self.screen.blit(self.more_car_hover, (11, 392))
						pygame.display.update()
					else:
						pass
				elif 249 <= pygame.mouse.get_pos()[1] <= 273:
					if 11 <= pygame.mouse.get_pos()[0] <= 280:
						self.screen.blit(self.more_background_hover, (11, 249))
						pygame.display.update()
					else:
						pass

				elif 143 <= pygame.mouse.get_pos()[1] <= 243:
					if 13 <= pygame.mouse.get_pos()[0] <= 113: #default
						self.screen.blit(self.background_hover, (13, 143))
						pygame.display.update()
					elif 126 <= pygame.mouse.get_pos()[0] <= 226: #ice
						self.screen.blit(self.background_hover, (126, 143))
						pygame.display.update()
					elif 238 <= pygame.mouse.get_pos()[0] <= 338: #jungle
						self.screen.blit(self.background_hover, (238, 143))
						pygame.display.update()
					else:
						pass

				elif 275 <= pygame.mouse.get_pos()[1] <= 392:
					if 10 <= pygame.mouse.get_pos()[0] <= 62: #firebird
						self.screen.blit(self.hover_car, (10, 275))
						pygame.display.update()
					elif 63 <= pygame.mouse.get_pos()[0] <= 115: #car4
						self.screen.blit(self.hover_car, (63, 275))
						pygame.display.update()
					elif 118 <= pygame.mouse.get_pos()[0] <= 171: #car7
						self.screen.blit(self.hover_car, (118, 275))
						pygame.display.update()
					elif 174 <= pygame.mouse.get_pos()[0] <= 229: #car5
						self.screen.blit(self.hover_car, (174, 275))
						pygame.display.update()
					elif 230 <= pygame.mouse.get_pos()[0] <= 281: #car2
						self.screen.blit(self.hover_car, (230, 275))
						pygame.display.update()
					elif 284 <= pygame.mouse.get_pos()[0] <= 339: #car1
						self.screen.blit(self.hover_car, (284, 275))
						pygame.display.update()
					else:
						pass

				else:
					self.screen.blit(self.options_screen, (0,0))
					if self.world == 0:
						self.screen.blit(self.selected_background, (13, 143))
					elif self.world == 1:
						self.screen.blit(self.selected_background, (126, 143))
					elif self.world == 2:
						self.screen.blit(self.selected_background, (238, 143))
					else:
						pass

					if self.car_choice == 0:
						self.screen.blit(self.selected_car, (10, 275))
					elif self.car_choice == 1:
						self.screen.blit(self.selected_car, (63, 275))
					elif self.car_choice == 2:
						self.screen.blit(self.selected_car, (118, 275))
					elif self.car_choice == 3:
						self.screen.blit(self.selected_car, (174, 275))
					elif self.car_choice == 4:
						self.screen.blit(self.selected_car, (230, 275))
					elif self.car_choice == 5:
						self.screen.blit(self.selected_car, (284, 275))
					else:
						pass

					pygame.display.update()

				if pygame.mouse.get_pressed()[0] == 1:
					if 85 <= pygame.mouse.get_pos()[1] <= 130:
						if 207 <= pygame.mouse.get_pos()[0] <= 258: #yes
							if self.music == 0:
								pygame.mixer.music.unpause()
							elif self.music == 1:
								pygame.mixer.music.play(-1)
							else:
								pass

							self.music = 0
							with open('data/music.dat', 'wb') as file:
								pickle.dump(self.music, file)
						elif 269 <= pygame.mouse.get_pos()[0] <= 321: #no
							pygame.mixer.music.pause()
							self.music = 1
							with open('data/music.dat', 'wb') as file:
								pickle.dump(self.music, file)
						else:
							pass

					elif 542 <= pygame.mouse.get_pos()[1] <= 590:
						if 82 <= pygame.mouse.get_pos()[0] <= 259: #exit
							self.options = False
							self.menu = True
						else:
							pass

					elif 392 <= pygame.mouse.get_pos()[1] <= 414:
						if 11 <= pygame.mouse.get_pos()[0] <= 229:
							print("More cars will come later!")
						else:
							pass
					elif 249 <= pygame.mouse.get_pos()[1] <= 273:
						if 11 <= pygame.mouse.get_pos()[0] <= 280:
							print("More backgrounds will come later!")
						else:
							pass

					elif 142 <= pygame.mouse.get_pos()[1] <= 242:
						if 11 <= pygame.mouse.get_pos()[0] <= 111: #default
							self.world = 0
							self.terrain = self.grass_terrain
							self.road = self.drive
							self.obstacle = self.obstacle
							with open('data/world.dat', 'wb') as file:
								pickle.dump(self.world, file)
						elif 125 <= pygame.mouse.get_pos()[0] <= 225: #snow
							self.world = 1
							self.terrain = self.snow_terrain
							self.road = self.ice_road
							self.obstacle = self.snow_pile
							with open('data/world.dat', 'wb') as file:
								pickle.dump(self.world, file)
						elif 238 <= pygame.mouse.get_pos()[0] <= 338: #jungle
							self.world = 2
							self.terrain = self.jungle_terrain
							self.road = self.dirt_road
							self.obstacle = self.rocks
							with open('data/world.dat', 'wb') as file:
								pickle.dump(self.world, file)

					elif 275 <= pygame.mouse.get_pos()[1] <= 392:
						if 10 <= pygame.mouse.get_pos()[0] <= 62: #firebird
							self.car = self.firebird
							self.car_choice = 0
							with open('data/car.dat', 'wb') as file:
								pickle.dump(self.car_choice, file)
						elif 63 <= pygame.mouse.get_pos()[0] <= 115: #car4
							self.car = self.car4
							self.car_choice = 1
							with open('data/car.dat', 'wb') as file:
								pickle.dump(self.car_choice, file)
						elif 118 <= pygame.mouse.get_pos()[0] <= 171: #car7
							self.car = self.car7
							self.car_choice = 2
							with open('data/car.dat', 'wb') as file:
								pickle.dump(self.car_choice, file)
						elif 174 <= pygame.mouse.get_pos()[0] <= 229: #car5
							self.car = self.car5
							self.car_choice = 3
							with open('data/car.dat', 'wb') as file:
								pickle.dump(self.car_choice, file)
						elif 230 <= pygame.mouse.get_pos()[0] <= 281: #car2
							self.car = self.car2
							self.car_choice = 4
							with open('data/car.dat', 'wb') as file:
								pickle.dump(self.car_choice, file)
						elif 284 <= pygame.mouse.get_pos()[0] <= 339: #car1
							self.car = self.car1
							self.car_choice = 5
							with open('data/car.dat', 'wb') as file:
								pickle.dump(self.car_choice, file)
						else:
							pass

		if self.menu == True:
			self.main_menu()
		else:
			pass

	def mainloop(self):
		if self.music == 0:
			pygame.mixer.music.play(-1)
		else:
			pass

		while self.running == True:
			self.main_menu()
			self.initial_load()
			self.gameplay()
			self.end_screen()

		pygame.mixer.music.stop()
		pygame.mixer.music.unload()
		pygame.quit()
		sys.exit()

if __name__ == "__main__":
	game = racing_fire()
	game.mainloop()
