import pygame as pg 
import constants as c 

#initialise game 
pg.init()

# create clock 
clock = pg.time.Clock()


#game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Emerald Village Defence")
#game loop 
run = True 
while run:

    clock.tick(c.FPS)

    #event handler
    for event in pg.event.get():
      #quit program
      if event.type == pg.QUIT:
         run = False

pg.quit()
