import pygame as pg
from pygame.math import Vector2
import math
from spawn_new_enemy import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
    def __init__(self,enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])  # Starting position at the first waypoint
        self.target_waypoint = 1  # Starting at the second waypoint
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)  # The sprite image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    def update(self):
        self.move()  # Just update the movement, no rotation
        self.check_alive()
    def move(self):
        # Define target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # If the enemy has reached the end of the path, kill it
            self.kill()

        # Calculate the distance to the target
        dist = self.movement.length()
        
        # Check if the remaining distance is greater than the enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed  # Move towards the target waypoint
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist  # Move to the target if it's close
            self.target_waypoint += 1  # Move to the next waypoint

        # Update the rect position for the sprite
        self.rect.center = self.pos

    def check_alive(self):
        if self.health <= 0:
            self.kill()
        
  
       
