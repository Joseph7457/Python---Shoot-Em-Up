"""
https://trello.com/b/1NyyOuI3/shootem-up
"""

from ctypes.wintypes import RGB
import pygame
import math
import json

from pygame import color


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
BLACK  = (  0, 0, 0)
WHITE = (  255, 255, 255)
MIDNIGHT_BLUE = (25, 25, 120)

# player 1 parameters
PLAYER1_SHIP_SIZE  = [80, 80]
PLAYER1_SHIP_SPEED = 10
PLAYER1_SHIP_OFFSET = 100
PLAYER1_SHIP_START_POS = [WINDOW_SIZE[0]//2, WINDOW_SIZE[1]-PLAYER1_SHIP_OFFSET]
PLAYER1_WEAPON_COOLDOWN = 200 # in ms
INVULNERABILITY_DURATION = 500 # in ms
LIVES_AT_START = 30

#Projectiles
    # declare your projectiles here first then create a weapon based on it
PROJECTILE_BLUEPRINTS = {
   #'projectileName' : (size    , 'Animation'    , 'AnimationOnHit'    , onHitSize, speed, movementType, projectileDamage),
    'blasterShot'    : ([15, 15], 'enemy1_base'  , 'ClusterExplosion'  , [80, 80] , 10   , None        , 1               ),
}

Projectiles = {
    'PlayerTeam' : [],
    'EnemyTeam' : [],
    'toDestroy' : [],
}

#Ennemies
ENEMY_WEAPON_COOLDOWN = 500
ENEMY_PROJECTILE_SPEED = 20

# Background
BACKGROUND_SPEED = 7

#Animation and Images to load in bank
ANIMATIONS_TO_LOAD = {
# format:
#   'name'            : (nImages, 'ext', size                     ),
    'ClusterExplosion': (11     , 'png', [48, 48]                 ),
    'player1_base'    : (10     , 'png', [80, 80]                 ),
    'enemy1_base'     : (10     , 'png', [80, 80]                 ),
    'skinA'           : (19     , 'png', [123, 194]               ),
    'V0'              : (8      , 'png', [128, 128]               ), 
    'V1'              : (5      , 'png', [192, 128]               ), 
    'V2'              : (35     , 'png', [152, 180]               ), 
    'V3'              : (27     , 'png', [111, 192]               ), 
    'V4'              : (62     , 'png', [256, 256]               ), 
    'V5'              : (13     , 'png', [256, 256]               ), 
    'V6'              : (35     , 'png', [224, 180]               ), 
    'V7'              : (4      , 'png', [224, 228]               ), 
    'V8'              : (9      , 'png', [120, 112]               ),
    'V9'              : (27     , 'png', [256, 256]               ),  
    'V10'             : (17     , 'png', [128, 112]               ),
    'V11'             : (1      , 'png', [128, 128]               ),
}
IMAGES_TO_LOAD = {
# format:
#   'name'            : (ext   , [sizeX, sizeY]                   ),
    'missing_texture' : ('jpeg', [400, 400]                       ),
    'backGround_1'    : ('png', [WINDOW_SIZE[X], 8*WINDOW_SIZE[Y]]  ),
    'backGround_2'    : ('png', [WINDOW_SIZE[X], 8*WINDOW_SIZE[Y]]  ),
}

# Definition of every wave
niveau_1 = ["data.json", "data.json", "data.json"]


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

def getCurrAnimationFrame(animation):
    return animation['indexCurrImage']

def shouldAnimate(animation, currTime):
    return animation['timeSinceLastAnim'] + animation['frameDuration'] < currTime

#--- END ANIMATION ---#

#--- ENTITY ---#

def createEntity(width = 10 , height = 10, x=0, y=0, speed = 0, scale = 1):
    return {
        'position': [x, y],
        'direction': [0,0], # normalized
        'speed': speed,
        'size': [width, height],
        'currImage' : pygame.transform.scale(getFixedImage('missing_texture'), (width, height)),
        'isAnimated' : False,
        'animations' : {},
        'currAnimation' : None,
        'scale': scale 
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

def getEntityCurrAnimationFrame(entity):
    if entity['isAnimated']:
        return getCurrAnimationFrame(entity['animations'][entity['currAnimation']])

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
    result = False
    if entity['isAnimated']:
        if shouldAnimate(entity['animations'][entity['currAnimation']], currTime):
            entity['currImage'] = pygame.transform.scale(getNextAnimationFrame(entity['animations'][entity['currAnimation']], currTime), entity['size'])
    window.blit(entity['currImage'], entity['position']) #[X] - entity['size'][X]//2, entity['position'][Y]- entity['size'][Y]//2])
    #pygame.draw.circle(window, RGB(255,0,0), entity['position'], 10, width=0) # Optionel. Outil de dev

#--- END ENTITY ---#

#--- PROJECTILE ---#
def createProjectile(size, Animation, AnimationOnHit, onHitSize, speed, movementType, projectileDamage, direction, position):
    projectileEntity = createEntity(size[X], size[Y], position[X], position[Y], speed)
    setDirection(projectileEntity, direction[X], direction[Y])
    addEntityAnimation(projectileEntity, 'standardAnimation', Animation, 0.4)
    addEntityAnimation(projectileEntity, 'AnimationOnHit', AnimationOnHit, 0.4)

    return {
        'entity' : projectileEntity,
        'onHitSize' : onHitSize,
        'damage' : projectileDamage,
        'movementType' : movementType,
    }

def projectileOnHit(projectiles, index):
    switchEntityAnimation(projectiles[index]['entity'], 'AnimationOnHit')
    setSpeed(projectiles[index]['entity'], 0)
    resizeEntity(projectiles[index]['entity'], *projectiles[index]['onHitSize'])
    position = getPos(projectiles[index]['entity']) 
    position[X] -= projectiles[index]['onHitSize'][X]//2
    position[Y] -= projectiles[index]['onHitSize'][Y]//2
    setPosition(projectiles[index]['entity'], position)
    Projectiles['toDestroy'].append(projectiles[index])
   
def addProjectile(projectileTeam, projectile):
   Projectiles[projectileTeam].append(projectile)

def moveProjectiles(projectiles):
    for projectile in projectiles:
        move(projectile['entity'])

def displayProjectiles(projectiles, currTime):
   for projectile in projectiles:
      displayEntity(projectile['entity'], currTime)

def updateProjectilesToDestroy():
    projectilesIndexToRemove = []
    for i in range(len(Projectiles['toDestroy'])):
        if(not getEntityCurrAnimationFrame(Projectiles['toDestroy'][i]['entity'])):
            projectilesIndexToRemove.append(i)
      
    removeFromList(Projectiles['toDestroy'], projectilesIndexToRemove)

def destroyProjOutBound(projectiles):
    toRemove = []
    for i in range(len(projectiles)-1):
        pos = getPos(projectiles[i]['entity'])
        if pos[Y] < 0 or pos[Y] > WINDOW_SIZE[Y] or pos[X] < 0 or pos[X] > WINDOW_SIZE[X]:
            toRemove.append(i)

    removeFromList(projectiles, toRemove)



#--- END PROJECTILE ---#


#--- WEAPON ---#
def createWeapon(projectileBP, offset, ownerTeam, cooldown):
    return {
        'projectileSize' : projectileBP[0],
        'projectileAnimation' : projectileBP[1],
        'projectileOnHitAnimation' : projectileBP[2],
        'projectileOnHitSize' : projectileBP[3],
        'projectileSpeed' : projectileBP[4],
        'projectileMoveType' : projectileBP[5],
        'projectileDamage' : projectileBP[6],
        'offset' : offset,
        'ownerTeam' : ownerTeam,
        'cooldown' : cooldown,
        'lastShot' : 0,
    }

def setWeaponDamage(weapon, damage):
    weapon['projectileDamage'] = damage

def setWeaponProjSpeed(weapon, speed):
    weapon['projectileSpeed'] = speed    

def setWeaponCooldown(weapon, cooldown):
    weapon['cooldown'] = cooldown

def weaponShoot(weapon, position, currTime, direction = None):
    if(currTime - weapon['lastShot'] >= weapon['cooldown']):
        if(not direction):
            if weapon['ownerTeam'] == 'PlayerTeam':
                direction = [0, -1]
            else:
                direction = [0, 1]
        addProjectile(weapon['ownerTeam'], createProjectile(weapon['projectileSize'], weapon['projectileAnimation'],
                                                            weapon['projectileOnHitAnimation'], weapon['projectileOnHitSize'],
                                                            weapon['projectileSpeed'], weapon['projectileMoveType'], 
                                                            weapon['projectileDamage'], direction, 
                                                            [position[X] + weapon['offset'][X]-weapon['projectileSize'][X]//2, position[Y] + weapon['offset'][Y]-weapon['projectileSize'][Y]//2]))
        weapon['lastShot'] = currTime

#--- END WEAPON ---#


#--- SHIPS ---#

def createShip(entity, isShooting = False):
    return {
        'entity' : entity,
        'isShooting' : isShooting,
        'weapons' : [],
        'weaponInUse' : 0,
    }

    # getters
def getShipEntity(Ship):
    return Ship['entity']

def isShipShooting(Ship):
    return Ship['isShooting']

    # setters
def setShipEntity(Ship, entity):
    Ship['entity'] = entity

def stopShipShooting(Ship):
    Ship['isShooting'] = False

def startShipShooting(Ship):
    Ship['isShooting'] = True

    # Methods
def addWeaponToShip(Ship, projectileBP, weaponOffset, ownerTeam, cooldown):
    Ship['weapons'].append(createWeapon(projectileBP, weaponOffset, ownerTeam, cooldown))

def displayShip(Ship, time):
    displayEntity(getShipEntity(Ship), time)

def switchWeapon(Ship, index = -1):
    if(Ship['weapons']):
        if index == -1:
            Ship['weaponInUse'] = (Ship['weaponInUse'] + 1)%len(Ship['weapons']) 
        else :
            if index < len(Ship['weapons']):
                Ship['weaponInUse'] = index

def shipShoot(Ship, time):
    # TODO add offset to weapon & way to change projectile direction
    if Ship['isShooting']:
        print("\n\n Le vaisseau est : \n")
        print(Ship['entity']['currImage'])
        w = Ship['entity']['currImage'].get_width()
        h = Ship['entity']['currImage'].get_height()
        pos = [w/2,h]
        pos[0] += getPos(getShipEntity(Ship))[0]
        pos[1] += getPos(getShipEntity(Ship))[1]
        # pygame.draw.circle(window, RGB(255,0,0), pos, 15, width=0) #Optionel, outil de dev
        weaponShoot(Ship['weapons'][Ship['weaponInUse']], getPos(getShipEntity(Ship)), time)


def shipMove(Ship):
    move(Ship['entity'])

#--- END SHIPS ---#


#--- ENEMIES ---#
Enemies = []

def createEnemy(ship, moveType = ""):
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
    for enemy in enemies:
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
    Player['horizontalInput'] = value

def inputPlayerVer(Player, value):
    Player['verticalInput'] = value

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
    global leftInput, rightInput, downInput, upInput
    Player['horizontalInput'] = 0
    Player['verticalInput'] = 0
    leftInput = 0
    rightInput = 0
    upInput = 0
    downInput = 0

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
    indexEnemiesToDestroy = []
    indexProjectileToDestroy = []

    for i in range(len(projectiles)):
        hasCollided = False
        j = 0
        while((j < len(enemies)) and (not hasCollided)): # stop the search if the projectile has already collided
            if collision_entite(projectiles[i]['entity'], getShipEntity(getEnemyShip(enemies[j]))):
                indexEnemiesToDestroy.append(j)
                indexProjectileToDestroy.append(i)
                hasCollided = True
                score += 1
                projectileOnHit(projectiles, i)
            j = j + 1

    # Removing projectiles and enemies that has collided
    removeFromList(enemies, indexEnemiesToDestroy)
    removeFromList(projectiles, indexProjectileToDestroy)
    
# Returns True if the player collides with an enemy
def collisionPlayerEnnemies(player, enemies):
    for enemy in enemies:
        if collision_entite(getShipEntity(getEnemyShip(enemy)), getShipEntity(getPlayerShip(player))):
            return True
    return False

# Returns True if the player collides with a projectile from a list
def collisionPlayerProjectile(player, projectiles):
    for projectileIndex in range(len(projectiles)):
        if collision_entite(projectiles[projectileIndex]['entity'], getShipEntity(getPlayerShip(player))):
            projectileOnHit(projectiles, projectileIndex)
            removeFromList(projectiles, [projectileIndex])
            return True
    return False


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



def initializeSpawners(nomFichier):
    global spawnController

    if (spawnController == 0):
        spawnController = createSpawnController()           # Création du controller

        for w in range(len(nomFichier)):                    # Ajouter toutes les vagues du niveau

            with open(nomFichier[0], "r") as read_file:        # Importation des données 
                vague = json.load(read_file)
            spawnController['spawner'].append(vague)
 

def control(time):
    global spawnController, oldTime, deltaTime

    initializeSpawners(niveau_1)
    if (len (spawnController['spawner']) > 0):
    
        if (spawnController['timeElapsed'] > spawnController['spawner'][0]['timer'][spawnController['spawnIndex']] ): # ok

            wi = spawnController['waveIndex']; i = spawnController['spawnIndex']                                      # i et wi pour confort de lecture


            scale = spawnController['spawner'][wi]['scale'][i]                                                        #ok

            w = int(ImageBank['animated'][spawnController['spawner'][wi]['skin'][i]][0].get_width()*scale)            #ok
            h = int(ImageBank['animated'][spawnController['spawner'][wi]['skin'][i]][0].get_height()*scale)
            print ( "la largeur est de " + str(w))  
            print ( "la hauteur est de " + str(h))

            newEnemy = createEnemy(createShip(createEntity(w,h)))

            # Mouvement 
            moveType = spawnController['spawner'][wi]['moveType'][i]
            newEnemy['moveType'] = moveType

            # Vitesse
            speed = spawnController['spawner'][wi]['speed'][i]
            newEnemy['ship']['entity']['speed'] = speed

            #Position
            position = [spawnController['spawner'][wi]['x'][i],    spawnController['spawner'][wi]['y'][i]]
            newEnemy['ship']['entity']['position'] = position

            
                                    
            addWeaponToShip(getPlayerShip(newEnemy), PROJECTILE_BLUEPRINTS['blasterShot'], [w//2, h] ,'EnemyTeam', ENEMY_WEAPON_COOLDOWN)
            startShipShooting(getEnemyShip(newEnemy))

            addEntityAnimation(getShipEntity(getEnemyShip(newEnemy)), 'Skin_1', spawnController['spawner'][wi]['skin'][i], 1)      # choix du skin
            print(newEnemy)
            addEnemy(newEnemy)  

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

    
Player1 = createPlayer(createShip(createEntity(PLAYER1_SHIP_SIZE[X], PLAYER1_SHIP_SIZE[Y], 
                                               PLAYER1_SHIP_START_POS[X], PLAYER1_SHIP_START_POS[Y], 
                                               PLAYER1_SHIP_SPEED), False))
addWeaponToShip(getPlayerShip(Player1), PROJECTILE_BLUEPRINTS['blasterShot'], [PLAYER1_SHIP_SIZE[X]//2, 0], 'PlayerTeam', PLAYER1_WEAPON_COOLDOWN)
addEntityAnimation(getShipEntity(getPlayerShip(Player1)), 'Skin_Base', 'player1_base', 0.4)

leftInput = 0
rightInput = 0
upInput = 0
downInput = 0

def inputManager(events):
    global Player1, finished, playing, projectiles_axe, leftInput, rightInput, upInput, downInput

    for event in events:

        if event.type == pygame.QUIT:
            finished = True
            playing = False

        if event.type == pygame.KEYDOWN :
            #Player 1
            if event.key == pygame.K_q or event.key == pygame.K_LEFT:
                leftInput -= 1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                rightInput = 1
            if event.key == pygame.K_z or event.key == pygame.K_UP:
                upInput = -1
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                downInput = 1
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
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_LEFT:
                leftInput = 0
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                rightInput = 0
            if event.key == pygame.K_z or event.key == pygame.K_UP:
                upInput = 0
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                downInput = 0
            if event.key == pygame.K_SPACE :
                inputPlayerStopShoot(Player1)

    inputPlayerHor(Player1, leftInput + rightInput)
    inputPlayerVer(Player1, upInput + downInput)

#--- BACKGROUND ---#
# Background
BGx = 0
BGy = [-7*WINDOW_SIZE[1], -15*WINDOW_SIZE[1]]

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
        BGy[0] = -15*WINDOW_SIZE[1]
    if(BGy[1]>WINDOW_SIZE[1]):
        BGy[1] = -15*WINDOW_SIZE[1]

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
    initializeSpawners(niveau_1
    )
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
            resetPlayerInput(Player1)

    window.fill(BLACK)
    displayMenu()
    pygame.display.flip()
    
    while playing:

        current_time = pygame.time.get_ticks()

        inputManager(pygame.event.get())

        # erase
        window.fill(MIDNIGHT_BLUE)
        BG()
      
        
        
        # actions
        control(current_time)
        moveProjectiles(Projectiles['EnemyTeam'])
        moveProjectiles(Projectiles['PlayerTeam'])
        destroyProjOutBound(Projectiles['EnemyTeam'])
        destroyProjOutBound(Projectiles['PlayerTeam'])

        shipShoot(getPlayerShip(Player1), current_time)
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
        displayProjectiles(Projectiles['EnemyTeam'], current_time)
        displayProjectiles(Projectiles['PlayerTeam'], current_time)
        displayProjectiles(Projectiles['toDestroy'], current_time)
        updateProjectilesToDestroy()
        displayScore()
        displayLives()
        pygame.display.flip()

        temps.tick(60)

pygame.display.quit()
pygame.quit()




