import pygame
import math
from pygame.locals import *


res = (640,480)
fps = 60

width = 20
height = 20

grav = .1
snap = 20

screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()


class Tile():
	def __init__(self, x=0, y=0, w=width, h=height):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		
		self.dx = 0
		self.dy = 0
		
		self.gravity = False
		self.ID = 0
		self.noContact = True
		

		self.rect = Rect(self.x, self.y, self.width, self.height)
		self.color = (255,255,255)
		
		self.tag = "tile"
		
	def movex(self, dx):
		self.dx = dx
	
	def movey(self, dy):
		self.dy = dy


class World():
	def __init__(self):
		self.objects = {}
		self.lastID = 0
		
	def newObj(self, obj):
		self.lastID += 1
		self.objects[self.lastID] = obj
		self.objects[self.lastID].ID = self.lastID
		

	def render(self):
		for e in self.objects:
			obj = self.objects[e]
			pygame.draw.rect(screen, (obj.color), obj.rect)
		
		
	def update(self):
		for e in self.objects:
			obj = self.objects[e]
			
			if obj.tag == "player":
				print("before: %.2f" % obj.dy)
			
			for el in self.objects:
				obj2 = self.objects[el]				
				
				if obj2.ID != obj.ID:
					if obj2.rect.colliderect(obj.rect):
						
						#if obj2.dx > 0:
							#obj2.rect.right = obj.rect.left
						
						#if obj2.dx < 0:
							#obj2.rect.left = obj.rect.right
						
						if obj2.dy > 0:
							obj2.noContact = False
							obj2.dy = 0
							obj2.rect.bottom = obj.rect.top
						
						#if obj2.dy < 0:
							#obj2.rect.top = obj.rect.bottom

					

			obj.dy += (grav * obj.gravity * obj.noContact)
			obj.x += obj.dx
			obj.y += obj.dy
			
			if obj.tag == "player":
				print("after: %.2f" % obj.dy)
			
			obj.rect = Rect(obj.x, obj.y, obj.width, obj.height)

def fillBottom():
	for e in range(res[0]/snap):
		world.newObj(Tile(e*snap,460))

def snapp(pos):
        snapped = math.floor((pos/snap) * snap)
        return snapped
        
world = World()
world.newObj(Tile(20,20))
player = world.objects[world.lastID]
player.gravity = True
player.tag = "player"
fillBottom()	


def main():
	screen.fill((0,0,0))
	
	user_in = pygame.event.get()
	mouse_buttons = pygame.mouse.get_pressed()
	mouse_pos = pygame.mouse.get_pos()
    
	for event in user_in:
		
		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				player.movex(-2)
			elif event.key == K_RIGHT:
				player.movex(2)
		
		elif event.type == KEYUP:
			if event.key == K_LEFT:
				player.movex(0)
			elif event.key == K_RIGHT:
				player.movex(0)
				
		#===========================#
#=======# 	Gen square on click		#
		#===========================#
		elif event.type == MOUSEBUTTONDOWN:
			snappedX = snapp(mouse_pos[0])
			snappedY = snapp(mouse_pos[1])
	
			ok = True
			for e in world.objects:
					if world.objects[e].__class__.__name__ == "Tile":
							if world.objects[e].x == snappedX and world.objects[e].y == snappedY:
									ok = False
							else:
									ok = True
									

			if ok == True:
					world.newObj(Tile(snappedX, snappedY))
		#===========================#
#=======# 	/Gen square on click	#
		#===========================#

	world.update()
	world.render()

	pygame.display.flip()
	clock.tick(fps)
	
running = True

while running == True:
	main()
	
