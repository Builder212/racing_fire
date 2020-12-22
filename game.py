import pygame, time, random, pickle

class main_game:
	def __init__(self, x=350, y=600):
		pygame.init()
		pygame.display.set_caption('Racing Fire')
		self.screen = pygame.display.set_mode((x, y))

		self.running = True
		self.menu = True
		self.game = False
		self.end = False
		self.options = False

		self.soundtrack = pygame.mixer.music.load("soundtrack.mp3")
		try:
			with open('data/music.dat', 'rb') as file:
				self.music = pickle.load(file)
		except:
			self.music = 0
			with open('data/music.dat', 'wb') as file:
				pickle.dump(self.music, file)

		self.display_width = x
		self.display_height = y
		self.x = self.display_width*0.45
		self.y = self.display_height*0.8
		self.x_change = 0
		self.speed = 1
		self.distance = 0
		self.y_val = 0

		self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

		#grass terrain
		self.grass_terrain = pygame.image.load("textures/scenery/road/grass_background.png").convert_alpha()
		self.road = pygame.image.load("textures/scenery/road/road_background.png").convert_alpha()
		self.obstacle = pygame.image.load("textures/scenery/road/pothole.png").convert_alpha()

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
			self.road = self.road
			self.obstacle = self.obstacle
		elif self.world == 1:
			self.terrain = self.snow_terrain
			self.road = self.ice_road
			self.obstacle = self.snow_pile
		elif self.world == 2:
			self.terrain = self.jungle_terrain
			self.road = self.dirt_road
			self.obstacle = self.rocks

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
		self.options_screen = pygame.image.load("textures/settings_menu/settings_background.png").convert_alpha()

		self.car = pygame.image.load("textures/cars/firebird.png").convert_alpha()
		self.car_hitbox = (self.x, self.y, 51, 111)

		self.obstacle_side = random.randrange(30, 100)
		self.obstacle_angle = random.randrange(0, 360)
		self.obstacle_startx = random.randrange(25, (self.display_width-25-self.obstacle_side))
		self.obstacle_starty = -300
		self.obstacle_hitbox = ((self.obstacle_side/2), self.obstacle_startx, self.obstacle_starty)

	def main_menu_setup(self):
		self.screen.blit(self.menu_background, (0,0))
		self.screen.blit(self.high_score_render, (220, 570))
		pygame.display.update()
	def initial_load(self):
		self.screen.blit(self.terrain, (0,0))
		self.screen.blit(self.road, (25,0))

	def move_car(self, x, y):
		self.screen.blit(self.car, (int(x), int(y)))

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.x_change = -.5
				elif event.key == pygame.K_RIGHT:
					self.x_change = .5
				else:
					pass
			else:
				pass
			if event.type == pygame.KEYUP:
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
		self.screen.blit(self.terrain, (0, (int(y-self.terrain.get_rect().height))))
		self.screen.blit(self.road, (25, (int(y-self.road.get_rect().height))))
		if y < 814:
			self.screen.blit(self.terrain, (0, int(y)))
			self.screen.blit(self.road, (25, int(y)))
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
			self.obstacle_side = random.randrange(30, 100)
			self.obstacle_angle = random.randrange(0, 360)
			self.obstacle_startx = random.randrange(25, (self.display_width-25-self.obstacle_side))
		else:
			pass

	def crash(self):
		self.game = False
		self.end = True
		self.screen.blit(self.death_screen, (0,0))
		if int(self.distance) >= self.highscore:
			self.highscore = int(self.distance)
			with open('data/highscore.dat', 'wb') as file:
				pickle.dump(self.highscore, file)
		self.highscore_string = str(self.highscore)
		self.high_score_render = self.font.render(self.highscore_string, True, (255, 255, 255))
		self.distance_render = self.font.render(str(int(self.distance)), True, (255, 255, 255))
		self.screen.blit(self.high_score_render, (60, 760))
		pygame.display.update()

	def end_screen(self):
		while self.end == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if 85 <= pygame.mouse.get_pos()[0] <= 261:
					if 505 <= pygame.mouse.get_pos()[1] <= 552:
						self.screen.blit(self.menu_clicked, (85, 505))
						pygame.display.update()
					else:
						self.screen.blit(self.death_screen, (0,0))
						self.screen.blit(self.high_score_render, (220, 570))
						self.screen.blit(self.distance_render, (212, 278))
						pygame.display.update()
				if pygame.mouse.get_pressed()[0] == 1: # menu
					if 85 <= pygame.mouse.get_pos()[0] <= 261:
						if 505 <= pygame.mouse.get_pos()[1] <= 552:
							self.end = False
							self.menu = True

	def is_collision(self):
		self.car_hitbox = (self.x, self.y, 51, 111)
		self.obstacle_hitbox = ((self.obstacle_side/2), self.obstacle_startx, self.obstacle_starty)
		if self.car_hitbox[1] < (self.obstacle_hitbox[2]-self.obstacle_hitbox[0]+60) < (self.car_hitbox[1]+self.car_hitbox[3]):
			if self.car_hitbox[0] < self.obstacle_hitbox[1] < (self.car_hitbox[0]+self.car_hitbox[2]) or self.car_hitbox[0] < (self.obstacle_hitbox[1]+self.obstacle_hitbox[0]) < (self.car_hitbox[0]+self.car_hitbox[2]):
				self.crash()
		else:
			pass

	def set_speed(self):
		if self.distance >= 10 and self.distance % 10 == 0:
			self.speed = 0.3 + (self.distance // 10)

	def gameplay(self):
		self.obstacle_side = random.randrange(30, 100)
		self.obstacle_angle = random.randrange(0, 360)
		self.obstacle_startx = random.randrange(25, (self.display_width-25-self.obstacle_side))
		self.obstacle_starty = -300
		self.obstacle_hitbox = ((self.obstacle_side/2), self.obstacle_startx, self.obstacle_starty)

		self.speed = .3
		self.distance = 0
		self.initial_load()
		while self.game == True:
			self.distance += 0.0005
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
		self.options == False
		while self.menu == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				else:
					pass

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
						else:
							self.main_menu_setup()
					else:
						self.main_menu_setup()
				else:
					pass

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
								exit()
							else:
								pass
						else:
							pass
					else:
						pass
				else:
					pass

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
		pygame.display.update()
		while self.options == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
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

				else:
					self.screen.blit(self.options_screen, (0,0))
					if self.world == 0:
						self.screen.blit(self.selected_background, (13, 143))
					elif self.world == 1:
						self.screen.blit(self.selected_background, (126, 143))
					elif self.world == 2:
						self.screen.blit(self.selected_background, (238, 143))

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

					elif 142 <= pygame.mouse.get_pos()[1] <= 242:
						if 11 <= pygame.mouse.get_pos()[0] <= 111: #default
							self.world = 0
							self.terrain = self.grass_terrain
							self.road = self.grass_road
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

		if self.menu == True:
			self.main_menu()

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
		exit()

if __name__ == "__main__":
	game = main_game()
	game.mainloop()
