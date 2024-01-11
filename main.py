import pygame as P
import json
from entities import Entity as ent
from map import Map
from settings import Settings as S
from turret import Turret as T
from button import Button

#Initialise pygame
P.init()

#Create clock
clock = P.time.Clock()

#Create game window with the set resolution
screen = P.display.set_mode((S.SCREEN_WIDTH + S.TURRET_PANEL, S.SCREEN_HEIGHT))
P.display.set_caption("EnTD")

#Game variables
waveStarted = False
musicLoaded = False
endSoundPlayed = False
fastForwardStatus = False
lastEntitySpawn = P.time.get_ticks()
placingTurrets = False
selectedTurret = None
gameOver = False
gameOutcome = 0 # -1 is loss & 1 is win

"""Load Images For Map, Entities, and Turrets"""

#Map image
spaceMapImage = P.image.load("map/Space_Map.png").convert_alpha()

#Entity images
entityImages = {
    "Basic": P.image.load("entityImages/Entity_Basic.png").convert_alpha(),
    "Fast": P.image.load("entityImages/Entity_Fast.png").convert_alpha(),
    "Tank": P.image.load("entityImages/Entity_Tank.png").convert_alpha(),
    "Mini-Boss": P.image.load("entityImages/Entity_Mini-Boss.png").convert_alpha(),
    "Boss": P.image.load("entityImages/Entity_Boss.png").convert_alpha()
}

#Turret spritesheets
basicTurretSpriteSheet = P.image.load("turretImages/Turret_Basic_Animation.png").convert_alpha()
sniperTurretSpriteSheet = P.image.load("turretImages/Turret_Sniper_Animation.png").convert_alpha()
machineGunTurretSpriteSheet = P.image.load("turretImages/Turret_MachineGun_Animation.png").convert_alpha()
turretSpriteSheets = [basicTurretSpriteSheet, sniperTurretSpriteSheet, machineGunTurretSpriteSheet]

#Turret images for mouse cursor
basicTurretImage = P.image.load("turretImages/Turret_Basic.png").convert_alpha()
sniperTurretImage = P.image.load("turretImages/Turret_Sniper.png").convert_alpha()
machineGunTurretImage = P.image.load("turretImages/Turret_MachineGun.png").convert_alpha()
cursorTurretImages = [basicTurretImage, sniperTurretImage, machineGunTurretImage]


"""Load Map json Data For Pre-determined Entity Path"""

with open("map/Space_Map.tmj") as file:
    mapData = json.load(file)

"""Load Images and Fonts For GUI Essentials"""

#Turret Buttons
buyBasicTurretImage = P.image.load("GUIImages/buyBasicTurretButton.png").convert_alpha()
buySniperTurretImage = P.image.load("GUIImages/buySniperTurretButton.png").convert_alpha()
buyMachineGunImage = P.image.load("GUIImages/buyMachineGunButton.png").convert_alpha()
cancelTurretImage = P.image.load("GUIImages/cancelTurretButton.png").convert_alpha()
upgradeTurretImage = P.image.load("GUIImages/upgradeTurretButton.png").convert_alpha()
sellTurretImage = P.image.load("GUIImages/sellTurretButton.png").convert_alpha()

#Game control buttons
startWaveImage = P.image.load("GUIImages/startWaveButton.png").convert_alpha()
restartImage = P.image.load("GUIImages/restartButton.png").convert_alpha()
fastForwardImage = P.image.load("GUIImages/fastForwardButton.png").convert_alpha()

#Extra images for better visuals
heartImage = P.image.load("GUIImages/heartImage.png").convert_alpha()
coinImage = P.image.load("GUIImages/coinImage.png").convert_alpha()

#Load fonts for displaying text on the screen
smallBoldedFont = P.font.SysFont("Consolas", 24, bold = True)
largeUnboldedFont = P.font.SysFont("Consolas", 36, bold = False)

"""Load Audio"""

