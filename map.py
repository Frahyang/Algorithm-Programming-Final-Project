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

    def processWaypointsData(self):
        #Look through data, the json file, to get the waypoint coordinates
        for property in self.mapData["layers"]: #This will access the layers list in the json file
            if property["name"] == "map":
                self.tileMap = property["data"]
            elif property["name"] == "waypoints": #To access the data from the waypoints section and not other properties
                for object in property["objects"]:
                    waypointsData = object["polyline"]
                    self.processWaypoints(waypointsData)

    def processWaypoints(self, waypointsData):
        #Iterate through waypoints to extract individual sets of x and y coordinates
        for waypoint in waypointsData: #Converts dictionary into a 2-tuple
            xCoordinateWaypoint = waypoint.get("x")
            yCoordinateWaypoint = waypoint.get("y")
            self.waypoints.append((xCoordinateWaypoint, yCoordinateWaypoint))

    def processEntities(self):
        entities = S.ENTITY_SPAWN_DATA[self.wave - 1]
        for entityType in entities:
            entitiesToSpawn = entities[entityType]
            for entity in range(entitiesToSpawn):
                self.entityList.append(entityType)
        #Randomise list to shuffle entity spawn
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

    def draw(self, mapLocation):
        mapLocation.blit(self.spaceMapImage, (0, 0))