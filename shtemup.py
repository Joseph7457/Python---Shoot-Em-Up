import pygame

#taille écran
FENETRE_LARGEUR = 1600; FENETRE_HAUTEUR = 900

#valeur couleur
NOIR  = (  0, 0, 0); BLANC = (  255, 255, 255)

#booleans
fini   = False; 
gauche = False; droite = False; tir = False

#Ship
SHIP_TAILLE  = 40; SHIP_VITESSE = 1
ship_position = [FENETRE_LARGEUR//2, FENETRE_HAUTEUR-100]

#Tirs
TIR_VITESSE   = -1; TIR_TAILLE    = 3
tir_positions = []

#Cooldowns
cooldown_tir = 0; cooldown_max_tir = 60


pygame.init()
fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)
fenetre.fill(NOIR)

#Definition fonctions

#Tirs joueurs

def tirer():
    global cooldown_tir
    if((tir == True) and (cooldown_tir <= 0)):

       cooldown_tir = cooldown_max_tir
       tp = [ship_position[0], ship_position[1]]
       tir_positions.append(tp)
def afficher_tir():
    for i in range(len(tir_positions)):
        pygame.draw.circle(fenetre, BLANC, tir_positions[i], TIR_TAILLE)
def effacer_tir():
    for i in range(len(tir_positions)):
        pygame.draw.circle(fenetre, NOIR, tir_positions[i], TIR_TAILLE)
def deplacer_tir():
    for i in range(len(tir_positions)):
        tir_positions[i][1] += TIR_VITESSE

#deplacement       

def deplacer_joueur(vitesse):
       ship_position[0] += (-int(gauche)+int(droite)) * vitesse
       
def deplacer(position, vitesse): # both must be list
       return [position[0]+vitesse[0], position[1]+vitesse[1]]


while not fini:

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
               fini = True

        if evenement.type    == pygame.KEYDOWN :
            if evenement.key == pygame.K_LEFT :
               gauche = True
            if evenement.key == pygame.K_RIGHT :
               droite = True
            if evenement.key == pygame.K_SPACE :
               tir = True

        if evenement.type == pygame.KEYUP :
            if evenement.key == pygame.K_LEFT :
               gauche = False
            if evenement.key == pygame.K_RIGHT :
               droite = False
            if evenement.key == pygame.K_SPACE :
               tir = False




    #effacer
    pygame.draw.circle(fenetre, NOIR, ship_position, SHIP_TAILLE)
    effacer_tir()
    
    #actions
        
    deplacer_joueur(SHIP_VITESSE)
    deplacer_tir()
    tirer()
    cooldown_tir -= 1
    print(cooldown_tir)
    
    #dessiner
    pygame.draw.circle(fenetre, BLANC, ship_position, SHIP_TAILLE)
    afficher_tir()
    pygame.display.flip()



pygame.display.quit()
pygame.quit()
