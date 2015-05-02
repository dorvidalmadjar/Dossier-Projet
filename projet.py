__author__ = 'Doryan Valentin Thomas'

from tkinter import *
from tkinter import ttk
from os import *
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageGrab

#Variables globales
VISAGES = 0
BOUCHES = 1
YEUX = 2
MOUSTACHES = 3
NEZ = 4
CHEVEUX = 5
MAX_VISAGE = 6

LARG_CANVAS = 720
HAUT_CANVAS = 1000

#Definition des fonctions
def charger_images(num : int):
    """
    Cette fonction va charger les images dans le notebook ainsi que donner un nom à chaque catalogue et chaque images.
    :param num: index de chaque liste d'éléments du visage dans la liste regroupant tout les éléments
    """
    global Catalogue, listes_image, nom_parties
    listewidget = Listbox(Catalogue)
    listewidget.bind('<<ListboxSelect>>', lambda event : change_selection(event, listes_image[num]))
    repertoire = "Images/" + nom_parties[num]                   #Emplacement ds images dans le disque dur
    liste_fichier = listdir(repertoire)                         #Liste contenant les noms de tout les fichiers dans repertoire
    for nomfichier in liste_fichier:
        nomcomplet = repertoire + "/" + nomfichier
        photo = PhotoImage(file = nomcomplet)
        listes_image[num].append(photo)
        nouveau_nom = '.'.join(nomfichier.split('.')[:-1])      #On retire l'extension dans le nom du fichier
        nouveau_nom = str.capitalize(nouveau_nom)
        listewidget.insert(num, nouveau_nom)                    #Insére le nouveau_nom dans la liste listewidget à l'index num
    Catalogue.add(listewidget, text = nom_parties[num])

def change_catalogue(event):
    """
    Cette fonction va permettre de mettre dans une variable l'index du catalogue séléctionné
    """
    global catalogue_choisi
    catalogue_choisi = event.widget.index("current")

def change_selection(event, l : list):
    """
    Cette fonction va permettre de changer l'image à afficher en fonction de ce qui est séléctionné dans le notebook
    :param l: liste dans laquelle se trouve les images
    """
    global catalogue_choisi, objets_canvas, canvas_visage
    nv_image = l[event.widget.curselection()[0]]                                    #On affecte à la variable nv_image celle qui est séléctionnée dans le notebook
    canvas_visage.itemconfig(objets_canvas[catalogue_choisi], image = nv_image)     #On change l'image à afficher sur le canvas

#Variables nécéssaires pour les bind
coord_obj_mobile = [[], [], [], [], [], []]     #Liste des coordonnées de chaques objet
coord_clic_souris = ()

def start_move_visage(event):
    """
    Cette fonction va enregistrer les coordonnées du clic de la souris
    """
    global coord_obj_mobile, canvas_visage, objets_canvas, catalogue_choisi, coord_clic_souris
    coord_clic_souris = (event.x, event.y)
    coord_obj_mobile[catalogue_choisi].append(canvas_visage.coords(objets_canvas[catalogue_choisi]))    #Insére les coordonnées de l'objet séléctionné dans la liste des coordonnées (si on change le type de l'objet, les coordonnées ne changent pas)
    canvas_visage.focus_set()                                                                           #Permet de désigner le canvas_visage comme celui qui recevra les event lorsqu'il est cliqué

def move_visage(event):
    """
    Cette fonction va changer les coordonnées de l'objet séléctionné en fonction du mouvement de la souris
    """
    global coord_obj_mobile, canvas_visage, objets_canvas, catalogue_choisi, coord_clic_souris
    offset = (event.x - coord_clic_souris[0], event.y - coord_clic_souris[1])                           #Tuple contenant la différence entre les coordonnées initiales et aprés le mouvement de la souris
    coord = coord_obj_mobile[catalogue_choisi][-1]                                                      #Récupére les derniéres coordonnées sauvées
    canvas_visage.coords(objets_canvas[catalogue_choisi],coord[0] + offset[0],coord[1] + offset[1])     #Changement des coordonnées de l'objet afin de le mettre en mouvement par rapport au mouvement de la souris

def reset_visage(event):
    """
    Cette fonction va remettre l'objet séléctionné à sa position de départ
    """
    global canvas_visage, objets_canvas, catalogue_choisi
    canvas_visage.coords(objets_canvas[catalogue_choisi],0 ,0) #Changement des coordonnées de l'objet à celle du départ

def annule_deplacement(event):
    """
    Cette fonction va annuler le déplacement précédent
    """
    global coord_obj_mobile, canvas_visage, objets_canvas, catalogue_choisi
    if len(coord_obj_mobile[catalogue_choisi]) > 0:                                 #Les actions suivantes ne s'effectuent que si il y a eu un ou plusieurs déplacements
        coord = coord_obj_mobile[catalogue_choisi].pop()                            #.pop() enléve et retroune le dernier élément de la liste
        canvas_visage.coords(objets_canvas[catalogue_choisi],coord[0], coord[1])    #Changement des coordonnées pour remettre à la position précédente


