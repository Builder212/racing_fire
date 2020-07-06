import pygame, time, random

class main_game:
	def __init__(self, x, y, terrain_image, road_image, car_image, exploded_car, pothole_image):
		self.screen = pygame.display.set_mode((x, y))
		self.running = True
		
		self.display_width = x
		self.display_height = y
		self.x = self.display_width*0.45
		self.y = self.display_height*0.8+50
		self.x_change = 0
		self.speed = 2
		self.y_val = 0
		
		self.terrain = pygame.image.load(terrain_image).convert_alpha()
		self.road = pygame.image.load(road_image).convert_alpha()
		
		self.car = pygame.image.load(car_image).convert_alpha()
		self.car_hitbox = (self.x, self.y, 51, 111)
		self.exploded_car = pygame.image.load(exploded_car).convert_alpha()
		
		self.pothole = pygame.image.load(pothole_image).convert_alpha()
		self.pothole_side = random.randrange(30, 100)
		self.pothole_angle = random.randrange(0, 360)
		self.pothole_startx = random.randrange(25, (self.display_width-25-self.pothole_side))
		self.pothole_starty = -300
		self.pothole_hitbox = ((self.pothole_side/2), self.pothole_startx, self.pothole_starty)
		
		self.explosion_1 = pygame.image.load("textures/explosion_1.png").convert_alpha()
		self.explosion_2 = pygame.image.load("textures/explosion_2.png").convert_alpha()
		self.explosion_3 = pygame.image.load("textures/explosion_3.png").convert_alpha()
		self.explosion_4 = pygame.image.load("textures/explosion_4.png").convert_alpha()
		self.explosion_5 = pygame.image.load("textures/explosion_5.png").convert_alpha()
		self.explosion_6 = pygame.image.load("textures/explosion_6.png").convert_alpha()
		self.explosion_7 = pygame.image.load("textures/explosion_7.png").convert_alpha()
		self.exploded_car = pygame.image.load("textures/exploded_car.png").convert_alpha()
		
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
					self.x_change = -2
				elif event.key == pygame.K_RIGHT:
					self.x_change = 2
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
		self.runnning = False
		self.explosion_1 = pygame.transform.scale(self.explosion_1, (15, 15))
		self.screen.blit(self.explosion_1, (self.x+18, self.y+5))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_1 = pygame.transform.scale(self.explosion_1, (17, 17))
		self.screen.blit(self.explosion_1, (self.x+16, self.y+4))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_1 = pygame.transform.scale(self.explosion_1, (20, 20))
		self.screen.blit(self.explosion_1, (self.x+14, self.y+3))
		pygame.display.update()
		time.sleep(0.01)
		self.screen.blit(self.explosion_2, (self.x+13, self.y+2))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_2 = pygame.transform.scale(self.explosion_2, (27, 27))
		self.screen.blit(self.explosion_2, (self.x+12, self.y))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_2 = pygame.transform.scale(self.explosion_2, (30, 30))
		self.screen.blit(self.explosion_2, (self.x+11, self.y-1))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_2 = pygame.transform.scale(self.explosion_2, (33, 33))
		self.screen.blit(self.explosion_2, (self.x+10, self.y-2))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_2 = pygame.transform.scale(self.explosion_2, (36, 36))
		self.screen.blit(self.explosion_2, (self.x+9, self.y-3))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_3 = pygame.transform.scale(self.explosion_3, (40, 40))
		self.screen.blit(self.explosion_3, (self.x+7, self.y-4))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_3 = pygame.transform.scale(self.explosion_3, (44, 44))
		self.screen.blit(self.explosion_3, (self.x+5, self.y-5))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_3 = pygame.transform.scale(self.explosion_3, (48, 48))
		self.screen.blit(self.explosion_3, (self.x+3, self.y-6))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_3 = pygame.transform.scale(self.explosion_3, (52, 52))
		self.screen.blit(self.explosion_3, (self.x+1, self.y-7))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_3 = pygame.transform.scale(self.explosion_3, (56, 56))
		self.screen.blit(self.explosion_3, (self.x-1, self.y-8))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_4 = pygame.transform.scale(self.explosion_4, (70, 70))
		self.screen.blit(self.explosion_4, (self.x-3, self.y-9))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_4 = pygame.transform.scale(self.explosion_4, (80, 80))
		self.screen.blit(self.explosion_4, (self.x-6, self.y-11))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_4 = pygame.transform.scale(self.explosion_4, (100, 100))
		self.screen.blit(self.explosion_4, (self.x-10, self.y-15))
		pygame.display.update()
		time.sleep(0.01)
		self.explosion_4 = pygame.transform.scale(self.explosion_4, (150, 150))
		self.screen.blit(self.explosion_4, (self.x-20, self.y-17))
		pygame.display.update()
		time.sleep(0.01)
		self.screen.blit(self.terrain, (0,0))
		self.screen.blit(self.road, (25,0))
		self.exploded_car = pygame.transform.scale(self.exploded_car, (60, 120))
		self.screen.blit(self.exploded_car, (self.x, self.y))
		self.explosion_5 = pygame.transform.scale(self.explosion_5, (160, 160))
		self.screen.blit(self.explosion_5, (self.x-35, self.y-20))
		pygame.display.update()
		time.sleep(0.01)
		self.screen.blit(self.terrain, (0,0))
		self.screen.blit(self.road, (25,0))
		self.screen.blit(self.exploded_car, (self.x, self.y))
		pygame.display.update()
		time.sleep(10)
		exit()
	
	def is_collision(self):
		self.car_hitbox = (self.x, self.y, 51, 111)
		self.pothole_hitbox = ((self.pothole_side/2), self.pothole_startx, self.pothole_starty)
		if self.car_hitbox[1] < (self.pothole_hitbox[2]-self.pothole_hitbox[0]+60) < (self.car_hitbox[1]+self.car_hitbox[3]):
			if self.car_hitbox[0] < self.pothole_hitbox[1] < (self.car_hitbox[0]+self.car_hitbox[2]) or self.car_hitbox[0] < (self.pothole_hitbox[1]+self.pothole_hitbox[0]) < (self.car_hitbox[0]+self.car_hitbox[2]):
				self.crash()
		else:
			pass
	
	def mainloop(self):
		self.initial_load()
		while self.running:
			self.events()
			self.car_onscreen()
			self.scrolling_road()
			self.potholes()
			self.move_car(self.x, self.y)
			self.is_collision()
			pygame.display.update()
			self.pothole_onscreen()
			
if __name__ == "__main__":
	pygame.init()
	game = main_game(350, 814, "textures/grass_background.png", "textures/road_background.png", "textures/car.png", "textures/exploded_car.png", "textures/pothole.png")
	game.mainloop()
	pygame.quit()
