# Python---Shoot-Em-Up



SQUELETTE


ennemi_temps_apparition = []          // liste des cdwitch: case ... break , etcwitch: case ... break , etc  

ennemi_index_apparition  = 0          // augmente quand temps[ennemi_index_apparition] ≤ 0. 

                                                        // type d'ennemis, String

vitesse_ennemi = [][]                        // ensemble de vecteur (x,y) 

ennemi_vie = []                                 // liste de la santé des ennemis 

ennemi_position = [][]                       // append() à chaque fois que le cd ≤ 0

vague = [boolean, boolean, boolean, boolean, boolean, boolean, boolean]

 

                                     ennemi == array vide 

                                          Alors

                                    index_vague++

              

bouger_ennemi(index)

type = ennemis[index]

switch: case type ... break, etc.

nettoyer_ennemi(index_ennemi)

Si vie ≤ 0 || ennemi en dessous de l'écran

⇒ sortir l'index de toutes les arrays ennemis

                  et ennemi_index_apparition -= 1    //évite les erreurs d'index et d'array out of range

apparition_ennemi()

Si cd [index] ≤ 0, spawn[index_apparition++]

afficher_ennemi(type_ennemi)

switch: case ... break; etc

// ennemis en forme de rectangle dans un premier temps. y a moyen de styliser ça, mais la hitbox doit rester claire.

bouger_tir ( type_tir, position)

switch: case... break, etc;

collision_tir (position_1, [largeur_1, hauteur_1], position_2, [largeur_1, hauteur_2]) 

si un des 4 points du mobile 1 se trouve entre le xmin et xmax et entre le ymin et ymax, 

return true.

//Collision entre rectangle uniquement

gestion_vague(index_vague)

si vague[index_vague] == true

⇒ false &&

renouveler_array(index_vague)

renouveler_array(index_vague)

switch case break

remplir les array comme on le  veut et remettre l'index des ennemis à 0.

bool droite, gauche, haut, bas, espace

gestion_touche_joueur()

Si touche enfoncee, bool = true,

si touche relachee, bool = false;

dessiner_background()

repeindre tout en noire. Bonus, fond étoilé?

Type d'ennemi:

diagonale_gauche

diagonale_droite

Colonne Gauche, Milieu, Droite,

Ligne_gauche (ennemis viennent de gauche, quand bord atteint, TP en bas à gauche)

Ligne_droite

dans un premier ne mettre que les tirs joueurs, pas les ennemis

ennemi[]

ennemi_position = [][]

ennemi[]

ennemi_position = [][]

ennemi[]

ennemi_position = [][]

ennemi[]

ennemi_position = [][]

ennemi[]
