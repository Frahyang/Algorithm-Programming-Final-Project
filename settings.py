class Settings:
    ROWS = 11
    COLS = 17
    TILE_SIZE = 64
    TURRET_PANEL = 320
    SCREEN_WIDTH = TILE_SIZE * COLS
    SCREEN_HEIGHT = TILE_SIZE * ROWS
    TOTAL_SCREEN_WIDTH = SCREEN_WIDTH + TURRET_PANEL
    FPS = 60
    TOTAL_HEALTH = 100
    TOTAL_MONEY = 600
    TOTAL_WAVES = 5

    #Turret animation constants
    ANIMATION_STEPS = 3
    ANIMATION_DELAY = 50

    #Turret upgrades
    TURRET_MAX_LEVEL = 4
    TURRET_PRICE = [200, 600, 3000]
    TURRET_UPGRADE_PRICE = [TURRET_PRICE[0]//2, TURRET_PRICE[1]//2, TURRET_PRICE[2]//2]
    TURRET_SELL_PRICE = [TURRET_PRICE[0]//2, TURRET_PRICE[1]//2, TURRET_PRICE[2]//2]
    BASIC_TURRET_DATA = [
        {
            #Level 1
            "range": 140,
            "attackSpeed": 2000,
            "damage": 5
        },
        {
            #Level 2
            "range": 160,
            "attackSpeed": 1700,
            "damage": 5
        },
        {
            #Level 3
            "range": 180,
            "attackSpeed": 1500,
            "damage": 10
        },
        {
            #Level 4
            "range": 200,
            "attackSpeed": 1300,
            "damage": 20
        },
    ]

    SNIPER_TURRET_DATA = [
        {
            #Level 1
            "range": 600,
            "attackSpeed": 8000,
            "damage": 100
        },
        {
            #Level 2
            "range": 700,
            "attackSpeed": 6000,
            "damage": 100
        },
        {
            #Level 3
            "range": 800,
            "attackSpeed": 5000,
            "damage": 200
        },
        {
            #Level 4
            "range": 900,
            "attackSpeed": 4000,
            "damage": 400
        },
    ]

    MACHINEGUN_TURRET_DATA = [
        {
            #Level 1
            "range": 200,
            "attackSpeed": 200,
            "damage": 5
        },
        {
            #Level 2
            "range": 250,
            "attackSpeed": 150,
            "damage": 10
        },
        {
            #Level 3
            "range": 300,
            "attackSpeed": 100,
            "damage": 20
        },
        {
            #Level 4
            "range": 350,
            "attackSpeed": 50,
            "damage": 20
        },
    ]

    #Entity data
    ENTITY_KILLED_REWARD = 50
    ENTITY_SPAWN_RATE = 800
    ENTITY_SPAWN_DATA = [
        {
            #Wave 1
            "Basic": 15,
            "Fast": 0,
            "Tank": 0,
            "Mini-Boss": 0,
            "Boss": 0
        },
        {
            #Wave 2
            "Basic": 10,
            "Fast": 10,
            "Tank": 0,
            "Mini-Boss": 0,
            "Boss": 0
        },
        {
            #Wave 3
            "Basic": 15,
            "Fast": 15,
            "Tank": 3,
            "Mini-Boss": 0,
            "Boss": 0
        },
        {
            #Wave 4
            "Basic": 5,
            "Fast": 5,
            "Tank": 10,
            "Mini-Boss": 1,
            "Boss": 0
        },
        {
            #Wave 5
            "Basic": 0,
            "Fast": 0,
            "Tank": 0,
            "Mini-Boss": 0,
            "Boss": 1
        },
        {
            #End
            "Basic": 0,
            "Fast": 0,
            "Tank": 0,
            "Mini-Boss": 0,
            "Boss": 0
        }
    ]

    ENTITY_ATTRIBUTE_VALUES = {
        "Basic": {
            "health": 10,
            "speed": 3,
            "reward": 20
        }, 
        "Fast": {
            "health": 5,
            "speed": 10,
            "reward": 50
        },
        "Tank": {
            "health": 800,
            "speed": 1,
            "reward": 200
        },
        "Mini-Boss": {
            "health": 3000,
            "speed": 0.5,
            "reward": 500
        },
        "Boss": {
            "health": 100000,
            "speed": 0.25,
            "reward": 2000
        }
    }

    #Wave completion reward
    WAVE_COMPLETED_REWARD = 1000