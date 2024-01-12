import pygame as P
from pygame.math import Vector2
import math
from settings import Settings as S

class Entity(P.sprite.Sprite):
    def __init__(self, entityType, waypoints, images):
        P.sprite.Sprite.__init__(self)
        self.waypoints = waypoints

        #Vector2 used to represent position of entities and the movement vectors. Simplifies operations involving positions and directions in a 2D space
        self.pos = Vector2(self.waypoints[0])
        self.targetWaypoint = 1

        #Initialise entity attributes
        self.entityHealth = S.ENTITY_ATTRIBUTE_VALUES.get(entityType)["health"]
        self.entitySpeed = S.ENTITY_ATTRIBUTE_VALUES.get(entityType)["speed"]
        self.entityKilledReward = S.ENTITY_ATTRIBUTE_VALUES.get(entityType)["reward"]

        #Rotation necessities
        self.angle = 0
        self.originalEntityImage = images.get(entityType)
        self.entityImage = P.transform.rotate(self.originalEntityImage, self.angle)
        self.rect = self.entityImage.get_rect()
        self.rect.center = self.pos

        #Create health bar and set position coordinates
        self.healthBar = HealthBar(self.pos.x - 20, self.pos.y - 30, 40, 5, self.entityHealth)

    def entityMovement(self, map):

        #When entity hasn't reach destination
        if self.targetWaypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.targetWaypoint])
            self.movement = self.target - self.pos

        #When entity has reach destination
        else:

            #Entities reached the end of the path
            self.kill()

            ##Total health is reduced by remaining entity health
            map.health -= min(self.entityHealth, map.health)
            map.entitiesMissed += 1
            map.displayEntitiesMissed += 1

        #calculate distance to target waypoint
        entityPathDistance = self.movement.length()

        #Check if remaining distance is greater than the enemy speed
        if entityPathDistance >= (self.entitySpeed * map.gameSpeed):
            self.pos += self.movement.normalize() * (self.entitySpeed * map.gameSpeed)
        else:

            #Check if the remaining distance is not 0
            if entityPathDistance != 0:

            #This prevents the object from overshooting the remaining distance and actually reaches 0
                self.pos += self.movement.normalize() * entityPathDistance

            #Once the distance is 0 for the first waypoint the object goes for the next waypoint
            self.targetWaypoint += 1

    def dynamicEntityFaceDirection(self):

        #Calculate distance to next waypoint
        entityPathDistance = self.target - self.pos

        #Use distance to calculate angle
        self.angle = math.degrees(math.atan2(-entityPathDistance[1], entityPathDistance[0]))

        #Rotate image and update rectangle
        self.entityImage = P.transform.rotate(self.originalEntityImage, self.angle)
        self.rect = self.entityImage.get_rect()
        self.rect.center = self.pos

    def draw(self, surface):

        # Draw the entity image
        surface.blit(self.entityImage, self.rect)

    def drawHealthBar(self, surface):
        self.healthBar.drawHealth(surface, self.entityHealth)

    def checkEntityStatus(self, map):
        if self.entityHealth <= 0:
            map.entitiesKilled += 1
            map.displayEntitiesKilled += 1
            map.money += self.entityKilledReward
            self.kill()

    def entityHealthBars(self):
        self.healthBar.xCoordinatePosition = self.pos.x - 20
        self.healthBar.yCoordinatePosition = self.pos.y - 30

    def update(self, map):
        self.entityMovement(map)
        self.dynamicEntityFaceDirection()
        self.checkEntityStatus(map)
        self.entityHealthBars()

class HealthBar():
    def __init__(self, xCoordinatePosition, yCoordinatePosition, width, height, maxHealth):
        self.xCoordinatePosition = xCoordinatePosition
        self.yCoordinatePosition = yCoordinatePosition
        self.width = width
        self.height = height
        self.maxHealth = maxHealth

    def drawHealth(self, surface, currentHealth):

        #Calculate health ratio of entity's current health to its maximum health
        ratio = currentHealth / self.maxHealth
        P.draw.rect(surface, "red", (self.xCoordinatePosition, self.yCoordinatePosition, self.width, self.height))
        P.draw.rect(surface, "green", (self.xCoordinatePosition, self.yCoordinatePosition, self.width * ratio, self.height))