#Load background music
backgroundMusic = "audio/Background_Music.mp3"
P.mixer.music.load(backgroundMusic)
P.mixer.music.set_volume(0.2)


#Load turret sound effects
turretBasicSound = P.mixer.Sound("audio/Turret_Basic_Shot_SFX.mp3")
turretSniperSound = P.mixer.Sound("audio/Turret_Sniper_Shot_SFX.mp3")
turretMachineGunSound = P.mixer.Sound("audio/Turret_MachineGun_Shot_SFX.mp3")
turretBasicSound.set_volume(0.25)
turretMachineGunSound.set_volume(0.25)

#Load win and lose condition sounds
winSound = P.mixer.Sound("audio/win_SFX.mp3")
loseSound = P.mixer.Sound("audio/lose_SFX.mp3")

"""Load Necessary Functions"""

#Function for outputting text onto the screen
def drawText(text, font, textColour, xCoordinatePosition, yCoordinatePosition):
    targetImage = font.render(text, True, textColour)
    screen.blit(targetImage, (xCoordinatePosition, yCoordinatePosition))

def displayData():
    #Draw panel
    P.draw.rect(screen, "black", (S.SCREEN_WIDTH, 0, S.TURRET_PANEL, S.SCREEN_HEIGHT))
    if map.wave <= S.TOTAL_WAVES:
        drawText("Wave " + str(map.wave), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 20, 20)
    else:
        drawText("End", smallBoldedFont, "grey100", S.SCREEN_WIDTH + 20, 20)
    screen.blit(heartImage, (S.SCREEN_WIDTH + 20, 50))
    drawText(str(map.health), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 60, 55)
    screen.blit(coinImage, (S.SCREEN_WIDTH + 20, 90))
    drawText(str(map.money), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 60, 95)

def createTurret(mousePosition):
    #Calculate tile position based on the mouse position
    mouseTileX = mousePosition[0] // S.TILE_SIZE
    mouseTileY = mousePosition[1] // S.TILE_SIZE

    #Calculate the sequential number of the tile
    mouseTileNum = (mouseTileY * S.COLS) + mouseTileX

    #Check if that tile is a platform
    if map.tileMap[mouseTileNum] == 28:

        #Check that there isn't already a turret there
        noTurretOnTile = True
        for turret in turretGroup:

            #If the cursor's position on that platform is equal to the turret's position, noTurretOnTile becomes false and turret can't be placed
            if (mouseTileX, mouseTileY) == (turret.tileX, turret.tileY):
                noTurretOnTile = False

        #If it was free noTurretOnTile becomes true
        #If the basic turret button was clicked
        if turretButtonList[0].selected:
            if noTurretOnTile == True:
                newBasicTurret = T(turretSpriteSheets[0], mouseTileX, mouseTileY, turretBasicSound, turretType = "Basic")
                turretGroup.add(newBasicTurret)

                #Deduct total money with the price of the basic turret
                map.money -= S.TURRET_PRICE[0]

        #If the sniper turret button was clicked
        elif turretButtonList[1].selected:
            if noTurretOnTile == True:
                newSniperTurret = T(turretSpriteSheets[1], mouseTileX, mouseTileY, turretSniperSound, turretType = "Sniper")
                turretGroup.add(newSniperTurret)

                #Deduct total money with the price of the sniper turret
                map.money -= S.TURRET_PRICE[1]

        #If the machine gun turret button was clicked
        elif turretButtonList[2].selected:
            if noTurretOnTile == True:
                newMachineGunTurret = T(turretSpriteSheets[2], mouseTileX, mouseTileY, turretMachineGunSound, turretType = "MachineGun")
                turretGroup.add(newMachineGunTurret)

                #Deduct total money with turret price
                map.money -= S.TURRET_PRICE[2]

