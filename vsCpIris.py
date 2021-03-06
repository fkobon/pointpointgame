########################################################
#                  POINT POINT GAME
#
# Catégorie        : Stratégie
# Auteur           : Gabeta Soro (Alchimiste des codes)
# Pseudo           : @lChiMi5tE_d0t_toRr€nt
# Compagnie        : EnighmaLab
# Date de création : 26/06/2017
# Scène            : Player vs Iris-CP12
# Niveau de l'IA   : Elève CP1/CP2
#
########################################################

from tkinter import *
from random import randrange

from Environnement.player import Player
from Environnement.pivot import Pivot
from Environnement.terrain import Terrain

from IA.irisCpIA import IrisCpIA


begin = False

#Paramètre Joueur
P1 = Player('blue')
P2 = IrisCpIA('red')
current_p = P1

#Classe qui gère les pivot
Pivot = Pivot()

#Paramètre Terrain
space = 30
Theight = 540
Twidth = 630
r = 5

#Dictionnaire des points
point_dico = {}

#Crétation de la plateform de jeu
def create_plateform():

    global begin

    if(begin is False):
        d = 0
        info.configure(text = "Joueur Bleu  = " + str(P1.getScore()))
        info2.configure(text = "Joueur Rouge = " + str(P2.getScore()))

        terrain.horizontalLine()
        terrain.verticalLine()

        begin = True

#Marquer un point en faisant un carré
def makeCarre(x,y):

    if(Pivot.top_left(x,y,space,point_dico)):

        if(current_p == P1):
            P1.setScore()
        else:
            P2.setScore()

        can.create_rectangle(x-space, y-space, x, y, fill=current_p.getColor())

        info.configure(text = "Joueur Bleu  = " + str(P1.getScore()))
        info2.configure(text = "Joueur Rouge = " + str(P2.getScore()))

        chaine.configure(text = "Jolie point")

    if(Pivot.top_right(x,y,space,point_dico)):

        if(current_p == P1):
            P1.setScore()
        else:
            P2.setScore()

        can.create_rectangle(x, y-space, x+space, y, fill=current_p.getColor())

        info.configure(text = "Joueur Bleu  = " + str(P1.getScore()))
        info2.configure(text = "Joueur Rouge = " + str(P2.getScore()))

        chaine.configure(text = "Jolie point")

    if(Pivot.bottom_left(x,y,space,point_dico)):

        if(current_p == P1):
            P1.setScore()
        else:
            P2.setScore()

        can.create_rectangle(x, y+space, x-space, y, fill=current_p.getColor())

        info.configure(text = "Joueur Bleu  = " + str(P1.getScore()))
        info2.configure(text = "Joueur Rouge = " + str(P2.getScore()))

        chaine.configure(text = "Jolie point")

    if(Pivot.bottom_right(x,y,space,point_dico)):

        if(current_p == P1):
            P1.setScore()
        else:
            P2.setScore()

        can.create_rectangle(x, y, x+space, y+space, fill=current_p.getColor())

        info.configure(text = "Joueur Bleu  = " + str(P1.getScore()))
        info2.configure(text = "Joueur Rouge = " + str(P2.getScore()))

        chaine.configure(text = "Jolie point")

#Au tour de l'utilisateur de jouer
def point(event):

    global current_p

    if (begin) & (current_p == P1):

        if(terrain.overFlow(event.y,event.x) & terrain.checkRayon(event.y,event.x)):


            event.y = terrain.rang_twenthy(event.y)
            event.x = terrain.rang_twenthy(event.x)
            value = str(str(event.x)+'_'+str(event.y))

            if(value in point_dico):

                chaine.configure(text = "Il y a déjà un point à ce emplacement")

            else:

                r = 5
                point_dico[value] = current_p.getColor()
                can.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill=current_p.getColor())

                makeCarre(event.x,event.y)

                P2.setOtherDico(value,current_p.getColor())
                P2.updateRandomList(value)

                current_p = P2

                IAtour()

#Au tour de l'IA de jouer.
def IAtour():

    global current_p

    if(len(P2.getOwnDico()) == 0):

        #Début du jeu faire un point aléatoire
        point = P2.randPoint(can,point_dico)
        x = point['x']
        y = point['y']

    else:

        #Vérification de l'Etat des lieux
        defense = P2.checkOtherDico(point_dico,space)
        attack = P2.checkOwnDico(point_dico,space)

        if(len(attack)):

            final_dico = P2.attack()
            x = final_dico['x']
            y = final_dico['y']
            can.create_oval(x-r, y-r, x+r, y+r, fill=current_p.getColor())

        else:

            vue = randrange(1,20) % 2

            if( len(defense) & vue):
                final_dico = P2.defense()
                x = final_dico['x']
                y = final_dico['y']
                can.create_oval(x-r, y-r, x+r, y+r, fill=current_p.getColor())
            else:
                #Vérification si il y a un possibilité de construire
                P2.checkOnePointDico(point_dico,space)
                P2.checkTwoPointDico(point_dico,space)

                if(P2.canBuild()):
                    if(len(P2.twoPointDico)):
                        point = P2.buildWithTwoPoint()
                    else:
                        point = P2.buildWithOnePoint()

                    x = point['x']
                    y = point['y']
                    can.create_oval(x-r, y-r, x+r, y+r, fill=current_p.getColor())
                else:
                    point = P2.randPoint(can,point_dico)
                    x = point['x']
                    y = point['y']

    #On vide tous les dictionnaires de l'IA
    P2.clearDico()

    #Enregistrement des coordonnées dans le dictionnaire global.
    coord = str(str(x)+'_'+str(y))
    point_dico[coord] = current_p.getColor()

    #Enregistrer les cordonnées de l'IA dans son dico
    P2.setOwnDico(coord)
    P2.updateRandomList(coord)

    #Tentative de faire un carré si possible
    makeCarre(x,y)

    #Donner la main à l'utilisateur
    current_p = P1

#Corps principale du programme
fen = Tk()
fen.title("Point point Game By EnighmaLab")

can = Canvas(fen, width =Twidth, height =Theight, bg="light yellow",borderwidth=2,relief=SOLID)
can.bind('<Button-1>', point)
can.grid(row = 0, rowspan = 45)

terrain = Terrain(Twidth,Theight,space,can)

b1 = Button(fen,bg='#FAF8E9',relief=GROOVE, text='Commencer',width=15, command=create_plateform)
b1.grid(row = 0,column = 1)

b2 = Button(fen,bg='#FAF8E9',relief=GROOVE, text='Instructtion',width=15, command=create_plateform)
b2.grid(row = 1,column = 1)

info = Label(fen,bg='#6699CC', text='Joueur Bleu',width=15,pady=5,relief=GROOVE)
info.grid(row = 13,column = 1)

info2 = Label(fen,bg='#FF6666', text='Joueur Rouge',width=15,pady=5,relief=GROOVE)
info2.grid(row = 15,column = 1)

b3 = Button(fen,bg='#FAF8E9',relief=GROOVE, text='Quitter',width=15, command=create_plateform)
b3.grid(row = 44,column = 1)

role = Label(fen)
role.grid(row = 44)

chaine = Label(fen,fg='red')
chaine.grid(row = 45)


fen.mainloop()
