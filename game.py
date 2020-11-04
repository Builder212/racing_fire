import pygame, time, random, pickle

class main_game:
	def __init__(self, x=350, y=814):
		pygame.init()
		pygame.display.set_caption('Firebird')
		self.screen = pygame.display.set_mode((x, y))

		self.running = True
		self.menu = True
		self.game = False
		self.end = False
		self.options = False

		self.soundtrack = pygame.mixer.music.load("soundtrack.mp3")

		self.display_width = x
		self.display_height = y
		self.x = self.display_width*0.45
		self.y = self.display_height*0.8+50
		self.x_change = 0
		self.speed = 1
		self.distance = 0
		self.y_val = 0

		self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

		try:
			with open('data/world.dat', 'rb') as file:
				self.world = pickle.load(file)
		except:
			self.world = 0

		try:
			with open('data/highscore.dat', 'rb') as file:
				self.highscore = pickle.load(file)
		except:
			self.highscore = 0

		self.highscore_string = str(self.highscore)
		self.high_score_render = self.font.render(self.highscore_string, True, (255, 255, 255))

		self.start_clicked = pygame.image.load("textures/main_menu/menu_start_clicked.png").convert_alpha()
		self.exit_clicked = pygame.image.load("textures/main_menu/menu_exit_clicked.png").convert_alpha()
		self.options_clicked = pygame.image.load("textures/main_menu/menu_options_clicked.png").convert_alpha()
		self.menu_background = pygame.image.load("textures/main_menu/menu_background.png").convert_alpha()

		self.menu_clicked = pygame.image.load("textures/exit_menu/menu_button_hover.png").convert_alpha()
		self.death_screen = pygame.image.load("textures/exit_menu/exit_menu.png").convert_alpha()

		self.music_off = pygame.image.load("textures/options_menu/music_off_hover.png").convert_alpha()
		self.music_on = pygame.image.load("textures/options_menu/music_on_hover.png").convert_alpha()
		self.off_selected = pygame.image.load("textures/options_menu/music_off_selected.png").convert_alpha()
		self.on_selected = pygame.image.load("textures/options_menu/music_on_selected.png").convert_alpha()
		self.options_exit = pygame.image.load("textures/options_menu/options_back_hover.png").convert_alpha()
		self.background_hover = pygame.image.load("textures/options_menu/hover_background.png").convert_alpha()
		self.selected_background = pygame.image.load("textures/options_menu/selected_background.png").convert_alpha()
		self.options_screen = pygame.image.load("textures/options_menu/options_background.png").convert_alpha()

		if self.world == 0:
			self.terrain = pygame.image.load("textures/scenery/road/grass_background.png").convert_alpha()
			self.road = pygame.image.load("textures/scenery/road/road_background.png").convert_alpha()
			self.pothole = pygame.image.load("textures/scenery/road/pothole.png").convert_alpha()
		elif self.world == 1:
			self.terrain = pygame.image.load("textures/scenery/ice/snow_background.png").convert_alpha()
			self.road = pygame.image.load("textures/scenery/ice/ice_road_background.png").convert_alpha()
			self.pothole = pygame.image.load("textures/scenery/ice/snow_pile.png").convert_alpha()
		elif self.world == 2:
			self.terrain = pygame.image.load("textures/scenery/jungle/heavy_grass_background.png").convert_alpha()
			self.road = pygame.image.load("textures/scenery/jungle/dirt_road_background.png").convert_alpha()
			self.pothole = pygame.image.load("textures/scenery/jungle/rocks.png").convert_alpha()

		self.car = pygame.image.load("textures/cars/firebird.png").convert_alpha()
		self.car_hitbox = (self.x, self.y, 51, 111)

		self.pothole_side = random.randrange(30, 100)
		self.pothole_angle = random.randrange(0, 360)
		self.pothole_startx = random.randrange(25, (self.display_width-25-self.pothole_side))
		self.pothole_starty = -300
		self.pothole_hitbox = ((self.pothole_side/2), self.pothole_startx, self.pothole_starty)

	def main_menu_setup(self):
		self.screen.blit(self.menu_background, (0,0))
		self.screen.blit(self.high_score_render, (256, 766))
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
					self.x_change = -1
				elif event.key == pygame.K_RIGHT:
					self.x_change = 1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					self.x_change = 0

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

	def potholes(self):
		self.resized_pothole = pygame.transform.scale(self.pothole, (self.pothole_side, self.pothole_side))
		self.rotated_pothole = pygame.transform.rotate(self.resized_pothole, self.pothole_angle)
		self.screen.blit(self.resized_pothole, (int(self.pothole_startx), int(self.pothole_starty)))
		self.pothole_starty += self.speed

	def pothole_onscreen(self):
		if self.pothole_starty > self.display_height:
			self.pothole_starty = 0 - self.pothole_side
			self.pothole_side = random.randrange(30, 100)
			self.pothole_angle = random.randrange(0, 360)
			self.pothole_startx = random.randrange(25, (self.display_width-25-self.pothole_side))
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
		self.screen.blit(self.high_score_render, (60, 760))
		pygame.display.update()

	def end_screen(self):
		while self.end == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if 26 <= pygame.mouse.get_pos()[0] <= 299:
					if 320 <= pygame.mouse.get_pos()[1] <= 430:
						self.screen.blit(self.menu_clicked, (26, 320))
						pygame.display.update()
					else:
						self.screen.blit(self.death_screen, (0,0))
						self.screen.blit(self.high_score_render, (60, 760))
						pygame.display.update()
				if pygame.mouse.get_pressed()[0] == 1: # menu
					if 26 <= pygame.mouse.get_pos()[0] <= 299:
						if 320 <= pygame.mouse.get_pos()[1] <= 430:
							self.end = False
							self.menu = True

	def is_collision(self):
		self.car_hitbox = (self.x, self.y, 51, 111)
		self.pothole_hitbox = ((self.pothole_side/2), self.pothole_startx, self.pothole_starty)
		if self.car_hitbox[1] < (self.pothole_hitbox[2]-self.pothole_hitbox[0]+60) < (self.car_hitbox[1]+self.car_hitbox[3]):
			if self.car_hitbox[0] < self.pothole_hitbox[1] < (self.car_hitbox[0]+self.car_hitbox[2]) or self.car_hitbox[0] < (self.pothole_hitbox[1]+self.pothole_hitbox[0]) < (self.car_hitbox[0]+self.car_hitbox[2]):
				self.crash()
		else:
			pass

	def set_speed(self):
		if self.distance >= 10:
			self.speed = 1 + (self.distance // 20)

	def gameplay(self):
		self.pothole_side = random.randrange(30, 100)
		self.pothole_angle = random.randrange(0, 360)
		self.pothole_startx = random.randrange(25, (self.display_width-25-self.pothole_side))
		self.pothole_starty = -300
		self.pothole_hitbox = ((self.pothole_side/2), self.pothole_startx, self.pothole_starty)

		self.speed = 1
		self.distance = 0
		self.initial_load()
		while self.game == True:
			self.distance += 0.0005
			self.score_render = self.font.render(str(int(self.distance)), True, (255, 255, 255))
			self.events()
			self.car_onscreen()
			self.scrolling_road()
			self.potholes()
			self.move_car(self.x, self.y)
			self.is_collision()
			self.screen.blit(self.score_render, (155, 10))
			pygame.display.update()
			self.pothole_onscreen()
			self.set_speed()

	def main_menu(self):
		self.main_menu_setup()
		self.options == False
		while self.menu == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if 35 <= pygame.mouse.get_pos()[0] <= 315:
					if 216 <= pygame.mouse.get_pos()[1] <= 306: #start
						self.screen.blit(self.start_clicked, (35, 220))
						pygame.display.update()
					elif 336 <= pygame.mouse.get_pos()[1] <= 426: #options
						self.screen.blit(self.options_clicked, (35, 336))
						pygame.display.update()
					elif 450 <= pygame.mouse.get_pos()[1] <= 540: #exit
						self.screen.blit(self.exit_clicked, (35, 450))
						pygame.display.update()
					else:
						self.screen.blit(self.menu_background, (0,0))
						self.screen.blit(self.high_score_render, (256, 766))
						pygame.display.update()
				if pygame.mouse.get_pressed()[0] == 1:
					if 35 <= pygame.mouse.get_pos()[0] <= 315:
						if 216 <= pygame.mouse.get_pos()[1] <= 306: #start
							self.menu = False
							self.game = True
							self.end = False
							time.sleep(0.1)
						elif 336 <= pygame.mouse.get_pos()[1] <= 426: #options
							self.options_menu()
						elif 450 <= pygame.mouse.get_pos()[1] <= 540: #exit
							exit()

	def options_menu(self):
		self.options = True
		self.menu = False
		self.screen.blit(self.options_screen, (0,0))
		if self.world == 0:
			self.screen.blit(self.selected_background, (13, 80))
		elif self.world == 1:
			self.screen.blit(self.selected_background, (126, 80))
		elif self.world == 2:
			self.screen.blit(self.selected_background, (206, 80))
		pygame.display.update()
		while self.options == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if 12 <= pygame.mouse.get_pos()[1] <= 67:
					if 206 <= pygame.mouse.get_pos()[0] <= 250: #yes
						self.screen.blit(self.music_on, (206, 12))
						pygame.display.update()
					elif 269 <= pygame.mouse.get_pos()[0] <= 304: #no
						self.screen.blit(self.music_off, (269, 12))
						pygame.display.update()
				elif 760 <= pygame.mouse.get_pos()[1] <= 805:
					if 88 <= pygame.mouse.get_pos()[0] <= 262: #exit
						self.screen.blit(self.options_exit, (88, 760))
						pygame.display.update()
				elif 80 <= pygame.mouse.get_pos()[1] <= 180:
					if 13 <= pygame.mouse.get_pos()[0] <= 113: #default
						self.screen.blit(self.background_hover, (13, 80))
						pygame.display.update()
					elif 125 <= pygame.mouse.get_pos()[0] <= 225: #ice
						self.screen.blit(self.background_hover, (125, 80))
						pygame.display.update()
					elif 237 <= pygame.mouse.get_pos()[0] <= 337: #jungle
						self.screen.blit(self.background_hover, (237, 80))
						pygame.display.update()
				else:
					self.screen.blit(self.options_screen, (0,0))
					if self.world == 0:
						self.screen.blit(self.selected_background, (13, 80))
					elif self.world == 1:
						self.screen.blit(self.selected_background, (125, 80))
					elif self.world == 2:
						self.screen.blit(self.selected_background, (237, 80))
					pygame.display.update()
				if pygame.mouse.get_pressed()[0] == 1:
					if 130 <= pygame.mouse.get_pos()[1] <= 200:
						if 76 <= pygame.mouse.get_pos()[0] <= 148: #yes
							pygame.mixer.music.unpause()
						elif 200 <= pygame.mouse.get_pos()[0] <= 269: #no
							pygame.mixer.music.pause()
					elif 80 <= pygame.mouse.get_pos()[1] <= 180:
						if 13 <= pygame.mouse.get_pos()[0] <= 113: #default
							self.world = 0
							self.terrain = pygame.image.load("textures/scenery/road/grass_background.png").convert_alpha()
							self.road = pygame.image.load("textures/scenery/road/road_background.png").convert_alpha()
							self.pothole = pygame.image.load("textures/scenery/road/pothole.png").convert_alpha()
							with open('data/world.dat', 'wb') as file:
								pickle.dump(self.world, file)
						elif 125 <= pygame.mouse.get_pos()[0] <= 225: #snow
							self.world = 1
							self.terrain = pygame.image.load("textures/scenery/ice/snow_background.png").convert_alpha()
							self.road = pygame.image.load("textures/scenery/ice/ice_road_background.png").convert_alpha()
							self.pothole = pygame.image.load("textures/scenery/ice/snow_pile.png").convert_alpha()
							with open('data/world.dat', 'wb') as file:
								pickle.dump(self.world, file)
						elif 237 <= pygame.mouse.get_pos()[0] <= 337: #jungle
							self.world = 2
							self.terrain = pygame.image.load("textures/scenery/jungle/heavy_grass_background.png").convert_alpha()
							self.road = pygame.image.load("textures/scenery/jungle/dirt_road_background.png").convert_alpha()
							self.pothole = pygame.image.load("textures/scenery/jungle/rocks.png").convert_alpha()
							with open('data/world.dat', 'wb') as file:
								pickle.dump(self.world, file)
					elif 715 <= pygame.mouse.get_pos()[1] <= 778:
						if 75 <= pygame.mouse.get_pos()[0] <= 269: #exit
							self.options = False
							self.menu = True

		if self.menu == True:
			self.main_menu()

	def mainloop(self):
		pygame.mixer.music.play(-1)
		while self.running == True:
			self.main_menu()
			self.initial_load()
			self.gameplay()
			self.end_screen()
		pygame.mixer.music.stop()
		pygame.mixer.music.unload()
		time.sleep(0.1)
		pygame.quit()
		exit()

if __name__ == "__main__":
	game = main_game()
	game.mainloop()