#Function for selecting turret to upgrade or sell it
def selectTurret(mousePosition):
    #Calculate tile position based on the mouse position
    mouseTileX = mousePosition[0] // S.TILE_SIZE
    mouseTileY = mousePosition[1] // S.TILE_SIZE

    for turret in turretGroup:
        if (mouseTileX, mouseTileY) == (turret.tileX, turret.tileY):
            return turret

#Function for deselecting a selected turret
def clearSelectedTurret():
    for turret in turretGroup:
        turret.selected = False

def reselectTurret():
    turretButtonList[0].selected = False
    turretButtonList[1].selected = False
    turretButtonList[2].selected = False

"""Creating The Objects"""

#Create the map of the level
map = Map(mapData, spaceMapImage)
map.processWaypointsData()
map.processEntities()

#Create groups for turrets and entities
entityGroup = P.sprite.Group()
turretGroup = P.sprite.Group()

"""Creating Clickable Buttons"""

#Create turret buttons
buyBasicTurretButton = Button(S.SCREEN_WIDTH + 30, 140, buyBasicTurretImage)
buySniperTurretButton = Button(S.SCREEN_WIDTH + 30, 220, buySniperTurretImage)
buyMachineGunButton = Button(S.SCREEN_WIDTH + 30, 300, buyMachineGunImage)
turretButtonList = [buyBasicTurretButton, buySniperTurretButton, buyMachineGunButton]

#Create turret modifier buttons
cancelTurretButton = Button(S.SCREEN_WIDTH + 62, 380, cancelTurretImage)
upgradeTurretButton = Button(S.SCREEN_WIDTH + 30, 460, upgradeTurretImage)
sellTurretButton = Button(S.SCREEN_WIDTH + 62, 540, sellTurretImage)

