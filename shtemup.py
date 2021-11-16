"""
https://trello.com/b/1NyyOuI3/shootem-up
"""

import pygame
import math

# --- To make code more readable
X = 0; Y = 1

# window size
WINDOW_SIZE = [1600, 900]
HEIGHT = WINDOW_SIZE[1]
WIDTH  = WINDOW_SIZE[0]
REFRESH_RATE = 60

#paths
ANIMATION_PATH = 'sprites/animations/'
IMAGES_PATH = 'sprites/images/'
SOUND_EFFECT_PATH = 'sounds/soundEffects/'
MUSIC_PATH = 'sounds/musics/'

# definition of colors
BLACK  = (  0, 0, 0); WHITE = (  255, 255, 255)

# player 1 parameters
PLAYER1_SHIP_SIZE  = 80
PLAYER1_SHIP_SPEED = 10
PLAYER1_SHIP_OFFSET = 100
PLAYER1_SHIP_START_POS = [WINDOW_SIZE[0]//2, WINDOW_SIZE[1]-PLAYER1_SHIP_OFFSET]
PLAYER1_WEAPON_COOLDOWN = 200 # in ms
INVULNERABILITY_DURATION = 500 # in ms
LIVES_AT_START = 3

#Projectiles
PROJECTILE_SPEED   = 20
projectiles_axe    = 1
PROJECTILE_SIZE    = 4
Projectiles = {
    'PlayerTeam' : [],
    'EnemyTeam' : [],
}

#Ennemies
ENEMY_SIZE = [125, 200]
ENEMY_WEAPON_COOLDOWN = 500
ENEMY_PROJECTILE_SPEED = 20

# Background
BACKGROUND_SPEED = 10

#Animation and Images to load in bank
ANIMATIONS_TO_LOAD = {
# format:
#   'name'            : (nImages, 'ext', size                     ),
    'player1_base'    : (10     , 'png', [80, 80]                 ),
    'enemy1_base'     : (10     , 'png', [80, 80]                 ),
    'skinA'           : (19     , 'png', [123, 194]               ),
}
IMAGES_TO_LOAD = {
# format:
#   'name'            : (ext   , [sizeX, sizeY]                   ),
    'missing_texture' : ('jpeg', [400, 400]                       ),
    'backGround_1'    : ('tif', [WINDOW_SIZE[X], WINDOW_SIZE[Y]]  ),
    'backGround_2'    : ('tif', [WINDOW_SIZE[X], WINDOW_SIZE[Y]]  ),
}

# Definition of every wave

def setAllWave():

    allWaveData = []



    t = [1000, 2000, 0, 1000 ];
    x = [WIDTH/2, WIDTH/4, 3*WIDTH/4, WIDTH/2 ];
    y = [-250, -250, -250, -250 ];
    s = [5, 6, 6, 5 ];
    typeMov = ["VERTICAL", "VERTICAL", "VERTICAL", "VERTICAL" ];
    skin = ["skinA", "skinA", "skinA", "skinA" ];
    oneWaveData = []
    oneWaveData.append(t);  oneWaveData.append(typeMov); oneWaveData.append(x); oneWaveData.append(y); oneWaveData.append(s), oneWaveData.append(skin)
    allWaveData.append(oneWaveData)


    t = [1000, 2000, 0, 1000 ];
    x = [WIDTH/2, WIDTH/4, 3*WIDTH/4, WIDTH/2 ];
    y = [-250, -250, -250, -250 ];
    s = [5, 6, 6, 5 ];
    typeMov = ["VERTICAL", "VERTICAL", "VERTICAL", "VERTICAL" ];
    skin = ["skinA", "skinA", "skinA", "skinA" ];
    oneWaveData = []
    oneWaveData.append(t);  oneWaveData.append(typeMov); oneWaveData.append(x); oneWaveData.append(y); oneWaveData.append(s), oneWaveData.append(skin)
    allWaveData.append(oneWaveData)



    return allWaveData

allWaveData = setAllWave()


pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
window.fill(BLACK)



#--- utility function ---#
def normalize2dVector(x, y):
    if not x and not y:
        return (0,0)
    module = math.sqrt(x**2+y**2)
    return (x/module, y/module)

def angleToCoords(angle):
    return (math.cos(angle), math.sin(angle))

    # Removes all the elements from the list at indexes in the indexesToRemove list, indexesToRemove needs to be in increasing order
def removeFromList(list, indexesToRemove):
    for i in range(len(indexesToRemove)):
        list.pop(indexesToRemove[i] - i) #indexesToRemove[i] >= i because indexesToRemove is in increasing order

    # linear interpolation between a and b using t as a percentage
def lerp(a, b, t):
    return a + (b - a) * t

    # inverse lerp, used to find the t
def invLerp(a, b, value):
    return (value - a)/(b-a)

    # remap the value between a & b to newA & newB using linera interpolation 
# remap the value between a & b to newA & newB using linera interpolation 
    # remap the value between a & b to newA & newB using linera interpolation 
def reMap(value, a, b, newA, newB):
    return lerp(newA, newB, invLerp(a, b, value))
    
#--- IMAGE BANK ---#
ImageBank = {
    'fixed': {},
    'animated' : {},
}

    # fixed images location follows this format : sprite/Images/imageName.ext
def addImageToBank(imageName, ext, imageScale = [50, 50]):
    image = pygame.image.load(IMAGES_PATH + imageName + '.' + ext).convert_alpha(window)
    ImageBank['fixed'][imageName] = pygame.transform.scale(image, (imageScale[X], imageScale[Y]))

def getFixedImage(imageName):
    if imageName in ImageBank['fixed']:
        return ImageBank['fixed'][imageName]
    else:
        return ImageBank['fixed']['missing_texture']

# animations follows this format : sprite/animations/animationName_k.ext where k between [0, nImages-1]
def addAnimationToBank(animationName, nImages, ext, imageScale):
    ImageBank['animated'][animationName] = []
    for i in range(nImages):
        image = pygame.image.load(ANIMATION_PATH + animationName + '_' + str(i) + '.' + ext).convert_alpha(window)
        ImageBank['animated'][animationName].append(pygame.transform.scale(image, (imageScale[X], imageScale[Y])))

def getAnimationFrame(animationName, frame):
    if animationName in ImageBank['animated'] and frame < len(ImageBank['animated'][animationName]):
        return ImageBank['animated'][animationName][frame]
    else:
        return ImageBank['fixed']['missing_texture']

def getLenAnimation(animationName):
    if animationName in ImageBank['animated']:
        return len(ImageBank['animated'][animationName])
    else:
        return 0

def fillImageBank():
    for image in IMAGES_TO_LOAD:
        addImageToBank(image, *IMAGES_TO_LOAD[image])
    for animation in ANIMATIONS_TO_LOAD:
        addAnimationToBank(animation, *ANIMATIONS_TO_LOAD[animation])

fillImageBank()
#--- END IMAGE BANK ---#


#--- AMIMATIONS ---#

def createAnimation(animationName, animationSpeed):
    return{
        'animationName' : animationName,
        'frameDuration' : animationSpeed * REFRESH_RATE,
        'timeSinceLastAnim' : 0,
        'indexCurrImage': 0,
    }

def getNextAnimationFrame(animation, time):
    animation['indexCurrImage'] = (animation['indexCurrImage'] + 1) % getLenAnimation(animation['animationName'])
    animation['timeSinceLastAnim'] = time
    return getAnimationFrame(animation['animationName'], animation['indexCurrImage'])

def shouldAnimate(animation, currTime):
    return animation['timeSinceLastAnim'] + animation['frameDuration'] < currTime

#--- END ANIMATION ---#

#--- ENTITY ---#

def createEntity(width, height, x=0, y=0, speed = 0, mT = ""):
    return {
        'position': [x, y],
        'direction': [0,0], # normalized
        'speed': speed,
        'size': [width, height],
        'currImage' : pygame.transform.scale(getFixedImage('missing_texture'), (width, height)),
        'isAnimated' : False,
        'animations' : {},
        'currAnimation' : None,
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

def resizeEntity(entity, x, y):
    entity['size'][X] = x
    entity['size'][Y] = y
    entity['currImage'] = pygame.transform.scale(entity['currImage'], (x, y))

def addEntityAnimation(entity, animationName, animationRef, animationSpeed):
    entity['isAnimated'] = True
    if not entity['animations']:
        entity['currAnimation'] = animationName
    entity['animations'][animationName] = createAnimation(animationRef, animationSpeed)

def animateEntity(entity):
    entity['isAnimated'] = True

def inanimateEntity(entity):
    entity['isAnimated'] = False

def switchEntityAnimation(entity, animationName):
    if entity['animations']:
        if animationName in entity['animations']:
            entity['currAnimation'] = animationName

    #Method
def move(entity):
    entity['position'][X] += entity['direction'][X] * entity['speed']
    entity['position'][Y] += entity['direction'][Y] * entity['speed']

def displayEntity(entity, currTime):
    if entity['isAnimated']:
        if shouldAnimate(entity['animations'][entity['currAnimation']], currTime):
            entity['currImage'] = pygame.transform.scale(getNextAnimationFrame(entity['animations'][entity['currAnimation']], currTime), entity['size'])
    window.blit(entity['currImage'], entity['position']) #[X] - entity['size'][X]//2, entity['position'][Y]- entity['size'][Y]//2])

#--- END ENTITY ---#


#--- SHIPS ---#

def createShip(entity, weaponCooldown = 200, shootingDirectionX = 0, shootingDirectionY = 1, isShooting = False):
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
def displayShip(Ship, time):
    displayEntity(getShipEntity(Ship), time)

def shipShoot(Ship, time, isEnemy = True):
    if((isShipShooting(Ship)) and (time - getShipTimeLastShot(Ship) >= getShipShootingCooldown(Ship))):

        setShipTimeLastShot(Ship, time)

        shipPos = getPos(getShipEntity(Ship))
        shipSize = getSize(getShipEntity(Ship))

        newProjectile = createEntity(PROJECTILE_SIZE*2, PROJECTILE_SIZE*2)
        direction = getShipShootingDirection(Ship)
        setDirection(newProjectile, direction[X], direction[Y])

        # Calcul de la position de départ du projectile

        posY = shipPos[Y] + shipSize[Y]//2
        if direction[Y] < 0:
            posY = shipPos[Y]
        elif direction[Y] > 0:
            posY = shipPos[Y] + shipSize[Y]

        posX = shipPos[X] + (shipSize[X]//2)
        if direction[X] < 0:
            posX = shipPos[X]
        elif direction[X] > 0:
            posX = shipPos[X] + shipSize[X]

        setPosition(newProjectile, (shipPos[X] + (shipSize[X]//2)+(shipSize[X]//2)*direction[X], posY ))

        if isEnemy:
            setSpeed(newProjectile, ENEMY_PROJECTILE_SPEED)
            Projectiles['EnemyTeam'].append(newProjectile)
        else:
            setSpeed(newProjectile, PROJECTILE_SPEED)
            Projectiles['PlayerTeam'].append(newProjectile)

def shipMove(Ship):
    move(Ship['entity'])

#--- END SHIPS ---#


#--- ENEMIES ---#
Enemies = []

def createEnemy(ship, moveType):
    return {
        'ship' : ship,
        'initPos' : [0,0],
        'moveType' : moveType, # ref to function controlling direction and speed of entity
    }

def moveEnemy(enemy, time):
    if (enemy['moveType'] == "VERTICAL"):
        setDirection(getShipEntity(enemy['ship']), *angleToCoords(math.pi/2))

    elif (enemy['moveType'] == "HORIZONTAL"):
        setDirection(getShipEntity(enemy['ship']), *angleToCoords(0))

    elif (enemy['moveType'] == "DIAGONAL"):
        setDirection(getShipEntity(enemy['ship']), *angleToCoords(3*math.pi/8))

    elif (enemy['moveType'] == "REBONDG"):
        t = time
        while(t>1000):
            t -= 1000
        d = reMap(t, 0,1000, 0, math.pi/2)
        setDirection(getShipEntity(enemy['ship']), *angleToCoords(-d))

    elif (enemy['moveType'] == "REBONDD"):
        t = time
        while(t>1000):
            t -= 1000
        d = reMap(t, 0,1000, 0, math.pi/2)
        setDirection(getShipEntity(enemy['ship']), angleToCoords(d))
    shipMove(enemy['ship'])

def getEnemyShip(Enemy):
    return Enemy['ship']

def setShip(Enemy, newShip):
    Enemy['ship'] = newShip

def addEnemy(enemy):
    Enemies.append(enemy)
        
def removeEnemy(index):
    Enemies.pop(index)

def displayEnemy(enemy, time):
    displayShip(enemy['ship'], time)
    
def displayEnemies(enemies, time):
    for enemy in Enemies:
        displayEnemy(enemy, time)
        
def enemiesShoot(time):
    for enemy in Enemies:
        shipShoot(getEnemyShip(enemy), time)

def moveAllEnnemies(enemies, time):
    for e in  enemies:
        moveEnemy(e, time)

#--- END ENNEMIES ---#

#--- PLAYER ---#
def createPlayer(ship):
    return{
        'ship' : ship,
        'verticalInput' : 0,
        'horizontalInput' : 0,
        'lives': LIVES_AT_START,
        'invulnerable': False,
        'lastTimeHit': 0
    }

    #Methods
def inputPlayerHor(Player, value):
    Player['horizontalInput'] += value

def inputPlayerVer(Player, value):
    Player['verticalInput'] += value

def movePlayer(Player):
    [x, y] = normalize2dVector(Player['horizontalInput'], Player['verticalInput'])
    setDirection(getShipEntity(Player['ship']), x, y)
    shipMove(Player['ship'])

def inputPlayerShoot(Player):
    startShipShooting(Player['ship'])

def inputPlayerStopShoot(Player):
    stopShipShooting(Player['ship'])

def getPlayerShip(Player):
    return Player['ship']

def resetPlayerInput(Player):
    Player['horizontalInput'] = 0
    Player['verticalInput'] = 0

def isInvulnerable(Player):
    return Player['invulnerable']

def onPlayerHit(Player, time):
    Player['invulnerable'] = True
    Player['lives'] -= 1
    Player['lastTimeHit'] = time

def updateInvulnerability(Player, time):
    if (time - Player['lastTimeHit']) >= INVULNERABILITY_DURATION:
        Player['invulnerable'] = False

def getPlayerLives(Player):
    return Player['lives']

#--- Collisions

# Return True if collision occurs, False otherway
def collision_entite(entite1, entite2):
    rect1 = pygame.Rect(getPos(entite1), getSize(entite1))
    rect2 = pygame.Rect(getPos(entite2), getSize(entite2))
    return pygame.Rect.colliderect(rect1, rect2)

# Deletes enemies and projectiles who collide
def collisionEnnemiesProjectile(enemies, projectiles):
    global score
    indexProjectileToDestroy = []
    indexEnemiesToDestroy = []

    for i in range(len(projectiles)):
        hasCollided = False
        j = 0
        while((j < len(enemies)) and (not hasCollided)): # stop the search if the projectile has already collided
            if collision_entite(projectiles[i], getShipEntity(getEnemyShip(enemies[j]))):
                indexProjectileToDestroy.append(i)
                indexEnemiesToDestroy.append(j)
                hasCollided = True
                score += 1
            j = j + 1

    # Removing projectiles and enemies that has collided
    removeFromList(projectiles, indexProjectileToDestroy) 
    removeFromList(enemies, indexEnemiesToDestroy)
    
# Returns True if the player collides with an enemy
def collisionPlayerEnnemies(player, enemies):
    for enemy in enemies:
        if collision_entite(getShipEntity(getEnemyShip(enemy)), getShipEntity(getPlayerShip(player))):
            return True
    return False

# Returns True if the player collides with a projectile from a list
def collisionPlayerProjectile(player, projectiles):    
    for enemy in projectiles:
        if collision_entite(enemy, getShipEntity(getPlayerShip(player))):
            return True
    return False

#--- PROJECTILE ---#
def displayProjectiles(projectiles):
    for projectile in projectiles:
        pygame.draw.circle(window, WHITE, (int(getPos(projectile)[X]), int(getPos(projectile)[Y])), PROJECTILE_SIZE)

def moveProjectiles(projectiles):
    for projectile in projectiles:
        move(projectile)

def destroyProjOutBound(projectiles):
    toRemove = []
    for i in range(len(projectiles)-1):
        pos = getPos(projectiles[i])
        if pos[Y] < 0 or pos[Y] > WINDOW_SIZE[Y] or pos[X] < 0 or pos[X] > WINDOW_SIZE[X]:
            toRemove.append(i)

    removeFromList(projectiles, toRemove)

#--- END PROJECTILE ---#

#--- Control ---#
spawner = []
spawnController = 0
oldTime = 0
deltaTime = 0

def createSpawnController():
    return{
        'spawnIndex' : 0,
        'waveIndex'  : 0,
        'spawner' : [],
        'timeElapsed': 0
    } 

def createSpawner(t, w, x, y, s, skin):
    return{
        'type'   : w,
        'timer'  : t,
        'x'      : x,
        'y'      : y,
        'speed'  : s,
        'skin'   : skin
    }

def initializeSpawners():
    global spawnController
    # celle  ci il faudrait l'extraire , elle fait part de l'initialisation
    if (spawnController == 0):
        spawnController = createSpawnController()
        # allWaveData [Vague][type de données][index 
        for w in range(len(allWaveData)):
            spawner = createSpawner(allWaveData[w][0], allWaveData[w][1],allWaveData[w][2], allWaveData[w][3], allWaveData[w][4], allWaveData[w][5])
            spawnController['spawner'].append(spawner)
    # jusqu'ici je pense

def control(time):
    global spawnController, oldTime, deltaTime

    initializeSpawners()

    if (len (spawnController['spawner']) > 0):
    
        if (spawnController['timeElapsed'] > spawnController['spawner'][0]['timer'][spawnController['spawnIndex']] ):
            wi = spawnController['waveIndex']; i = spawnController['spawnIndex']

            newEnemy = createEnemy(createShip(createEntity( ENEMY_SIZE[X], ENEMY_SIZE[Y], 
                                                            spawnController['spawner'][wi]['x'][i], 
                                                            spawnController['spawner'][wi]['y'][i],
                                                            spawnController['spawner'][wi]['speed'][i],
                                                            )), 
                                    spawnController['spawner'][wi]['type'][i] )

            setShipShootingCooldown(getEnemyShip(newEnemy), ENEMY_WEAPON_COOLDOWN)
            startShipShooting(getEnemyShip(newEnemy))
            setShipShootingDirection(getEnemyShip(newEnemy), 0,  1)            

            addEntityAnimation(getShipEntity(getEnemyShip(newEnemy)), 'Skin_1', spawnController['spawner'][wi]['skin'][i], 1)
            addEnemy(newEnemy)  
                                #spawnController['spawner'][0]['type'][spawnController['spawnIndex']]
            spawnController['timeElapsed'] = 0
            spawnController['spawnIndex'] += 1
    
    if (len(spawnController['spawner']) > 0):
        if ( ( spawnController['spawnIndex'] >= len(spawnController['spawner'][0]['timer'])  ) ):
            spawnController['spawner'].pop(0)
            spawnController['spawnIndex'] = 0
            #spawnController['waveIndex'] += 1
            
    deltaTime = time-oldTime
    oldTime   = time
    spawnController['timeElapsed'] +=  deltaTime

    
Player1 = createPlayer(createShip(createEntity(PLAYER1_SHIP_SIZE, PLAYER1_SHIP_SIZE, 
                                               PLAYER1_SHIP_START_POS[X], PLAYER1_SHIP_START_POS[Y], 
                                               PLAYER1_SHIP_SPEED),
                                  PLAYER1_WEAPON_COOLDOWN, 0, -1, False))
addEntityAnimation(getShipEntity(getPlayerShip(Player1)), 'Skin_Base', 'player1_base', 0.4)


def inputManager(event):
    global Player1, finished, playing, projectiles_axe 
    if event.type == pygame.KEYDOWN :
        #Player 1
        if event.key == pygame.K_q or event.key == pygame.K_LEFT:
            inputPlayerHor(Player1, -1)
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            inputPlayerHor(Player1, 1)
        if event.key == pygame.K_z or event.key == pygame.K_UP:
            inputPlayerVer(Player1, -1)
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            inputPlayerVer(Player1, 1)
        if event.key == pygame.K_SPACE :
            inputPlayerShoot(Player1)
        if event.key == pygame.K_LCTRL:
            if (projectiles_axe == 1 ):
                projectiles_axe  =-1
                setShipShootingDirection(getPlayerShip(Player1), 0, -1)
            else:
                projectiles_axe =1
                setShipShootingDirection(getPlayerShip(Player1), 0, 1)

        if event.key == pygame.K_ESCAPE:
            finished = True
            playing = False 

    if event.type == pygame.KEYUP :
        #Player 1
        if event.key == pygame.K_q or event.key == pygame.K_LEFT:
            inputPlayerHor(Player1, 1)
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            inputPlayerHor(Player1, -1)
        if event.key == pygame.K_z or event.key == pygame.K_UP:
            inputPlayerVer(Player1, 1)
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            inputPlayerVer(Player1, -1)
        if event.key == pygame.K_SPACE :
            inputPlayerStopShoot(Player1)


#--- BACKGROUND ---#
# Background
BGx = 0
BGy = [0, -WINDOW_SIZE[1]]

def BG():
    moveBG()
    reinitialiseBG()
    displayBG()

def displayBG():
    window.blit(getFixedImage('backGround_1'), (BGx, BGy[0]))
    window.blit(getFixedImage('backGround_2'), (BGx, BGy[1]))
    

def moveBG():
    global BGy
    BGy[0] += BACKGROUND_SPEED
    BGy[1] += BACKGROUND_SPEED

def reinitialiseBG():
    if(BGy[0]>WINDOW_SIZE[1]):
        BGy[0] = - WINDOW_SIZE[1]
    if(BGy[1]>WINDOW_SIZE[1]):
        BGy[1] = - WINDOW_SIZE[1]

#--- END BACKGROUND ---#


# Score
score = 0
def displayScore():
    displayMessage(scoreFont, "Score: " + str(score), WHITE, (0,0))

def displayMessage(font, string, color, position):
    message = font.render(string, True, color)
    window.blit(message, position)

# Menu

def displayMenu():
    displayMessage(scoreFont, "Shootem'up", WHITE, (WINDOW_SIZE[0]//3, WINDOW_SIZE[1]//3))
    displayMessage(menuFont, "Appuyer sur une touche pour commencer à jouer", WHITE, (100, WINDOW_SIZE[1]-100))

# Lives

def displayLives():
    displayMessage(scoreFont, "Lives: " + str(getPlayerLives(Player1)), WHITE, (0,WINDOW_SIZE[Y]-100))

# used to restart everything when going back to the menu from playing.
def restart():
    global spawnController, score
    spawnController = 0    
    initializeSpawners()
    setPosition(getShipEntity(getPlayerShip(Player1)), PLAYER1_SHIP_START_POS)

    Enemies.clear()
    Projectiles['PlayerTeam'].clear()
    Projectiles['EnemyTeam'].clear()
    resetPlayerInput(Player1)
    score = 0
    Player1['lives'] = LIVES_AT_START

# ----- End function definition

temps = pygame.time.Clock()
    
scoreFont = pygame.font.SysFont('monospace', WINDOW_SIZE[Y]//12, True)
menuFont = pygame.font.SysFont('monospace', WINDOW_SIZE[Y]//20, True)


finished   = False
playing = False

while not finished:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        if event.type == pygame.KEYDOWN :
            playing = True
            inputManager(event)

    window.fill(BLACK)
    displayMenu()
    pygame.display.flip()
    
    while playing:

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                   finished = True
                   playing = False

            else:
              inputManager(event)


        # erase
        #window.fill(BLACK)
        #BG()
        window.fill(BLACK)
        
        
        # actions
        control(current_time)
        moveProjectiles(Projectiles['EnemyTeam'])
        moveProjectiles(Projectiles['PlayerTeam'])
        destroyProjOutBound(Projectiles['EnemyTeam'])
        destroyProjOutBound(Projectiles['PlayerTeam'])

        shipShoot(getPlayerShip(Player1), current_time, False)
        enemiesShoot(current_time)
        movePlayer(Player1)

        moveAllEnnemies(Enemies, current_time)
        collisionEnnemiesProjectile(Enemies, Projectiles['PlayerTeam'])

        if not isInvulnerable(Player1):
            if collisionPlayerEnnemies(Player1, Enemies) or collisionPlayerProjectile(Player1, Projectiles['EnemyTeam']):
                onPlayerHit(Player1, current_time)
                if getPlayerLives(Player1) <= 0:
                    playing = False
                    restart()
        else:
            updateInvulnerability(Player1, current_time)
        
        # display
        displayEnemies(Enemies, current_time)
        displayShip(getPlayerShip(Player1), current_time)
        displayProjectiles(Projectiles['EnemyTeam'])
        displayProjectiles(Projectiles['PlayerTeam'])
        displayScore()
        displayLives()
        pygame.display.flip()

        temps.tick(60)

pygame.display.quit()
pygame.quit()



