import pygame

# --- To make code more readable
X = 0; Y = 1

# window size
WINDOW_SIZE = [1600, 900]

# definition of colors
BLACK  = (  0, 0, 0); WHITE = (  255, 255, 255)

# booleans
finished   = False; 
left = False; right = False; shooting = False

# Ship
SHIP_SIZE  = 40; SHIP_SPEED = 10
SHIP_OFFSET = 100
SHIP_START_POS = [WINDOW_SIZE[0]//2, WINDOW_SIZE[1]-SHIP_OFFSET]

#Projectiles
PROJECTILE_SPEED   = 20
PROJECTILE_SIZE    = 3
projectiles = []

#Ennemies
ENNEMY_SIZE = 40
ennemies = []

#Cooldowns
COOLDOWN_SHOOT = 200 # Milliseconds between each fire
TIME_LAST_SHOT = 0

#Spawner
spawner = []

#spawnController
spawnController = 0
oldTime = 0
deltaTime = 0
  #Pour le futur


pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
window.fill(BLACK)



#--- Definition entity

def createSpawnController():
    return{
        'spawnIndex' : 0,
        'waveIndex'  : 0,
        'spawner' : [],
        'ennemies': [],
        'timeElapsed': 0
    } 
    

def createSpawner(w, t):
    return{
        'type'   : w,
        'timer'  : t
    }


def createEntity(width, height, x=0, y=0, vx=0, vy=0):
    return {
        'position': [x, y],
        'direction': [0,0], # normalized
        'speed': 0,
        'size': [width, height],
        'controller' : None # ref to function controlling direction and speed of entity
    }

def getPos(entity):
    return entity['position']

def getDirection(entity):
    return entity['direction']

def getSpeed(entity):
    return entity['speed']

def getSize(entity):
    return entity['size']

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

#Definition functions

#--- Collisions

# Return True if collision occurs, False otherway
def collision_entite(entite1, entite2):
    rect1 = pygame.Rect(getPos(entite1), getSize(entite1))
    rect2 = pygame.Rect(getPos(entite2), getSize(entite2))
    return pygame.Rect.colliderect(rect1, rect2)

def collisionProjectilePlayersEnnemies():
    indexProjectileToDestroy = []
    indexEnnemiesToDestroy = []

    for i in range(len(projectiles)):
        hasCollided = False
        j = 0
        while((j < len(ennemies)) and (not hasCollided)): # stop the search if the projectile has already collided
            if collision_entite(projectiles[i], ennemies[j]):
                indexProjectileToDestroy.append(i)
                indexEnnemiesToDestroy.append(j)
                hasCollided = True
            j = j + 1

    # Removing projectiles and ennemies that has collided

    for i in range(len(indexProjectileToDestroy)):
        projectiles.pop(indexProjectileToDestroy[i] - i) #indexProjectileToDestroy[i] >= i because indexProjectileToDestroy is in increasing order

    for i in range(len(indexEnnemiesToDestroy)):
        destroyEnemy(indexEnnemiesToDestroy[i] - i) #indexEnnemiesToDestroy[i] >= i because indexEnnemiesToDestroy is in increasing order

#--- Player

def displayPlayer():
    pygame.draw.circle(window, WHITE, (getPos(player)[X] + getSize(player)[X]//2, getPos(player)[Y] + getSize(player)[Y]//2), SHIP_SIZE)


# Player's projectiles

def shoot():
    global COOLDOWN_SHOOT, TIME_LAST_SHOT
    if((shooting == True) and (pygame.time.get_ticks() - TIME_LAST_SHOT >= COOLDOWN_SHOOT)):

        TIME_LAST_SHOT = pygame.time.get_ticks()

        playerPos = getPos(player)

        newProjectile = createEntity(PROJECTILE_SIZE*2, PROJECTILE_SIZE*2)
        setPosition(newProjectile, (playerPos[X] + getSize(player)[X]//2, playerPos[Y] + getSize(player)[Y]//2))
        setSpeed(newProjectile, PROJECTILE_SPEED)
        setDirection(newProjectile, 0, -1)
        projectiles.append(newProjectile)

def displayProjectile():
    for i in range(len(projectiles)):
        pygame.draw.circle(window, WHITE, getPos(projectiles[i]), PROJECTILE_SIZE)

def deplacer_tir():
    for projectile in projectiles:
        move(projectile)

def destroyProjOutBound():
    for projectile in range(len(projectiles)-1):
        if getPos(projectiles[projectile])[Y] < 0:
            projectiles.pop(projectile)

# movement

def move(entity):
    entity['position'][X] += entity['direction'][X] * entity['speed']
    entity['position'][Y] += entity['direction'][Y] * entity['speed']

# ennemies

def createEnemy(width, height, x, y):
    ennemies.append( createEntity(width, height, x, y) )

def displayEnnemy():
    for ennemy in ennemies:
        pygame.draw.circle(window, WHITE, (getPos(ennemy)[X] + getSize(ennemy)[X]//2, getPos(ennemy)[Y] + getSize(ennemy)[Y]//2), ENNEMY_SIZE)

def destroyEnemy(index):
    ennemies.pop(index)



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
            createEnemy(50, 50, 50+100*spawnController['spawnIndex'], 300)
            spawnController['timeElapsed'] = 0
            spawnController['spawnIndex'] += 1
    
        if ( ( spawnController['spawnIndex'] >= len(spawnController['spawner'][0]['timer'])-1  ) ):
            spawnController['spawner'].pop()
            spawnController['spawnIndex'] = 0
            
    deltaTime = pygame.time.get_ticks()-oldTime
    oldTime   = pygame.time.get_ticks()
    spawnController['timeElapsed'] +=  deltaTime
    
    return

# ----- End function definition

temps = pygame.time.Clock()

player = createEntity(SHIP_SIZE*2, SHIP_SIZE*2, SHIP_START_POS[0], SHIP_START_POS[1])
setSpeed(player, SHIP_SPEED)

for i in range(1, 8):
    createEnemy(ENNEMY_SIZE*2, ENNEMY_SIZE*2, 200*i, 100 )

while not finished:

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
               finished = True

        if evenement.type    == pygame.KEYDOWN :
            if evenement.key == pygame.K_LEFT :
               left = True
            if evenement.key == pygame.K_RIGHT :
               right = True
            if evenement.key == pygame.K_SPACE :
               shooting = True

        if evenement.type == pygame.KEYUP :
            if evenement.key == pygame.K_LEFT :
               left = False
            if evenement.key == pygame.K_RIGHT :
               right = False
            if evenement.key == pygame.K_SPACE :
               shooting = False

    setDirection(player, (-int(left)+int(right)), 0)

    # erase
    window.fill(BLACK)
    
    # actions
    control()
    move(player)
    deplacer_tir()
    destroyProjOutBound()
    shoot()

    collisionProjectilePlayersEnnemies()
    
    # display
    displayEnnemy()
    displayPlayer()
    displayProjectile()
    pygame.display.flip()

    temps.tick(60)

pygame.display.quit()
pygame.quit()
