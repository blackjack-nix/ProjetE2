import tkinter
import random
import os

from random import *
from tkinter import messagebox

#################################################################################
#
#  Parametres du jeu

canvas = None   # zone de dessin

#Grille[0][0] désigne la case en haut à gauche
#Grille[2][0] désigne la case en haut à droite
#Grille[0][2] désigne la case en bas à gauche


Grille = [ [0,0,0],
           [0,0,0],
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille

Scores = [0,0]   # score du joueur 1 (Humain) et 2 (IA)
nbTour = 0      # Permet de savoir si on a match nul



#
#
#

###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI
#Grille[x][y]

def gagne():
    global Grille,nbTour
    for i in range(0,3):
        if Grille[0][i] != 0 and Grille[0][i] == Grille[1][i] and Grille[0][i] == Grille[2][i]:
            Scores[Grille[0][i]-1]+=1   #ligne gagnate donc on return le numero du joueur
            reset()                        #1 pour l'ia et 0 pour l'humain
            return Grille[0][i]
        if Grille[i][0] != 0 and Grille[i][0] == Grille[i][1] and Grille[i][0] == Grille[i][2]:
            Scores[Grille[i][0]-1]+=1     #colonne gagnate
            reset()
            return Grille[i][0]

    if Grille[0][0] != 0 and Grille[0][0] == Grille[1][1] and Grille [0][0] == Grille[2][2]:
        Scores[Grille[0][0]-1]+=1
        reset()
        return Grille[0][0]

    if Grille[2][0] != 0 and Grille[2][0] == Grille[1][1] and Grille[2][0] == Grille[0][2]:
        Scores[Grille[2][0]-1]+=1
        reset()
        return Grille[0][2]

    if nbTour == 9 :
        reset()
        return -1

    return 0








def Play(x,y):
    global Grille,nbTour

    #tour de l'humain
    if Grille[x][y] != 0:
        return 0
    Grille[x][y] = 1
    nbTour += 1
    Affiche(gagne())


    #tour de l'ia
    os.system("sleep 1")
    IAjoue = False
    if nbTour == 0:return 0 #code d'erreur pas ok

    CoupIA = JoueurSimule(2)
    print(CoupIA[1])
    DeplacementIA = CoupIA[1]
    Grille[DeplacementIA[0]][DeplacementIA[1]]=2


    nbTour += 1
    Affiche(gagne())

    return 1 #code d'erreur ok



def reset():
    global Grille,nbTour
    nbTour = 0
    os.system("sleep 1")
    Grille=[ [0,0,0],
             [0,0,0],
             [0,0,0] ]
    Affiche()

def coupsPossibles():
    global Grille
    L = []
    for i in range(0,3):
        for j in range(0,3):
            if Grille[i][j]==0:
                L.append((i,j))
    return L


def JoueurSimule(IDjoueur): #ID joueur : 1 humain 2 IA
    global Grille
    if(gagne() != 0):
        return CalculScore()
    L=coupsPossibles()
    Resultats=[]
    for k in L:
        print(k)
        Grille[k[0]][k[1]] = IDjoueur
        if IDjoueur==1 : Score = JoueurSimule(2)
        else : Score=JoueurSimule(1)
        Resultats.append((Score,IDjoueur),k)
        Grille[k[0],k[1]]=0
    return max(Resultats)


def CalculScore():
    gagne = gagne()
    if gagne == 2 : return (0,1)
    if gagne == 1 : return (1,0)
    return (0,0)

################################################################################
#
# Dessine la grille de jeu

def Affiche(PartieGagnee = 0):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        fillcoul='blue'
        if (PartieGagnee == 1) : fillcoul = 'red'
        if (PartieGagnee == 2) : fillcoul = 'yellow'
        if (PartieGagnee == 3) : fillcoul = 'white'
        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill=fillcoul, width="4" )
            canvas.create_line(0,i*100,300,i*100,fill=fillcoul, width="4" )

        for x in range(3):
            for y in range(3):
                xc = x * 100
                yc = y * 100
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )

        msg = 'SCORES : ' + str(Scores[0]) + '-' + str(Scores[1])
        fillcoul = 'gray'
        canvas.create_text(150,400, font=('Helvetica', 30), text = msg, fill=fillcoul)


        canvas.update()   #force la mise a jour de la zone de dessin


####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):

    window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return


    print("clicked at", x,y)

    if not Play(x,y):
        print("erreur")
        return

          # gestion du joueur humain et de l'IA


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

# fenetre
window = tkinter.Tk()
window.geometry("300x500")
window.title('Mon Super Jeu')
window.protocol("WM_DELETE_WINDOW", lambda : window.destroy())
window.bind("<Button-1>", MouseClick)

#zone de dessin
WIDTH = 300
HEIGHT = 500
canvas = tkinter.Canvas(window, width=WIDTH , height=HEIGHT, bg="#000000")
canvas.place(x=0,y=0)
Affiche()

# active la fenetre
window.mainloop()
