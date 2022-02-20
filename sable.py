from tkinter import Tk, Canvas, PhotoImage, Button
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo
from random import randint

#   On declare les variables qui seront accessibles par les fonctions
global HAUT, LARGE, ZOOM, root, img, couleurs, grains

def importer():  #On lit un fichier avec des charactere a 8 oct
    fichier = askopenfilename()#, filetypes=[['*']])
    
    if not fichier:
        showinfo(title="Erreur", message="Aucun fichier")
        return
    
    with open(fichier, 'r') as fp:
        #   Ici on enleve les espaces en trop au bout au cas ou, les , en trop, les \n deviennes des ','
        #   et on cree un liste en coupant le texte en ','
        nombres = fp.read().replace('\n',',').replace(',,',',').strip(' ').strip(',').split(',')

        #   Si il y a trop ou pas assez de nombres on stope
        if len(nombres) != HAUT*LARGE:
            showinfo(title="Erreur", message=f"Il y a {len(nombres)} nombres, alors qu'il en faut {HAUT*LARGE}")
            return
        
        #   Mettre les characters dans grains
        for y in range(HAUT):
            for x in range(LARGE):
                grains[y][x] = int(nombres[y*LARGE + x])

    afficher()

def exporter(): #On ecrit dans un fichier
    fichier = asksaveasfilename()#, filetypes=[['*']])
    
    if not fichier:
        showinfo(title="Erreur", message="Aucun fichier")
        return

    try:
        texte = ','.join([str(grains[y][x]) for y in range(HAUT) for x in range(LARGE)])
    except:
        breakpoint()

    with open(fichier, 'w') as fp:
        fp.write(texte)

#   Affiche tout les grains dans chaque pixel de l'image
def afficher():
    for y in range(HAUT):
        for x in range(LARGE):
            nb = grains[y][x]
            couleur = couleurs[nb if nb < 4 else 4] #ce qui veut dire que si nb>4 alors la couleur[4] sera mise, en dessous ca change

            #   Zoom *2 ca veut dire dessiner le pixel sur *2 plus de lignes et de colones. On fait un carree en fait de ZOOM taille
            for zoomx in range(ZOOM):
                for zoomy in range(ZOOM):
                    img.put(couleur, (x*ZOOM + zoomx, y*ZOOM + zoomy))  #on met le pixel (x,y) a la couleur [nb if nb < 4 else 4]

#   Fonction qui met a jour le plateau et l'affiche dans l'image
def update():
    #   Si aucun instable on updta e rien
    if not any(grains[y][x] >= 4 for y in range(HAUT) for x in range(LARGE)):
        return
    
    #   On copie temporairement les informations, sinon dans la mise a jour elles seront effacees par l'ajout ou le retrait de grains
    tmp = [[grains[y][x] for x in range(LARGE)] for y in range(HAUT)]

    #   On remet la grille a 0
    for y in range(HAUT):
        for x in range(LARGE):
            grains[y][x] = 0

    #   Mise a jour selon les regles
    for y in range(HAUT):
        for x in range(LARGE):
            if tmp[y][x] >= 4:
                #   On enleve 4 au tat trop haut (+= car des actions precedents peuvent lui avoire donnees qlq grains)
                grains[y][x] += (tmp[y][x] - 4)

                #A gauche
                if x > 0: grains[y][x-1] += 1
                #A droite
                if x < LARGE-1: grains[y][x+1] += 1
                #En haut
                if y > 0: grains[y-1][x] += 1
                #En bas
                if y < HAUT-1: grains[y+1][x] += 1
            else:
                # On ne met la valeur stable d'avant (les pixels a cote peuvent avoire deja ajouter des grains, donc '+=')
                grains[y][x] += tmp[y][x]
    afficher()
    del tmp

ZOOM = 50
HAUT, LARGE = 10, 10

#   Couleurs selon le nombre de grains
couleurs = [    #code couleur RGB en hexadecimale
    "#ffffff",  #0 grain c'est blanc
    "#48cae4",  #1 grains c'est jaunatre
    "#0077b6",  #2 grains c'est orange
    "#03045e",  #3 grains c'est rouge
    "#000000",  #4 grains ou plus c'est noir
]

######################################
################ Main ################
######################################

#   Fenetre
root = Tk()

#   La ou on va .pack() une image
canvas = Canvas(root, width=ZOOM*LARGE, height=ZOOM*HAUT, bg="#000000")
canvas.pack()

#   Sur l'image, grace aux pixels nous aurons les tats de sables
img = PhotoImage(width=ZOOM*LARGE, height=ZOOM*HAUT)
canvas.create_image((ZOOM*LARGE/2, ZOOM*HAUT/2), image=img, state="normal")

#   On crée un liste ou les nombres de grains seront stoquées (initialisation aleatoire)
#   On importe n'importe quel config ici
grains = [[randint(0, 5) for _ in range(LARGE)] for _ in range(HAUT)]

#   On affiche direct dans l'image
afficher()

#   On cree un bouton qui genere une nouvelle mise a jour
Button(root, text='Importer', command=importer).pack()
Button(root, text='Exporter', command=exporter).pack()
Button(root, text='Mettre a jour', command=update).pack()

#   On lance le tout
root.mainloop()
