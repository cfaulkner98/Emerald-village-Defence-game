import pygame as pg 
import json
from enemy import Enemy
from world import World
from turrets import Turret 
from button import Button
import constants as c 

#initialise game 
pg.init()

# create clock 
clock = pg.time.Clock()

#game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Emerald Village: Defence")

#game variables
game_over = False
game_outcome = 0 #-1 lose 1 win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None

#load images
#map
map_image = pg.image.load('map/level.png').convert_alpha()
#turret sprite sheets
turret_sheet = pg.image.load('images/turret_1.png').convert_alpha()
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
   turret_sheet = pg.image.load(f'images/turret_{x}.png').convert_alpha()
   turret_spritesheets.append(turret_sheet)
#individual turret image for mouse cursor
cursor_turret = pg.image.load('images/cursor_turret.png').convert_alpha()
#enemies
enemy_images = {
   "weak": pg.image.load('images/witch_1.png').convert_alpha(),
   "medium": pg.image.load('images/witch_3.png').convert_alpha(),
   "strong": pg.image.load('images/witch_2.png').convert_alpha(),
   "elite": pg.image.load('images/witch_4.png').convert_alpha()
}

#button
buy_turret_image = pg.image.load('images/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('images/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('images/turret_upgrade.png').convert_alpha()
begin_image = pg.image.load('images/begin_1.png').convert_alpha()
restart_image = pg.image.load('images/restart_1.png').convert_alpha()

money_image = pg.image.load('images/money_1.png').convert_alpha()
health_image = pg.image.load('images/health_1.png').convert_alpha()


#load json data for level
with open('map/waypoints.json') as file:
   world_data = json.load(file)

#load font for displaying text on screen
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 34)

#function for outputting text onto screen
def draw_text(text, font, text_col, x, y):
   img = font.render(text, True, text_col)
   screen.blit(img, (x, y))

def display_data():
   #draw panel
   pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
   #display data
   screen.blit(health_image, (c.SCREEN_WIDTH + 10, 35))
   draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40) 
   screen.blit(money_image, (c.SCREEN_WIDTH + 10, 65))
   draw_text(str(world.money),text_font, "grey100", c.SCREEN_WIDTH + 50, 70)
   draw_text("Level: " + str(world.level),text_font, "grey100", c.SCREEN_WIDTH + 10, 10)

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
         new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
         turret_group.add(new_turret)
         #deduct cost of turret
         world.money -= c.BUY_COST

def select_turret(mouse_pos):
   mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
   mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
   for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
         return turret

def clear_selection():
   for turret in turret_group:
      turret.selected = False
      
#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

#create groups 
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
button_upgrade = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True )
begin_button = Button(c.SCREEN_WIDTH + 60, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)


#game loop 
run = True 
while run:

    clock.tick(c.FPS)
    
    #updating section
    ################

    if game_over == False:
       #check if player lost
       if world.health <= 0:
          game_over = True
          game_outcome = -1 #lose

       #check if won
       if world.level > c.TOTAL_LEVELS:
          game_over = True
          game_outcome = 1 #winner

       #update groups
       enemy_group.update(world)
       turret_group.update(enemy_group)

       #highlight selected turret
       if selected_turret:
         selected_turret.selected = True

    #drawing section
    #################

    #draw level
    world.draw(screen) 

   #draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
       turret.draw(screen)

    display_data()

    if game_over == False:
       #check if level is being started or not
       if level_started == False:
         if begin_button.draw(screen):
           level_started = True
       else:
       #spawn enemy
          if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
           if world.spawned_enemies < len(world.enemy_list):
            enemy_type = world.enemy_list[world.spawned_enemies]
            enemy = Enemy(enemy_type, world.waypoints, enemy_images)
            enemy_group.add(enemy)
            world.spawned_enemies += 1
            last_enemy_spawn = pg.time.get_ticks()

       #check if wave is finished
       if world.check_level_complete() == True:
         world.money += c.LEVEL_COMPLETE_REWARD
         world.level += 1
         level_started = False
         last_enemy_spawn = pg.time.get_ticks()
         world.reset_level()
         world.process_enemies()
    
       #draw buttons
       #button for placing turret
       #for turret button show cost and draw button
       draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
       screen.blit(money_image, (c.SCREEN_WIDTH +260, 130))
       if turret_button.draw(screen):
         placing_turrets = True
       #if placing turrets then show the cancel button as well
       if placing_turrets == True:
         #show cursor turret
         cursor_rect = cursor_turret.get_rect()
         cursor_pos = pg.mouse.get_pos()
         cursor_rect.center = cursor_pos
         if cursor_pos[0] <= c.SCREEN_WIDTH:
           screen.blit(cursor_turret, cursor_rect)
         if cancel_button.draw(screen):
          placing_turrets = False
      #if turret is selected then show the upgrade button
       if selected_turret:
     #if a turret can be upgraded then show a upgrade button
        if selected_turret.upgrade_level < c.TURRET_LEVELS:
        #show cost and draw button
         draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH +215, 195)
         screen.blit(money_image, (c.SCREEN_WIDTH + 260, 190))
         if button_upgrade.draw(screen):
          if world.money >= c.UPGRADE_COST:
           selected_turret.upgrade()
           world.money -= c.UPGRADE_COST
       
    else:
       pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
       if game_outcome == -1:
          draw_text("Game Over", large_font, "grey0", 310, 230)
       elif game_outcome == 1:
          draw_text("WINNER", large_font, "grey0", 315, 230)
          
       #restart level
       if restart_button.draw(screen):
          game_over = False
          level_started = False
          placing_turrets = False
          selected_turret = None
          last_enemy_spawn = pg.time.get_ticks()
          world = World(world_data, map_image)
          world.process_data()
          world.process_enemies()
          #empty groups
          enemy_group.empty()
          turret_group.empty()

        
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
            # clear selected turret
            selected_turret = None 
            clear_selection()
            if placing_turrets == True:
               #check if there is enough money for turret
               if world.money >= c.BUY_COST: 
                 create_turret(mouse_pos)
            else:
               selected_turret = select_turret(mouse_pos)
            
    #update display
    pg.display.flip()

pg.quit()


