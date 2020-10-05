import pygame, time, random

class main_game:
	def __init__(self, x=350, y=814, terrain_image="textures/grass_background.png", road_image="textures/road_background.png", car_image="textures/car.png", potholes= "textures/pothole.png"):
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
		self.highscore = 0
		self.highscore_string = "Highscore: " + str(self.highscore)
		self.high_score_render = self.font.render(self.highscore_string, True, (255, 255, 255))

		self.options_screen = pygame.image.load("textures/options_screen.png").convert_alpha()
		self.death_screen = pygame.image.load("textures/death_screen.png").convert_alpha()
		self.menu_background = pygame.image.load("textures/menu_background.png").convert_alpha()
		self.terrain = pygame.image.load(terrain_image).convert_alpha()
		self.road = pygame.image.load(road_image).convert_alpha()

		self.car = pygame.image.load(car_image).convert_alpha()
		self.car_hitbox = (self.x, self.y, 51, 111)

		self.pothole = pygame.image.load(potholes).convert_alpha()
		self.pothole_side = random.randrange(30, 100)
		self.pothole_angle = random.randrange(0, 360)
		self.pothole_startx = random.randrange(25, (self.display_width-25-self.pothole_side))
		self.pothole_starty = -300
		self.pothole_hitbox = ((self.pothole_side/2), self.pothole_startx, self.pothole_starty)

	def main_menu_setup(self):
		self.screen.blit(self.menu_background, (0,0))
		self.screen.blit(self.high_score_render, (60, 760))
		pygame.display.update()
	def initial_load(self):
		self.screen.blit(self.terrain, (0,0))
		self.screen.blit(self.road, (25,0))

	def move_car(self, x, y):
		self.screen.blit(self.car, (x, y))

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game = False
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
		self.screen.blit(self.terrain, (0, (y-self.terrain.get_rect().height)))
		self.screen.blit(self.road, (25, (y-self.road.get_rect().height)))
		if y < 814:
			self.screen.blit(self.terrain, (0, y))
			self.screen.blit(self.road, (25, y))
		else:
			pass
		self.y_val += self.speed

	def potholes(self):
		self.resized_pothole = pygame.transform.scale(self.pothole, (self.pothole_side, self.pothole_side))
		self.rotated_pothole = pygame.transform.rotate(self.resized_pothole, self.pothole_angle)
		self.screen.blit(self.resized_pothole, (self.pothole_startx, self.pothole_starty))
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
		self.highscore_string = "Highscore: " + str(self.highscore)
		self.high_score_render = self.font.render(self.highscore_string, True, (255, 255, 255))
		self.screen.blit(self.high_score_render, (60, 760))
		pygame.display.update()

	def end_screen(self):
		while self.end == True:
			for event in pygame.event.get():
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
			self.speed = self.distance // 5

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
				if pygame.mouse.get_pressed()[0] == 1:
					if 26 <= pygame.mouse.get_pos()[0] <= 323:
						if 225 <= pygame.mouse.get_pos()[1] <= 310: #start
							self.menu = False
							self.game = True
							self.end = False
							time.sleep(0.1)
						elif 334 <= pygame.mouse.get_pos()[1] <= 431: #options
							self.options_menu()
						elif 444 <= pygame.mouse.get_pos()[1] <= 542: #exit
							exit()

	def options_menu(self):
		self.options == True
		self.screen.blit(self.options_screen, (0,0))
		pygame.display.update()
		while True:
			for event in pygame.event.get():
				if pygame.mouse.get_pressed()[0] == 1:
					if 130 <= pygame.mouse.get_pos()[1] <= 200:
						if 76 <= pygame.mouse.get_pos()[0] <= 148: #yes
							pygame.mixer.music.unpause()
						elif 200 <= pygame.mouse.get_pos()[0] <= 269: #no
							pygame.mixer.music.pause()
					elif 715 <= pygame.mouse.get_pos()[1] <= 778:
						if 75 <= pygame.mouse.get_pos()[0] <= 269:
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
		exit()

if __name__ == "__main__":
	pygame.init()
	game = main_game()
	game.mainloop()
	pygame.quit()
