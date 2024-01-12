import random
from settings import Settings as S

class Map():
    def __init__(self, mapData, spaceMapImage):
        self.wave = 1
        self.gameSpeed = 1
        self.health = S.TOTAL_HEALTH
        self.money = S.TOTAL_MONEY
        self.tileMap = []
        self.waypoints = []
        self.mapData = mapData
        self.spaceMapImage = spaceMapImage
        self.entityList = []
        self.entitiesSpawned = 0
        self.entitiesKilled = 0
        self.entitiesMissed = 0
        self.displayEntitiesKilled = 0
        self.displayEntitiesMissed = 0


    def processWaypointsData(self):

        #Look through data of the json file, to get the waypoint coordinates
        for property in self.mapData["layers"]:

            #For tile properties of the map
            if property["name"] == "map":
                self.tileMap = property["data"]

            #For waypoint coordinates of the map
            elif property["name"] == "waypoints":
                for object in property["objects"]:
                    waypointsData = object["polyline"]
                    self.processWaypoints(waypointsData)

    def processWaypoints(self, waypointsData):

        #Iterate through waypoints to extract individual sets of x and y coordinates
        for waypoint in waypointsData:
            xCoordinateWaypoint = waypoint.get("x")
            yCoordinateWaypoint = waypoint.get("y")
            self.waypoints.append((xCoordinateWaypoint, yCoordinateWaypoint))

    def processEntities(self):

        #Add entities of current wave to a list
        entities = S.ENTITY_SPAWN_DATA[self.wave - 1]
        for entityType in entities:
            entitiesToSpawn = entities[entityType]
            for entity in range(entitiesToSpawn):
                self.entityList.append(entityType)

        #Shuffle list to randomise entity spawn
        random.shuffle(self.entityList)

    def checkWaveCompletion(self):
        if (self.entitiesKilled + self.entitiesMissed) == len(self.entityList):
            return True

    def continueNextWave(self):

        #Reset enemy variables
        self.entityList = []
        self.entitiesSpawned = 0
        self.entitiesKilled = 0
        self.entitiesMissed = 0

    def draw(self, surface):
        surface.blit(self.spaceMapImage, (0, 0))