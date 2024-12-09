import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])  # Starting position at the first waypoint
        self.target_waypoint = 1  # Starting at the second waypoint
        self.speed = 2  # Movement speed
        self.image = image  # The sprite image
        self.rect = self.image.get_rect(center=self.pos)  # The position of the sprite on screen

    def update(self):
        self.move()  # Just update the movement, no rotation

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
        
  
       