def apropos():
    """
    Cette fonction va simplement faire apparaitre une messagebox avec le texte suivant lorsque l'on clique sur la commande A propos
    """
    tkinter.messagebox.showinfo("A propos","Projet de fin d'année en Informatique & Sciences du Numérique\nAnnée 2014-2015, Lycée J.B.Corot (Savigny sur Orge)\nTerminale S2\nEnseignant : Mr Latreyte\n\nOutil de création de visages type portrait robot ver 1.0\n\nDeveloppé par :\n\tDoryan Vidal Madjar\n\tValentin Le Roux\n\tThomas Jarrion\n\nLangage & outils utilisés :\n\tPython 3.4\n\tPillow 2.8.1\n\tJetBrains PyCharm 3.4.1")

def sauver_portrait():
    """
    Cette fonction va permettre d'enregistrer le contenu de canvas_visage sous forme de jpg
    """
    global canvas_visage
    filename = tkinter.filedialog.asksaveasfilename(title="Enregistrer le Portrait",filetypes=[('Jpeg files','.jpeg'),('all files','.*')], defaultextension=".jpeg")
    #Incrémentation des coordonnées ainsi que la hauteur et largeur du canvas dans l'écran dans des variables
    x = canvas_visage.winfo_rootx()
    y = canvas_visage.winfo_rooty()
    w = canvas_visage.winfo_width()
    h = canvas_visage.winfo_height()
    image=ImageGrab.grab((x, y, x+w, y+h))
    image.save(filename)

def nouveau_portrait():
    """
    Cette fonction va permettre de réinitialiser le portrait
    """
    print("soupe")

def portrait_random():
    """
    Cette fonction va permettre de faire apparaitre un portrait aléatoire
    """
    print("spaghetti")

#Initialisation de la fenétre
fenetre = Tk()
fenetre.title('Outil de création de visage type portrait robot')
fenetre['bg']='white'
fenetre.resizable(FALSE, FALSE)                                     #Enléve la possibilité de changer la taille de la fenetre manuellement

#Création de l'interface
FrameCatalogue = Frame(fenetre, borderwidth=2, relief=GROOVE, width = 250, height = HAUT_CANVAS)
Catalogue = ttk.Notebook(FrameCatalogue)
Catalogue.bind_all("<<NotebookTabChanged>>", change_catalogue)
Label(FrameCatalogue,text="Parties du Visage").pack(padx=5,pady=2)
FramePortrait = Frame(fenetre, borderwidth=2, relief = SUNKEN, width = LARG_CANVAS, height = HAUT_CANVAS)
FramePortrait.pack(side=RIGHT, padx=2, pady=2)
canvas_visage = Canvas(FramePortrait, width =LARG_CANVAS, height =HAUT_CANVAS)
canvas_visage.pack(side=LEFT, padx = 0, pady = 0)
canvas_visage.bind('<Button-1>', start_move_visage)
canvas_visage.bind('<B1-Motion>', move_visage)
canvas_visage.bind('<r>', reset_visage)
canvas_visage.bind('<Button-3>', annule_deplacement)

#Chargement des images
#Création des objets de visage

catalogue_choisi = 0
listes_image = [[], [], [], [], [], []]
objets_canvas = [0, 0, 0, 0, 0, 0]
nom_parties = ["Visages", "Bouches", "Yeux", "Moustaches", "Nez", "Cheveux"]

for i in range(MAX_VISAGE):
    charger_images(i)
    objets_canvas[i] = canvas_visage.create_image(0,0,anchor=NW, image=listes_image[i][0])
    if (i == 0):
        canvas_visage.tag_lower(objets_canvas[i])
    else:
        canvas_visage.tag_raise(objets_canvas[i], objets_canvas[i-1])

#Positionnement du Catalogue
Catalogue.pack(side = TOP)
Label(FrameCatalogue,justify = LEFT,  text="Commandes:\n\n\tPour déplacer un objet, il faut qu'il soit séléctionné dans le Notebook\n\tet il suffit simplement de maintenir le clic gauche\n\tet de bouger la souris.\n\n\tSi vous souhaitez faire un retour en arriére dans le déplacement,\n\til suffit de faire un clic droit autantde fois\n\tque vous voulez de retour en arriére.\n\n\tSi vous souhaitez remettre un objet à sa position initiale,\n\til suffit d'appuyer sur la touche 'r' de votre clavier.").pack(side = TOP, padx=5, pady =10)
FrameCatalogue.pack(side=TOP, padx=2, pady=2, expand = True, fill = Y)


# Création d'un widget Menu
menubar = Menu(fenetre)

menufichier = Menu(menubar,tearoff=0)
menufichier.add_command(label="Nouveau Portrait",command=nouveau_portrait)
menufichier.add_command(label="Portrait Aléatoire",command=portrait_random)
menufichier.add_separator()
menufichier.add_command(label="Enregistrer le Portrait",command=sauver_portrait)
menufichier.add_separator()
menufichier.add_command(label="Quitter",command=fenetre.destroy)
menubar.add_cascade(label="Fichier", menu=menufichier)

menuaide = Menu(menubar,tearoff=0)
menuaide.add_command(label="A propos",command=apropos)
menubar.add_cascade(label="Aide", menu=menuaide)

# Affichage du menu
fenetre.config(menu=menubar)

#Boucle Principale
fenetre.mainloop()


    

