import pygame as P
from pygame.math import Vector2
import math
from settings import Settings as S

class Entity(P.sprite.Sprite):
    #Inheriting the sprite functions into the class entity to pass on those functions and make them usable
    def __init__(self, entityType, waypoints, images):
        P.sprite.Sprite.__init__(self)
        self.waypoints = waypoints

        #Vector2 used to represent position of entities and the movement vectors. Simplifies operations involving positions and directions in a 2D space
        self.pos = Vector2(self.waypoints[0])
        self.targetWaypoint = 1
        self.entityHealth = S.ENTITY_ATTRIBUTE_VALUES.get(entityType)["health"]
        self.entitySpeed = S.ENTITY_ATTRIBUTE_VALUES.get(entityType)["speed"]
        self.entityKilledReward = S.ENTITY_ATTRIBUTE_VALUES.get(entityType)["reward"]
        self.angle = 0
        self.originalEntityImage = images.get(entityType)
        self.image = P.transform.rotate(self.originalEntityImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        #Create health bar and set position coordinates
        self.healthBar = HealthBar(self.pos.x - 20, self.pos.y - 30, 40, 5, self.entityHealth)

    def update(self, map):
        self.entityMovement(map)
        self.dynamicEntityFaceDirection()
        self.checkEntityStatus(map)
        self.entityHealthBars()

    def entityHealthBars(self):
        self.healthBar.xCoordinatePosition = self.pos.x - 20
        self.healthBar.yCoordinatePosition = self.pos.y - 30

    def entityMovement(self, map):
        #Define a target waypoint
        if self.targetWaypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.targetWaypoint]) #The reason the object keeps oscillating is the distance between the object pos and the waypoint is less than the actual movement speed
            self.movement = self.target - self.pos
        else:
            #Entities reached the end of the path
            self.kill() #Function inherited from the sprite class
            ##Total health is reduced by remaining entity health
            map.health -= min(self.entityHealth, map.health)
            map.entitiesMissed += 1
            map.displayEntitiesMissed += 1

        #calculate distance to target
        entityPathDistance = self.movement.length()

        #Check if remaining distance is greater than the enemy speed
        if entityPathDistance >= (self.entitySpeed * map.gameSpeed):
            self.pos += self.movement.normalize() * (self.entitySpeed * map.gameSpeed)
        else:
            #The if statement below ensures that the vector will always have a length of more than 0
            #It is necessary as for some instances the object moving overshoots the remaining distance and would oscillate
            if entityPathDistance != 0:
            #This prevents the object from overshooting the remaining distance and actually reaches 0
                self.pos += self.movement.normalize() * entityPathDistance
            #Once the distance is 0 for the first waypoint the object goes for the next waypoint
            self.targetWaypoint += 1
        #self.rect.center = self.pos this is now repositioned in dyamicEntityFaceDirection
        #self.rect.x += 1 not needed because this does not have a specific direction, only moves the element across the screen

    def dynamicEntityFaceDirection(self):
        #Calculate distance to next waypoint
        entityPathDistance = self.target - self.pos
        
        #Use distance to calculate angle
        self.angle = math.degrees(math.atan2(-entityPathDistance[1], entityPathDistance[0]))
        #The entityPathDistance[1] is for the distance on the y axis and index 0 for the x axis
        #The y axis distance is negative because in pygame the y axis starts from the top
        #By default math.atan2 gives the angle in radians hence the function math.degrees is needed to change those values to degrees

        #Rotate image and update rectangle
        self.image = P.transform.rotate(self.originalEntityImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def draw(self, surface):
        # Draw the entity image
        surface.blit(self.image, self.rect)

    def drawHealthBar(self, surface):
        self.healthBar.drawHealth(surface, self.entityHealth)

    def checkEntityStatus(self, map):
        if self.entityHealth <= 0:
            map.entitiesKilled += 1
            map.displayEntitiesKilled += 1
            map.money += self.entityKilledReward
            self.kill()

class HealthBar():
    def __init__(self, xCoordinatePosition, yCoordinatePosition, width, height, maxHP):
        self.xCoordinatePosition = xCoordinatePosition
        self.yCoordinatePosition = yCoordinatePosition
        self.width = width
        self.height = height
        self.maxHP = maxHP

    def drawHealth(self, surface, currentHealth):
        #Calculate health ratio
        ratio = currentHealth / self.maxHP
        P.draw.rect(surface, "red", (self.xCoordinatePosition, self.yCoordinatePosition, self.width, self.height))
        P.draw.rect(surface, "green", (self.xCoordinatePosition, self.yCoordinatePosition, self.width * ratio, self.height))