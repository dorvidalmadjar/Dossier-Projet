__author__ = 'Doryan Valentin Thomas'

from tkinter import *
from tkinter import ttk
from os import *
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageGrab

VISAGES = 0
BOUCHES = 1
YEUX = 2
MOUSTACHES = 3
NEZ = 4
CHEVEUX = 5
MAX_VISAGE = 6

LARG_CANVAS = 720
HAUT_CANVAS = 1000

def charger_images(num : int):
    global Catalogue, listes_image, nom_parties
    listewidget = Listbox(Catalogue)
    listewidget.bind('<<ListboxSelect>>', lambda event : change_selection(event, listes_image[num]))
    repertoire = "Images/" + nom_parties[num]
    liste_fichier = listdir(repertoire)
    for nomfichier in liste_fichier:
        nomcomplet = repertoire + "/" + nomfichier
        photo = PhotoImage(file = nomcomplet)
        listes_image[num].append(photo)
        nouveau_nom = '.'.join(nomfichier.split('.')[:-1])  #On retire l'extension dans le nom du fichier
        nouveau_nom = str.capitalize(nouveau_nom)
        listewidget.insert(num, nouveau_nom)
    Catalogue.add(listewidget, text = nom_parties[num])

def change_catalogue(event):
    global catalogue_choisi
    catalogue_choisi = event.widget.index("current")

def change_selection(event, l : list):
    global catalogue_choisi, objets_canvas, canvas_visage
    nv_image = l[event.widget.curselection()[0]]
    canvas_visage.itemconfig(objets_canvas[catalogue_choisi], image = nv_image)

coord_obj_mobile = [[], [], [], [], [], []]
coord_clic_souris = 0
object_scale = 1.0

def start_move_visage(event):
    global coord_obj_mobile, canvas_visage, objets_canvas, catalogue_choisi, coord_clic_souris
    coord_clic_souris = (event.x, event.y)
    coord_obj_mobile[catalogue_choisi].append(canvas_visage.coords(objets_canvas[catalogue_choisi]))
    canvas_visage.focus_set()

def move_visage(event):
    global coord_obj_mobile, canvas_visage, objets_canvas, catalogue_choisi, coord_clic_souris
    offset = (event.x - coord_clic_souris[0], event.y - coord_clic_souris[1])
    coord = coord_obj_mobile[catalogue_choisi][-1]
    canvas_visage.coords(objets_canvas[catalogue_choisi],coord[0] + offset[0],coord[1] + offset[1])

def reset_visage(event):
    global canvas_visage, objets_canvas, catalogue_choisi
    canvas_visage.coords(objets_canvas[catalogue_choisi],0 ,0)

def annule_deplacement(event):
    global coord_obj_mobile, canvas_visage, objets_canvas, catalogue_choisi
    if len(coord_obj_mobile[catalogue_choisi]) > 0:
        coord = coord_obj_mobile[catalogue_choisi].pop()
        canvas_visage.coords(objets_canvas[catalogue_choisi],coord[0], coord[1])

def reset_scale(event):
    global canvas_visage, objets_canvas, catalogue_choisi
    canvas_visage.scale(objets_canvas[catalogue_choisi],0, 0, 1, 1)

def scale_visage(event):
    global object_scale
    if event.num == 5 or event.delta == -120:
        object_scale -= .01
    if event.num == 4 or event.delta == 120:
        object_scale += .01
    object_scale = max(min(object_scale, 5.0), 0.1)
    canvas_visage.scale(objets_canvas[catalogue_choisi],0, 0, object_scale, object_scale)
    print(object_scale)

def apropos():
    tkinter.messagebox.showinfo("A propos","sincére")

def commandes():
    tkinter.messagebox.showinfo("Commandes","sincére")

def sauver_portrait():
    global canvas_visage
    filename = tkinter.filedialog.asksaveasfilename(title="Enregistrer le Portrait",filetypes=[('Jpeg files','.jpeg'),('all files','.*')])
    x = canvas_visage.winfo_rootx()
    y = canvas_visage.winfo_rooty()
    w = canvas_visage.winfo_width()
    h = canvas_visage.winfo_height()
    image=ImageGrab.grab((x+2, y+2, x+w-2, y+h-2))
    image.save(filename)

def nouveau_portrait():
    print("soupe")

def portrait_random():
    print("spaghetti")

fenetre = Tk()
fenetre.title('Outil de création de visage type portrait robot')
fenetre['bg']='white'
fenetre.resizable(FALSE, FALSE)

#Création de l'interface
FrameCatalogue = Frame(fenetre, borderwidth=2, relief=GROOVE, width = 250, height = HAUT_CANVAS)
FrameCatalogue.pack(side=LEFT, padx=2, pady=2)
Catalogue = ttk.Notebook(FrameCatalogue)
Catalogue.bind_all("<<NotebookTabChanged>>", change_catalogue)
FramePortrait = Frame(fenetre, borderwidth=2, relief = SUNKEN, width = LARG_CANVAS, height = HAUT_CANVAS)
FramePortrait.pack(side=RIGHT, padx=2, pady=2)
canvas_visage = Canvas(FramePortrait, width =LARG_CANVAS, height =HAUT_CANVAS)
canvas_visage.pack(side=LEFT, padx = 0, pady = 0)
canvas_visage.bind('<Button-1>', start_move_visage)
canvas_visage.bind('<B1-Motion>', move_visage)
canvas_visage.bind('<r>', reset_visage)
canvas_visage.bind('<Button-3>', annule_deplacement)
'''
canvas_visage.bind('<Button-2>', reset_scale)
canvas_visage.bind('<MouseWheel>', scale_visage)
'''

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
Catalogue.pack(side = LEFT, fill = Y)

# Création d'un widget Menu
menubar = Menu(fenetre)

menufichier = Menu(menubar,tearoff=0)
menufichier.add_command(label="Nouveau Portrait",command=nouveau_portrait)
menufichier.add_command(label="Portrait Aléatoire",command=portrait_random)
menufichier.add_command(label="Enregistrer le Portrait",command=sauver_portrait)
menufichier.add_command(label="Quitter",command=fenetre.destroy)
menubar.add_cascade(label="Fichier", menu=menufichier)

menuaide = Menu(menubar,tearoff=0)
menuaide.add_command(label="Commandes",command=commandes)
menuaide.add_command(label="A propos",command=apropos)
menubar.add_cascade(label="Aide", menu=menuaide)

# Affichage du menu
fenetre.config(menu=menubar)

#Boucle Principale
fenetre.mainloop()


    

