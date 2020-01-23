import tkinter
from tkinter import messagebox
import random
import os
import copy

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
# 1 et 2 pour joueur 1 et joueur 2

Scores = [0,0]   # score du joueur 1 (Humain) et 2 (IA)

DebutDePartie = False




###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI
def init():
    global Grille
    # attendre un petit temps
    os.system("sleep 1")
    # remettre la grille à zero
    Grille = [ [0,0,0], [0,0,0], [0,0,0] ]


def gagne(grille):
    # chercher une situation gagnante
    for i in range(0,3):
        if (grille[0][i] != 0 and grille[0][i] == grille[1][i] and grille[1][i] == grille[2][i]):
            return grille[0][i]

        if (grille[i][0] != 0 and grille[i][0] == grille[i][1] and grille[i][1] == grille[i][2]):
            return grille[i][0]

    if (grille[0][0] != 0 and grille[0][0] == grille[1][1] and grille[0][0] == grille[2][2]):
        return grille[0][0]

    if (grille[0][2] != 0 and grille[0][2] == grille[1][1] and grille[0][2] == grille[2][0]):
        return grille[0][2]
    # regarder si la grille est pleine : égalité
    if (not CoupPossibles(grille)):
        return -1

    return 0



def CalculScore(grille):
    result = gagne(grille)
    if result==1 : return -1
    if result==2 : return 1
    if result==-1 : return 0



def CoupPossibles(grille):
    possible = []
    for x in range(0,3):
        for y in range(0,3):
            if (grille[x][y] == 0):
                possible.append((x,y))
    return possible




def SimulIA(grille):
    Score_max = -1000
    liste_possible = CoupPossibles(grille)
    if gagne(grille) == -1 : return (0,None)
    if gagne(grille) == 1 : return (-1,None)
    if gagne(grille) == 2 : return (1,None)
    meilleur_coup = liste_possible[0]
    for coup in liste_possible:
        grille[coup[0]][coup[1]] = 2
        Score = SimulHumain(grille)[0]
        if Score_max < Score :
            Score_max = Score
            meilleur_coup = coup
        grille[coup[0]][coup[1]] = 0
    return (Score_max,meilleur_coup)



def SimulHumain(grille):
    Score_min = 1000
    liste_possible = CoupPossibles(grille)
    if gagne(grille) == -1: return (0,None)
    if gagne(grille) == 1 : return (-1,None)
    if gagne(grille) == 2 : return (1,None)
    meilleur_coup = liste_possible[0]
    for coup in liste_possible:
        grille[coup[0]][coup[1]] = 1
        Score = SimulIA(grille)[0]
        if Score_min > Score :
            Score_min = Score
            meilleur_coup = coup
        grille[coup[0]][coup[1]] = 0
    return (Score_min,meilleur_coup)



def Play(x,y):
    global Grille
    # savoir si le placement est possible
    Grille[x][y] = 1
    # regarder si l'humain a gagner
    Affiche()
    # joueur IA

def joueIA():
    global Grille
    coupIA = SimulIA(Grille)[1]
    Grille[coupIA[0]][coupIA[1]] = 2
    Affiche()
    return 1


################################################################################
#
# Dessine la grille de jeu

def Affiche(PartieGagnee = 0):
        global Grille, Scores
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        # couleur de la grille enn fonction de qui a gagner la precedente partie
        fillcoul = "blue"
        if (PartieGagnee == 1): fillcoul = "red"
        if (PartieGagnee == 2): fillcoul = "yellow"
        if (PartieGagnee == -1): fillcoul = "white"

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
        #fillcoul = 'gray'
        #if (PartieGagnee) : fillcoul = 'red'
        canvas.create_text(150,400, font=('Helvetica', 30), text = msg, fill=fillcoul)


        canvas.update()   #force la mise a jour de la zone de dessin


####################################################################################
#
#  fonction appelée par un clic souris sur la zone de dessin

def MouseClick(event):
    global DebutDePartie,Grille
    window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return


    print("clicked at", x,y)

    if DebutDePartie == True :
        init()
        Affiche()
        DebutDePartie = False

    if Grille[x][y] != 0 :
        print('case invalide')
        return

    Play(x,y)
    gagnant = gagne(Grille)
    if gagnant != 0 :
        if gagnant == 1 : Scores[0] += 1
        DebutDePartie=True
        Affiche(gagnant)
    else :
        os.system("sleep 1")
        joueIA()
        IAgagne = gagne(Grille)
        if IAgagne != 0 :
            if IAgagne == 2 : Scores[1] += 1
            DebutDePartie = True
            Affiche(IAgagne)


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
