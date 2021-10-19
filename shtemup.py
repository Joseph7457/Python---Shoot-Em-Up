import pygame
import math

# --- To make code more readable
X = 0; Y = 1

# window size
WINDOW_SIZE = [1600, 900]
REFRESH_RATE = 60

# definition of colors
BLACK  = (  0, 0, 0); WHITE = (  255, 255, 255)

# booleans

finished   = False; 
playing = False

# player 1 parameters
PLAYER1_SHIP_SIZE  = 40
PLAYER1_SHIP_SPEED = 10
PLAYER1_SHIP_OFFSET = 100
PLAYER1_SHIP_START_POS = [WINDOW_SIZE[0]//2, WINDOW_SIZE[1]-PLAYER1_SHIP_OFFSET]
PLAYER1_WEAPON_COOLDOWN = 200 # in ms

#Projectiles
PROJECTILE_SPEED   = 20
PROJECTILE_SIZE    = 3
projectiles = []

#Ennemies
ENNEMY_SIZE = 40

#Spawner
spawner = []

#spawnController
spawnController = 0
oldTime = 0
deltaTime = 0
  #Pour le futur

score = 0

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
window.fill(BLACK)

#--- utility function ---#
def normalize2dVector(x, y):
    if not x and not y:
        return (0,0)
    module = math.sqrt(x**2+y**2)
    return (x/module, y/module)


def createSpawnController():
    return{
        'spawnIndex' : 0,
        'waveIndex'  : 0,
        'spawner' : [],
        'enemies': [],
        'timeElapsed': 0
    } 
    

def createSpawner(w, t):
    return{
        'type'   : w,
        'timer'  : t
    }

  
#--- DEFINITION ENTITY ---#

def createEntity(width, height, x=0, y=0, speed = 0):
    return {
        'position': [x, y],
        'direction': [0,0], # normalized
        'speed': speed,
        'size': [width, height],
        'controller' : None # ref to function controlling direction and speed of entity
    }

    #Getters
def getPos(entity):
    return entity['position']

def getDirection(entity):
    return entity['direction']

def getSpeed(entity):
    return entity['speed']

def getSize(entity):
    return entity['size']

    #Setters
def setSpeed(entity, vecteur):
    entity['speed'] = vecteur

def setDirection(entity, x, y):
    entity['direction'][X] = x
    entity['direction'][Y] = y

def setPosition(entity, coords):
    entity['position'][X] = coords[X]
    entity['position'][Y] = coords[Y]

def setSize(entity, x, y):
    entity['size'][X] = x
    entity['size'][Y] = y

    #Method
def move(entity):
    entity['position'][X] += entity['direction'][X] * entity['speed']
    entity['position'][Y] += entity['direction'][Y] * entity['speed']

#--- END ENTITY ---#


#--- SHIPS ---#

def createShip(entity, weaponCooldown = 1, shootingDirectionX = 0, shootingDirectionY = 1, isShooting = False):
    return {
        'entity' : entity,
        'shootingCooldown' : weaponCooldown,
        'timeLastShot' : 0,
        'shootingDirection' : [shootingDirectionX, shootingDirectionY], #vector director [x, y] normalized
        'isShooting' : isShooting
    }

    # getters
def getShipEntity(Ship):
    return Ship['entity']

def getShipShootingCooldown(Ship):
    return Ship['shootingCooldown']

def getShipTimeLastShot(Ship):
    return Ship['timeLastShot']

def getShipShootingDirection(Ship):
    return Ship['shootingDirection']

def isShipShooting(Ship):
    return Ship['isShooting']

    # setters
def setShipEntity(Ship, entity):
    Ship['entity'] = entity

def setShipShootingCooldown(Ship, newCooldown):
    Ship['shootingCooldown'] = newCooldown

def setShipTimeLastShot(Ship, time):
    Ship['timeLastShot'] = time

def setShipShootingDirection(Ship, directionX, directionY):
    Ship['shootingDirection'] = [directionX, directionY]

def stopShipShooting(Ship):
    Ship['isShooting'] = False

def startShipShooting(Ship):
    Ship['isShooting'] = True

    # Methods
def displayShip(Ship, color):
    pygame.draw.circle(window, color, 
                       (int(getPos(getShipEntity(Ship))[X] + getSize(getShipEntity(Ship))[X]//2),
                        int(getPos(getShipEntity(Ship))[Y] + getSize(getShipEntity(Ship))[Y]//2)),
                       getSize(getShipEntity(Ship))[X])

def shipShoot(Ship):
    if((isShipShooting(Ship)) and (pygame.time.get_ticks() - getShipTimeLastShot(Ship) >= getShipShootingCooldown(Ship))):

        setShipTimeLastShot(Ship, pygame.time.get_ticks())

        shipPos = getPos(getShipEntity(Ship))
        shipSize = getSize(getShipEntity(Ship))

        newProjectile = createEntity(PROJECTILE_SIZE*2, PROJECTILE_SIZE*2)
        setPosition(newProjectile, (shipPos[X] + shipSize[X]//2, shipPos[Y] + shipSize[Y]//2))
        setSpeed(newProjectile, PROJECTILE_SPEED)
        setDirection(newProjectile, 0, -1)
        projectiles.append(newProjectile)

def shipMove(Ship):
    move(Ship['entity'])

#--- END SHIPS ---#

#--- ENEMIES ---#
enemies = []

def createEnemy(ship):
    return {
        'ship' : ship,
    }

def getEnemyShip(Enemy):
    return Enemy['ship']

def setShip(Enemy, newShip):
    Enemy['ship'] = newShip

def addEnemy(enemy):
    enemies.append(enemy)
        
def destroyEnemy(index):
    enemies.pop(index)

def displayEnemies():
    for enemy in enemies:
        displayShip(getEnemyShip(enemy), WHITE)

#--- END ENNEMIES ---#

#--- PLAYER ---#
def createPlayer(ship):
    return{
        'ship' : ship,
        'verticalInput' : 0,
        'horrizontalInput' : 0,
    }

    #Methods
def inputPlayerHor(Player, value):
    Player['horrizontalInput'] += value


def inputPlayerVer(Player, value):
    Player['verticalInput'] += value

def inputPlayerShoot(Player):
    shipShoot(getPlayerShip(Player1))

def movePlayer(Player):
    [x, y] = normalize2dVector(Player['horrizontalInput'], Player['verticalInput'])
    setDirection(getShipEntity(Player['ship']), x, y)
    shipMove(Player['ship'])

def inputPlayerShoot(Player):
    startShipShooting(Player['ship'])

def inputPlayerStopShoot(Player):
    stopShipShooting(Player['ship'])

def getPlayerShip(Player):
    return Player['ship']


# Removes all the elements from the list at indexes in the indexesToRemove list, indexesToRemove needs to be in increasing order
def removeFromList(list, indexesToRemove):
    for i in range(len(indexesToRemove)):
        list.pop(indexesToRemove[i] - i) #indexesToRemove[i] >= i because indexesToRemove is in increasing order

#--- Collisions

# Return True if collision occurs, False otherway
def collision_entite(entite1, entite2):
    rect1 = pygame.Rect(getPos(entite1), getSize(entite1))
    rect2 = pygame.Rect(getPos(entite2), getSize(entite2))
    return pygame.Rect.colliderect(rect1, rect2)

def collisionProjectilePlayersEnnemies():
    global score
    indexProjectileToDestroy = []
    indexEnemiesToDestroy = []

    for i in range(len(projectiles)):
        hasCollided = False
        j = 0
        while((j < len(enemies)) and (not hasCollided)): # stop the search if the projectile has already collided
            if collision_entite(projectiles[i],getShipEntity(getEnemyShip(enemies[j]))):
                indexProjectileToDestroy.append(i)
                indexEnemiesToDestroy.append(j)
                hasCollided = True
                score += 1
            j = j + 1

    # Removing projectiles and enemies that has collided
    removeFromList(projectiles, indexProjectileToDestroy) 
    removeFromList(enemies, indexEnemiesToDestroy)
    

#--- PROJECTILE ---#
def displayProjectile():
    for i in range(len(projectiles)):
        pygame.draw.circle(window, WHITE, (int(getPos(projectiles[i])[X]), int(getPos(projectiles[i])[Y])), PROJECTILE_SIZE)

def deplacer_tir():
    for projectile in projectiles:
        move(projectile)

def destroyProjOutBound():
    for projectile in range(len(projectiles)-1):
        if getPos(projectiles[projectile])[Y] < 0:
            projectiles.pop(projectile)

#--- END PROJECTILE ---#

#--- Control

def control():
    global spawnController, oldTime, deltaTime
    if (spawnController == 0):
        spawnController = createSpawnController()
        print()
        spawnController['spawner'].append(   createSpawner( (0   ,0   , 0  ,0   ,0  ,0   ,0   ,0    ,0   ,0   ,0) , 
                                                            (200,200,400,400,300,300, 500, 500 ,500 ,500 ,500)  )  )
    
    if (len (spawnController['spawner']) > 0):
    
        if (spawnController['timeElapsed'] > spawnController['spawner'][0]['timer'][spawnController['spawnIndex']]):
            newEnemy = createEnemy(createShip(createEntity(50, 50, 50+100*spawnController['spawnIndex'], 300)))
            addEnemy(newEnemy)
            spawnController['timeElapsed'] = 0
            spawnController['spawnIndex'] += 1
    
        if ( ( spawnController['spawnIndex'] >= len(spawnController['spawner'][0]['timer'])-1  ) ):
            spawnController['spawner'].pop()
            spawnController['spawnIndex'] = 0
            
    deltaTime = pygame.time.get_ticks()-oldTime
    oldTime   = pygame.time.get_ticks()
    spawnController['timeElapsed'] +=  deltaTime
    
    return

Player1 = createPlayer(createShip(createEntity(PLAYER1_SHIP_SIZE, PLAYER1_SHIP_SIZE, 
                                               PLAYER1_SHIP_START_POS[X], PLAYER1_SHIP_START_POS[Y], 
                                               PLAYER1_SHIP_SPEED),
                                  PLAYER1_WEAPON_COOLDOWN, 0, 1, False))

def inputManager(event):
    global Player1
    if event.type == pygame.KEYDOWN :
        #Player 1
        if event.key == pygame.K_LEFT :
            inputPlayerHor(Player1, -1)
        if event.key == pygame.K_RIGHT :
            inputPlayerHor(Player1, 1)
        if event.key == pygame.K_UP:
            inputPlayerVer(Player1, -1)
        if event.key == pygame.K_DOWN:
            inputPlayerVer(Player1, 1)
        if event.key == pygame.K_SPACE :
            inputPlayerShoot(Player1)


    if event.type == pygame.KEYUP :
        #Player 1
        if event.key == pygame.K_LEFT :
            inputPlayerHor(Player1, 1)
        if event.key == pygame.K_RIGHT :
            inputPlayerHor(Player1, -1)
        if event.key == pygame.K_UP:
            inputPlayerVer(Player1, 1)
        if event.key == pygame.K_DOWN:
            inputPlayerVer(Player1, -1)
        if event.key == pygame.K_SPACE :
            inputPlayerStopShoot(Player1)

# Score

def displayScore():
    displayMessage(scoreFont, "Score: " + str(score), WHITE, (0,0))

def displayMessage(font, string, color, position):
    message = font.render(string, True, color)
    window.blit(message, position)

# Menu

def displayMenu():
    displayMessage(scoreFont, "Shootem'up", WHITE, (WINDOW_SIZE[0]//3, WINDOW_SIZE[1]//3))
    displayMessage(menuFont, "Appuyer sur une touche pour commencer à jouer", WHITE, (100, WINDOW_SIZE[1]-100))


# ----- End function definition

temps = pygame.time.Clock()


for i in range(1, 8):
    addEnemy(createEnemy(createShip(createEntity(ENNEMY_SIZE*2, ENNEMY_SIZE*2, 200*i, 100 ),
                                    1, 0, -1, False)))
    

scoreFont = pygame.font.SysFont('monospace', WINDOW_SIZE[Y]//12, True)
menuFont = pygame.font.SysFont('monospace', WINDOW_SIZE[Y]//20, True)

while not finished:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        if event.type == pygame.KEYDOWN :
            playing = True

    displayMenu()
    pygame.display.flip()

    while playing:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                   finished = True
                   playing = False

            else:
              inputManager(event)


        # erase
        window.fill(BLACK)
        
        # actions
        control()
        deplacer_tir()
        destroyProjOutBound()
        
        shipShoot(getPlayerShip(Player1))
        movePlayer(Player1)

        collisionProjectilePlayersEnnemies()
        
        # display
        displayEnemies()
        displayShip(getPlayerShip(Player1), WHITE)
        displayProjectile()
        displayScore()
        pygame.display.flip()

        temps.tick(60)

pygame.display.quit()
pygame.quit()


