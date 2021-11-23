TO DO LIST

Un menu avec choix du niveau.
Comme ça je peux créer différentes vagues dans différentes sauvegardes json et donc gg wp

Peut-être tirer size [] du dictionnaire des images.
Laisser python se charger de calculer la taille selon le fichier automatiquement par appel d'une fonction?
C'est plus facile de changer la taille avec un facteur scale associé aux ennemis des vagues
Edit: mauvaise idée. C'est mieux que je puisse corriger manuellement la taille des skins

Différents types de tir? :
Unique, double diagonale, laser? 

Et différents timing de tir
ex: munition = ..., munitionMax = x; cdEntreTir = ...; cdRechargement = ...;
(pour des rafales de x tirs)

ajout hitboxSize [] dans les entités ou dans les ennemis
Ajout d'une fonction montrer hitbox pour faciliter le développement


Bug de tir avec les skns, ce n'est pas centré.
Pourtant à part, les skins sont tous centrés et croppés du coup c'est bizare 

J'ai essayé ça 

    if Ship['isShooting']:
    
        print("\n\n Le vaisseau est : \n")
        print(Ship['entity']['currImage'])
        
        
        w = Ship['entity']['currImage'].get_width()
        h = Ship['entity']['currImage'].get_height()
        
        pos = [w/2,h]
        pos[0] += getPos(getShipEntity(Ship))[0]
        pos[1] += getPos(getShipEntity(Ship))[1]
        
        weaponShoot(Ship['weapons'][Ship['weaponInUse']], getPos(getShipEntity(Ship)), time)
      
Mais nope

