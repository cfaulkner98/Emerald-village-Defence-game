import pygame as pg 
import json
from enemy import Enemy
from world import World
from turrets import Turret 
import constants as c 

#initialise game 
pg.init()

# create clock 
clock = pg.time.Clock()

#game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Emerald Village: Defence")

#load images
#map
map_image = pg.image.load('map/level.png').convert_alpha()
#individual turret image for mmouse cursor
cursor_turret = pg.image.load('images/cursor_turret.png').convert_alpha()
#enemies
enemy_image = pg.image.load('images/enemy_1.png').convert_alpha()

#button
buy_turret_image = pg.image.load('images/buy_turret.png').convert_alpha()


#load json data for level
with open('map/waypoints.json') as file:
   world_data = json.load(file)

def create_turret(mouse_pos):
   mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
   mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
   #calculate the sequential number of tile
   mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
   #check if that tile is grass
   if world.tile_map[mouse_tile_num] == 7:
      #check that their isnt already a turret there
      space_is_free = True
      for turret in turret_group: 
         if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            space_is_free = False
      #if it is a free space then create turret
      if space_is_free == True:
         new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
         turret_group.add(new_turret)
      

#create world
world = World(world_data, map_image)
world.process_data()

#create groups 
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()


enemy = Enemy((world.waypoints), enemy_image)
enemy_group.add(enemy)

#game loop 
run = True 
while run:

    clock.tick(c.FPS)

    screen.fill("grey100")

    #draw level
    world.draw(screen) 

    #update groups
    enemy_group.update()

    #draw groups
    enemy_group.draw(screen)
    turret_group.draw(screen)

    
    #event handler
    for event in pg.event.get():
      #quit program
      if event.type == pg.QUIT:
         run = False
      #mouse click 
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
         mouse_pos = pg.mouse.get_pos()
         #check if mouse if on the game area
         if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
            create_turret(mouse_pos)
            
    #update display
    pg.display.flip()

pg.quit()