#Create game control buttons
startWaveButton = Button(S.SCREEN_WIDTH + 64, 620, startWaveImage)
restartButton = Button(S.TOTAL_SCREEN_WIDTH // 2 - 64, S.SCREEN_HEIGHT // 2 + 16, restartImage)
fastForwardButton = Button(S.SCREEN_WIDTH + 150, 30, fastForwardImage)

"""Game Loop"""

#Boolean value to determine condition of game loop
running = True

#Game loop, to allow the screen to continue display
while running:

    clock.tick(S.FPS)

    """Update Section"""

    if gameOver == False:
        #Check if player has lost
        if map.health <= 0:
            gameOver = True
            gameOutcome = -1
        #Check if player has won or lost
        if map.wave > S.TOTAL_WAVES:
            if map.health > 0:
                gameOver = True
                gameOutcome = 1 #Win
            else:
                gameOver = True
                gameOutcome = -1 #Lost
        #Update groups
        entityGroup.update(map)
        turretGroup.update(entityGroup, map)

        #Highlight selected turret
        if selectedTurret: 
            selectedTurret.selected = True
    else:
        if gameOutcome == 1 and not endSoundPlayed:
            P.mixer.music.stop()
            winSound.play()
            endSoundPlayed = True
        elif gameOutcome == -1 and not endSoundPlayed:
            P.mixer.music.stop()
            loseSound.play()
            endSoundPlayed = True

    """Draw Section"""

    #draw map level
    map.draw(screen)

    #enable this to see the waypoints and the path of the entities
    #P.draw.lines(screen, "black", False, map.waypoints)

    #draw groups
    for entity in entityGroup:
        #Draw each entity
        entity.draw(screen)
        #Draw each entity's respective health
        entity.drawHealthBar(screen)
    for turret in turretGroup:
        turret.draw(screen)

    displayData()

    #Check if the game is over
    if gameOver == False:
        #Check if the wave has started
        if waveStarted == False:
            if startWaveButton.draw(screen):
                waveStarted = True
                if not musicLoaded:
                    P.mixer.music.play(-1)
                    musicLoaded = True
        else:
            #Fast forward option
            if fastForwardButton.draw(screen):

                #If it was true it becomes false and vice versa
                fastForwardStatus = not fastForwardStatus

                #If true then increase game speed else use default speed
                if fastForwardStatus:
                    map.gameSpeed = 2
                else:
                    map.gameSpeed = 1

            #Spawn enemies | if current time subtract with last enemy spawn time is more than the rate, spawn enemy
            if P.time.get_ticks() - lastEntitySpawn > (S.ENTITY_SPAWN_RATE / map.gameSpeed):

                #Continue spawning enemies if number of entities spawn is less than the current entity list
                if map.entitiesSpawned < len(map.entityList):
                    entityType = map.entityList[map.entitiesSpawned]
                    entity = ent(entityType, map.waypoints, entityImages)
                    entityGroup.add(entity)
                    map.entitiesSpawned += 1
                    lastEntitySpawn = P.time.get_ticks()

        #Check if the wave has finished
        if map.checkWaveCompletion() == True:
            map.money += S.WAVE_COMPLETED_REWARD

            #Goes to the next wave
            map.wave += 1

            #Prevents wave from continuing directly
            waveStarted = False

            lastEntitySpawn = P.time.get_ticks()
            map.continueNextWave()
            map.processEntities()

        #Draw buttons
        #Button for placing turrets
        #For each turret show cost of turret and draw the button
        drawText(str(S.TURRET_PRICE[0]), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 265, 160)
        screen.blit(coinImage, (S.SCREEN_WIDTH + 230, 155))
        drawText(str(S.TURRET_PRICE[1]), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 265, 240)
        screen.blit(coinImage, (S.SCREEN_WIDTH + 230, 235))
        drawText(str(S.TURRET_PRICE[2]), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 265, 320)
        screen.blit(coinImage, (S.SCREEN_WIDTH + 230, 315))
        if turretButtonList[0].draw(screen) or turretButtonList[1].draw(screen) or turretButtonList[2].draw(screen):
            placingTurrets = True

        #If placing turrets then show the cancel button as well
        if placingTurrets:
            if turretButtonList[0].selected:
                #Show basic turret on cursor
                cursor_rect = cursorTurretImages[0].get_rect()
                cursorPosition = P.mouse.get_pos()
                cursor_rect.center = cursorPosition
                if cursorPosition[0] <= S.SCREEN_WIDTH:
                    screen.blit(cursorTurretImages[0], cursor_rect)
                if cancelTurretButton.draw(screen):
                    placingTurrets = False
                    reselectTurret()
            elif turretButtonList[1].selected:
                #Show sniper turret on cursor
                cursor_rect = cursorTurretImages[1].get_rect()
                cursorPosition = P.mouse.get_pos()
                cursor_rect.center = cursorPosition
                if cursorPosition[0] <= S.SCREEN_WIDTH:
                    screen.blit(cursorTurretImages[1], cursor_rect)
                if cancelTurretButton.draw(screen):
                    placingTurrets = False
                    reselectTurret()
            elif turretButtonList[2].selected:
                #Show machine gun turret on cursor
                cursor_rect = cursorTurretImages[2].get_rect()
                cursorPosition = P.mouse.get_pos()
                cursor_rect.center = cursorPosition
                if cursorPosition[0] <= S.SCREEN_WIDTH:
                    screen.blit(cursorTurretImages[2], cursor_rect)
                if cancelTurretButton.draw(screen):
                    placingTurrets = False
                    reselectTurret()

        #If a placed turret is selected then show the upgrade button
        if selectedTurret:
            #If a turret can be upgraded then show the upgrade button
            if selectedTurret.upgradeLevel < S.TURRET_MAX_LEVEL:
                #For the "turret button" show cost of turret upgrade and draw the button
                drawText(str(selectedTurret.sellPrice), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 233, 561)
                screen.blit(coinImage, (S.SCREEN_WIDTH + 198, 556))
                drawText(str(selectedTurret.upgradePrice), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 265, 483)
                screen.blit(coinImage, (S.SCREEN_WIDTH + 230, 478))
                if upgradeTurretButton.draw(screen):
                    #Check if total money is sufficient to upgrade selected turret
                    if map.money >= selectedTurret.upgradePrice:
                        selectedTurret.upgradeTurret()
                        map.money -= selectedTurret.upgradePrice
                elif sellTurretButton.draw(screen):
                    selectedTurret.kill()
                    map.money += selectedTurret.sellPrice
                    selectedTurret = None

            #If the the turret is at max level keep the sell button displayed
            elif selectedTurret.upgradeLevel < S.TURRET_MAX_LEVEL + 1:
                drawText(str(selectedTurret.sellPrice), smallBoldedFont, "grey100", S.SCREEN_WIDTH + 233, 561)
                screen.blit(coinImage, (S.SCREEN_WIDTH + 198, 556))
                if sellTurretButton.draw(screen):
                    selectedTurret.kill()
                    map.money += selectedTurret.sellPrice
                    selectedTurret = None
    else:
        P.draw.rect(screen, "black", (S.TOTAL_SCREEN_WIDTH // 2 - 200, S.SCREEN_HEIGHT // 2 - 100, 400, 200), border_radius = 30)
        if gameOutcome == -1:
            drawText("GAME OVER", largeUnboldedFont, "white", S.TOTAL_SCREEN_WIDTH // 2 - 90, 280)
            drawText("Entities Passed: " + str(map.displayEntitiesMissed), smallBoldedFont, "white", S.TOTAL_SCREEN_WIDTH // 2 - 120, 320)
            drawText("Entities Killed: " + str(map.displayEntitiesKilled), smallBoldedFont, "white", S.TOTAL_SCREEN_WIDTH // 2 - 120, 340)
        elif gameOutcome == 1:
            drawText("YOU WIN", largeUnboldedFont, "white", S.TOTAL_SCREEN_WIDTH // 2 - 75, 280)
            drawText("Entities Passed: " + str(map.displayEntitiesMissed), smallBoldedFont, "white", S.TOTAL_SCREEN_WIDTH // 2 - 120, 320)
            drawText("Entities Killed: " + str(map.displayEntitiesKilled), smallBoldedFont, "white", S.TOTAL_SCREEN_WIDTH // 2 - 120, 340)
        #Restart wave
        if restartButton.draw(screen):
            waveStarted = False
            musicLoaded = False
            endSoundPlayed = False
            fastForwardStatus = False
            placingTurrets = False
            selectedTurret = None
            gameOver = False
            lastEntitySpawn = P.time.get_ticks()
            map.displayEntitiesMissed = 0
            map.displayEntitiesKilled = 0

            #Reset the map of the level
            map = Map(mapData, spaceMapImage)
            map.processWaypointsData()
            map.processEntities()

            #Empty groups
            entityGroup.empty()
            turretGroup.empty()

    """Event Handler"""
    for event in P.event.get():
        #Quit program
        if event.type == P.QUIT:
            running = False

        #Left mouse click
        if event.type == P.MOUSEBUTTONDOWN and event.button == 1: #event.button == 1 is left mouse button
            #Get the coordinates of the cursor location and pass those values into the turret
            mousePosition = P.mouse.get_pos()
            #Check if mouse is on the game area
            if mousePosition[0] < S.SCREEN_WIDTH and mousePosition[1] < S.SCREEN_HEIGHT:
                #Clear selected turrets
                selectedTurret = None
                clearSelectedTurret()
                if placingTurrets:
                    # Check if total money is sufficient to buy turret
                    if turretButtonList[0].selected and map.money >= S.TURRET_PRICE[0]:
                        createTurret(mousePosition)
                    elif turretButtonList[1].selected and map.money >= S.TURRET_PRICE[1]:
                        createTurret(mousePosition)
                    elif turretButtonList[2].selected and map.money >= S.TURRET_PRICE[2]:
                        createTurret(mousePosition)
                else:
                    selectedTurret = selectTurret(mousePosition)

    #update display
    P.display.flip()
P.quit()