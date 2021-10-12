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
tirs = []

#Ennemis 
TAILLE_ENNEMI = 40
ennemis = []

#Cooldowns
cooldown_tir = 200 # Millisecondes entre chaque tir
temps_dernier_tir = 0

# --- Pour que ce soit plus lisible
X = 0; Y = 1


pygame.init()
fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)
fenetre.fill(NOIR)

#--- Définition entite

def creer_entite(largeur, hauteur, x=0, y=0, vx=0, vy=0):
    return {
        'position': [x, y],
        'vitesse': [vx, vy],
        'taille': [largeur, hauteur]
    }

def position(entite):
    return entite['position']

def vitesse(entite):
    return entite['vitesse']

def taille(entite):
    return entite['taille']

def modifier_vitesse(entite, vecteur):
    entite['vitesse'][X] = vecteur[X]
    entite['vitesse'][Y] = vecteur[Y]

def modifier_position(entite, coordonnees):
    entite['position'][X] = coordonnees[X]
    entite['position'][Y] = coordonnees[Y]

#Definition fonctions

#--- Collisions

# Return True si collision entre les deux entites, False sinon
def collision_entite(entite1, entite2):
    rect1 = pygame.Rect(position(entite1), taille(entite1))
    rect2 = pygame.Rect(position(entite2), taille(entite2))
    return pygame.Rect.colliderect(rect1, rect2)

def collision_tirs_joueurs_ennemis():
    index_tirs_a_supprimer = []
    index_ennemis_a_supprimer = []

    for i in range(len(tirs)):
        for j in range(len(ennemis)):
            if collision_entite(tirs[i], ennemis[j]):
                index_tirs_a_supprimer.append(i)
                index_ennemis_a_supprimer.append(j)
                break # Si une collision est détectée, on ne considère plus les autres collisions éventuelles du tir actuel

    # Suppression des tirs et ennemis qui ont générés des collisions

    for i in range(len(index_tirs_a_supprimer)):
        detruire_tir(index_tirs_a_supprimer[i] - i) #index_tirs_a_supprimer[i] >= i car index_tirs_a_supprimer est en ordre croissant

    for i in range(len(index_ennemis_a_supprimer)):
        detruire_ennemi(index_ennemis_a_supprimer[i] - i) #index_ennemis_a_supprimer[i] >= i car index_ennemis_a_supprimer est en ordre croissant

#--- Joueur

def afficher_joueur():
    pygame.draw.circle(fenetre, BLANC, (position(joueur)[X] + taille(joueur)[X]//2, position(joueur)[Y] + taille(joueur)[Y]//2), SHIP_TAILLE)


#Tirs joueurs

def tirer():
    global cooldown_tir, temps_dernier_tir
    if((tir == True) and (pygame.time.get_ticks() - temps_dernier_tir >= cooldown_tir)):

        temps_dernier_tir = pygame.time.get_ticks()

        position_joueur = position(joueur)

        nouveau_tir = creer_entite(TIR_TAILLE*2, TIR_TAILLE*2)
        modifier_position(nouveau_tir, (position_joueur[X] + taille(joueur)[X]//2, position_joueur[Y] + taille(joueur)[Y]//2))
        modifier_vitesse(nouveau_tir, (0, TIR_VITESSE))
        tirs.append(nouveau_tir)

def afficher_tir():
    for i in range(len(tirs)):
        pygame.draw.circle(fenetre, BLANC, position(tirs[i]), TIR_TAILLE)

def effacer_tir():
    for i in range(len(tirs)):
        pygame.draw.circle(fenetre, NOIR, position(tirs[i]), TIR_TAILLE)

def deplacer_tir():
    for i in range(len(tirs)):
        deplacer(tirs[i])

def detruire_tir_hors_ecran():
    index_tirs_a_supprimer = []
    for i in range(len(tirs)):
        if position(tirs[i])[Y] < 0:
            index_tirs_a_supprimer.append(i)
    
    for i in range(len(index_tirs_a_supprimer)):
        detruire_tir(index_tirs_a_supprimer[i] - i)

def detruire_tir(index):
    tirs.pop(index)


#deplacement       

# --- Retourne la distance parcourue sur une dimension pendant un tour de boucle
def deplacement_1d(vitesse):
    return vitesse * temps.get_time()

# --- Retourne une liste contenant la distance parcourue pour chaque dimension
def deplacement_2d(vitesse): #must be list
       return [deplacement_1d(vitesse[X]), deplacement_1d(vitesse[Y])]

# --- Fonctions de deplacement utilisant les entites

def translation(entite, mouvement):
    entite['position'][X] += mouvement[X]
    entite['position'][Y] += mouvement[Y]

def deplacer(entite):
    translation(entite, deplacement_2d(vitesse(entite)) )

#ennemis

def creer_ennemi(largeur, hauteur, x, y):
    ennemis.append( creer_entite(largeur, hauteur, x, y) )

def afficher_ennemis():
    for i in range(len(ennemis)):
        pygame.draw.circle(fenetre, BLANC, (position(ennemis[i])[X] + taille(ennemis[i])[X]//2, position(ennemis[i])[Y] + taille(ennemis[i])[Y]//2), TAILLE_ENNEMI)

def detruire_ennemi(index):
    ennemis.pop(index)



# ----- Fin définitions fonctions

temps = pygame.time.Clock()

joueur = creer_entite(SHIP_TAILLE*2, SHIP_TAILLE*2, ship_position[0], ship_position[1])

for i in range(1, 8):
    creer_ennemi(TAILLE_ENNEMI*2, TAILLE_ENNEMI*2, 200*i, 100 )

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

    modifier_vitesse(joueur, (SHIP_VITESSE * -int(gauche)+int(droite), 0) )

    #effacer
    fenetre.fill(NOIR)
    
    #actions
        
    deplacer(joueur)
    deplacer_tir()
    detruire_tir_hors_ecran()
    tirer()

    collision_tirs_joueurs_ennemis()
    
    #dessiner
    afficher_ennemis()
    afficher_joueur()
    afficher_tir()
    pygame.display.flip()

    temps.tick(60)

pygame.display.quit()
pygame.quit()
