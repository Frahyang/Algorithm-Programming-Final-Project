import pygame as P
import math
from settings import Settings as S

class Turret(P.sprite.Sprite):
    def __init__(self, turretTypeSpriteSheet, tileX, tileY, shotFx, turretType = ""):
        P.sprite.Sprite.__init__(self)
        self.upgradeLevel = 1
        self.turretType = turretType
        loadTurretData(self)
        self.lastShot = P.time.get_ticks()
        self.selected = False
        self.target = None

        #Position variables
        self.tileX = tileX
        self.tileY = tileY

        #Calculate center coordinates
        self.xCoordinatePosition = (self.tileX + 0.5) * S.TILE_SIZE
        self.yCoordinatePosition = (self.tileY + 0.5) * S.TILE_SIZE

        #Shot sound effect
        self.shotFx = shotFx

        #Animation variables
        self.turretTypeSpriteSheet = turretTypeSpriteSheet
        self.animationList = self.loadImages()
        self.frameIndex = 0
        self.updateTime = P.time.get_ticks()

        #Set default image direction (Upwards)
        self.angle = 90
    
        #Update image 
        self.originalImage = self.animationList[self.frameIndex]
        self.image = P.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.xCoordinatePosition, self.yCoordinatePosition)

        #Create transparent circle showing range
        self.rangeImage = P.Surface((self.range * 2, self.range * 2))
        self.rangeImage.fill((0, 0, 0))
        self.rangeImage.set_colorkey((0, 0, 0))
        P.draw.circle(self.rangeImage, "grey100", (self.range, self.range), self.range)
        self.rangeImage.set_alpha(100)
        self.range_rect = self.rangeImage.get_rect()
        self.range_rect.center = self.rect.center

        #Create red transparent circle to distinguish selected turret
        self.distinguishTurret = 30
        self.distinguishTurretImage = P.Surface((self.distinguishTurret * 2, self.distinguishTurret * 2))
        self.distinguishTurretImage.fill((0, 0, 0))
        self.distinguishTurretImage.set_colorkey((0, 0, 0))
        P.draw.circle(self.distinguishTurretImage, "red", (self.distinguishTurret, self.distinguishTurret), self.distinguishTurret)
        self.distinguishTurretImage.set_alpha(100)
        self.distinguishTurret_rect = self.distinguishTurretImage.get_rect()
        self.distinguishTurret_rect.center = self.rect.center

    def loadImages(self):

        #Extract images from spritesheet
        size = self.turretTypeSpriteSheet.get_height()
        animationList = []
        for step in range(S.ANIMATION_STEPS):
            frame = self.turretTypeSpriteSheet.subsurface(step * size, 0, size, size)
            animationList.append(frame)
        return animationList

    def update(self, entityGroup, map):
        #If target in range. play firing animation
        if self.target:
            self.playAnimation()
        else:
            #Search for new target once turret has cooled down
            if (P.time.get_ticks() - self.lastShot) > (self.attackSpeed / map.gameSpeed):
                self.pickTarget(entityGroup, map)

    def pickTarget(self, entityGroup, map):

        #Used for pythagoral calculations
        xAxisDistance = 0
        yAxisDistance = 0

        #Check distance to each enemy if it is in range
        for entity in entityGroup:

            #Check if entity health is more than 0
            if entity.entityHealth > 0:

                #Calculate closest distance between an entity and a turret
                xAxisDistance = entity.pos[0] - self.xCoordinatePosition
                yAxisDistance = entity.pos[1] - self.yCoordinatePosition
                euclideanDistance = math.sqrt(xAxisDistance ** 2 + yAxisDistance ** 2)

                #Check if entity becomes in range with turret
                if euclideanDistance < self.range:
                    self.target = entity
                    self.angle = math.degrees(math.atan2(-yAxisDistance, xAxisDistance))
                    self.target.entityHealth -= self.damage
                    map.money += self.damage
                    self.shotFx.play()
                    break

    def playAnimation(self):

        #Update image
        self.originalImage = self.animationList[self.frameIndex]

        #Check if enough time has passed since the last update
        if (P.time.get_ticks() - self.updateTime) > S.ANIMATION_DELAY:
            self.updateTime = P.time.get_ticks()
            self.frameIndex += 1

            #Check if the animation has finished and reset to idle
            if self.frameIndex >= len(self.animationList):
                self.frameIndex = 0

                #Record completed time and clear target so attackSpeed can begin
                self.lastShot = P.time.get_ticks()
                self.target = None

    def upgradeTurret(self):

        #Upgrade turret based on type
        if self.turretType == "Basic":
            turretData = S.BASIC_TURRET_DATA
        elif self.turretType == "Sniper":
            turretData = S.SNIPER_TURRET_DATA
        elif self.turretType == "MachineGun":
            turretData = S.MACHINEGUN_TURRET_DATA
        self.upgradeLevel += 1
        self.range = turretData[self.upgradeLevel - 1].get("range")
        self.attackSpeed = turretData[self.upgradeLevel - 1].get("attackSpeed")
        self.damage = turretData[self.upgradeLevel - 1].get("damage")

        #Upgrade range circle
        self.rangeImage = P.Surface((self.range * 2, self.range * 2))
        self.rangeImage.fill((0, 0, 0))
        self.rangeImage.set_colorkey((0, 0, 0))
        P.draw.circle(self.rangeImage, "grey100", (self.range, self.range), self.range)
        self.rangeImage.set_alpha(100)
        self.range_rect = self.rangeImage.get_rect()
        self.range_rect.center = self.rect.center

        #Circle to distinguish selected turret
        self.distinguishTurretImage = P.Surface((self.distinguishTurret * 2, self.distinguishTurret * 2))
        self.distinguishTurretImage.fill((0, 0, 0))
        self.distinguishTurretImage.set_colorkey((0, 0, 0))
        P.draw.circle(self.distinguishTurretImage, "red", (self.distinguishTurret, self.distinguishTurret), self.distinguishTurret)
        self.distinguishTurretImage.set_alpha(100)
        self.distinguishTurret_rect = self.distinguishTurretImage.get_rect()
        self.distinguishTurret_rect.center = self.rect.center

    def draw(self, surface):
        self.image = P.transform.rotate(self.originalImage, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.xCoordinatePosition, self.yCoordinatePosition)
        surface.blit(self.image, self.rect)

        #When a turret is selected show range and red circle
        if self.selected:
            surface.blit(self.rangeImage, self.range_rect)
            surface.blit(self.distinguishTurretImage, self.distinguishTurret_rect)

def loadTurretData(self):

    #Load turret attributes based on type
    if self.turretType == "Basic":
        turretData = S.BASIC_TURRET_DATA
        self.upgradePrice = S.TURRET_UPGRADE_PRICE[0]
        self.sellPrice = S.TURRET_SELL_PRICE[0]
    elif self.turretType == "Sniper":
        turretData = S.SNIPER_TURRET_DATA
        self.upgradePrice = S.TURRET_UPGRADE_PRICE[1]
        self.sellPrice = S.TURRET_SELL_PRICE[1]
    elif self.turretType == "MachineGun":
        turretData = S.MACHINEGUN_TURRET_DATA
        self.upgradePrice = S.TURRET_UPGRADE_PRICE[2]
        self.sellPrice = S.TURRET_SELL_PRICE[2]

    #Load turret upgrades based on type
    self.range = turretData[self.upgradeLevel - 1].get("range")
    self.attackSpeed = turretData[self.upgradeLevel - 1].get("attackSpeed")
    self.damage = turretData[self.upgradeLevel - 1].get("damage")