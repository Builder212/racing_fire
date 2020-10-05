import pygame, time, random

class main_game:
	def __init__(self, x, y, terrain_image, road_image, car_image, exploded_car, pothole_image):
		self.screen = pygame.display.set_mode((x, y))
		self.menu = True
		self.running = False
		self.end = False

		self.display_width = x
		self.display_height = y
		self.x = self.display_width*0.45
		self.y = self.display_height*0.8+50
		self.x_change = 0
		self.speed = 1
		self.distance = 0
		self.y_val = 0

		self.death_screen = pygame.image.load("textures/death_screen.png")
		self.menu_background = pygame.image.load("textures/menu_background.png")
		self.terrain = pygame.image.load(terrain_image).convert_alpha()
		self.road = pygame.image.load(road_image).convert_alpha()

		self.car = pygame.image.load(car_image).convert_alpha()
		self.car_hitbox = (self.x, self.y, 51, 111)

		self.pothole = pygame.image.load(pothole_image).convert_alpha()
		self.pothole_side = random.randrange(30, 100)
		self.pothole_angle = random.randrange(0, 360)
		self.pothole_startx = random.randrange(25, (self.display_width-25-self.pothole_side))
		self.pothole_starty = -300
		self.pothole_hitbox = ((self.pothole_side/2), self.pothole_startx, self.pothole_starty)

	def main_menu_setup(self):
		self.screen.blit(self.menu_background, (0,0))
		pygame.display.update()
	def initial_load(self):
		self.screen.blit(self.terrain, (0,0))
		self.screen.blit(self.road, (25,0))

	def move_car(self, x, y):
		self.screen.blit(self.car, (x, y))

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
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
		self.running = False
		self.screen.blit(self.death_screen, (0,0))
		pygame.display.update()
		time.sleep(5)
		exit()

	def is_collision(self):
		self.car_hitbox = (self.x, self.y, 51, 111)
		self.pothole_hitbox = ((self.pothole_side/2), self.pothole_startx, self.pothole_starty)
		if self.car_hitbox[1] < (self.pothole_hitbox[2]-self.pothole_hitbox[0]+60) < (self.car_hitbox[1]+self.car_hitbox[3]):
			if self.car_hitbox[0] < self.pothole_hitbox[1] < (self.car_hitbox[0]+self.car_hitbox[2]) or self.car_hitbox[0] < (self.pothole_hitbox[1]+self.pothole_hitbox[0]) < (self.car_hitbox[0]+self.car_hitbox[2]):
				self.crash()
		else:
			pass

	def set_speed(self):
		if self.distance < 20:
			pass
		elif self.distance >= 20:
			self.speed = self.distance // 10
			print(self.speed)

	def mainloop(self):
		self.main_menu_setup()
		while self.menu:
			for event in pygame.event.get():
				if pygame.mouse.get_pressed()[0] == 1:
					if 26 <= pygame.mouse.get_pos()[0] <= 300:
						if 225 <= pygame.mouse.get_pos()[1] <= 310:
							self.menu = False
							self.running = True
							time.sleep(0.2)
			print(pygame.mouse.get_pos())

		self.initial_load()
		while self.running:
			self.distance += 0.0005
			self.events()
			self.car_onscreen()
			self.scrolling_road()
			self.potholes()
			self.move_car(self.x, self.y)
			self.is_collision()
			pygame.display.update()
			self.pothole_onscreen()
			self.set_speed()

if __name__ == "__main__":
	pygame.init()
	game = main_game(350, 814, "textures/grass_background.png", "textures/road_background.png", "textures/car.png", "textures/exploded_car.png", "textures/pothole.png")
	game.mainloop()
	pygame.quit()
