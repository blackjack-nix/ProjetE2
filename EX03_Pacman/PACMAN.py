import pygame
import random
import tkinter

#################################################################
##
##  variables du jeu

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

TBL = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]

# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]
CYAN  = [ 0, 255 ,255]
ORANGE = [255, 165, 0 ]
PINK = [ 255,105,180]
YELLOW = [255,255,0]

Score = 0

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels
HAUTEUR = len(TBL)     # nb de cases en hauteur
LARGEUR = len(TBL[0])  # nb de cases en largeur


def PlacementsGUM():  # placements des pacgums
   GUM = []
   for t in range(HAUTEUR):
      GUM.append([0]*LARGEUR)
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[y][x] == 0):
            GUM[y][x] = 1
   return GUM

GUM = PlacementsGUM()

PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  PINK]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  ORANGE] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  CYAN]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  RED]    )

#################################################################
##
##  INIT FENETRE


# Setup
pygame.init()
police = pygame.font.SysFont("arial", 22)
screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM
screen = pygame.display.set_mode((screeenWidth,screenHeight))
pygame.display.set_caption("ESIEE - PACMAN")
done = False
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)


#################################################################
##
##  FNT AFFICHAGE



def To(coord):
   return coord * ZOOM + ZOOM

# dessine les murs et les stockes dans un buffer
def CreateDecor():
   fond = pygame.Surface((screeenWidth,screenHeight))
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[y][x] == 1 and TBL[y][x+1] == 1 ):
            xx = To(x)
            yy = To(y)
            e = EPAISS // 2
            pygame.draw.rect(fond,BLUE,[xx,yy-e, ZOOM,EPAISS],0)

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[y][x] == 1 and TBL[y+1][x] == 1 ):
            xx = To(x)
            yy = To(y)
            e = EPAISS // 2
            pygame.draw.rect(fond,BLUE,[xx-e,yy, EPAISS,ZOOM],0)

   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[y][x] == 1):
            xx = To(x)
            yy = To(y)
            e = EPAISS // 2
            pygame.draw.ellipse(fond,BLUE,[xx-e,yy-e, EPAISS,EPAISS],0)
   return fond



DECOR = CreateDecor()

# dessine l'ensemble des éléments du jeu par dessus le décor
anim_bouche = 0
def Dessine():
   global anim_bouche
   screen.fill(BLACK)
   screen.blit(DECOR,(0,0))

   #dessine les bonbons
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[y][x] == 1):
            xx = To(x)
            yy = To(y)
            e = 4
            pygame.draw.ellipse(screen,WHITE,[xx-e,yy-e, 2*e, 2*e],0)

   #dessine pacman
   xx = To(PacManPos[0])
   yy = To(PacManPos[1])
   e = 20
   pygame.draw.ellipse(screen,YELLOW,[xx-e,yy-e, 2*e, 2*e],0)


   anim = [ 5, 10, 15,  10]
   anim_bouche = (anim_bouche+1)%len(anim)
   ouv_bouche = anim[anim_bouche]
   bouche = [(xx,yy),(xx+e,yy-ouv_bouche),(xx+e,yy+ouv_bouche)]



   pygame.draw.polygon(screen, BLACK, bouche)


   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0])
      yy = To(P[1])
      e = 15

      pygame.draw.ellipse(screen,P[2],[dec+xx-e,yy-e, 2*e, 2*e],0)
      pygame.draw.rect(screen,P[2],[dec+xx-e,yy, 2*e, e],0)
      t = 10
      pygame.draw.ellipse(screen,WHITE,[dec+xx-7-t//2,yy-t//2, t, t],0)
      pygame.draw.ellipse(screen,WHITE,[dec+xx+7-t//2,yy-t//2, t, t],0)
      t = 6
      pygame.draw.ellipse(screen,BLACK,[dec+xx-7-t//2,yy-t//2, t, t],0)
      pygame.draw.ellipse(screen,BLACK,[dec+xx+7-t//2,yy-t//2, t, t],0)

      dec += 3

   # affiche texte
   zone = police.render( "Score : "+ str(Score), True, YELLOW)
   screen.blit(zone,(300,screenHeight - 50))

#################################################################
##
##  IA RANDOM



def PacManPossibleMove():
   L = []
   x = PacManPos[0]
   y = PacManPos[1]
   if ( TBL[y-1][x  ] == 0 ): L.append((0,-1))
   if ( TBL[y+1][x  ] == 0 ): L.append((0, 1))
   if ( TBL[y  ][x+1] == 0 ): L.append(( 1,0))
   if ( TBL[y  ][x-1] == 0 ): L.append((-1,0))
   return L

def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[y-1][x  ] == 2 ): L.append((0,-1))
   if ( TBL[y+1][x  ] == 2 ): L.append((0, 1))
   if ( TBL[y  ][x+1] == 2 ): L.append(( 1,0))
   if ( TBL[y  ][x-1] == 2 ): L.append((-1,0))
   return L

def IA():
   global PacManPos, Ghosts, Score
   #deplacement Pacman
   L = PacManPossibleMove()
   choix = random.randrange(len(L))
   PacManPos[0] += L[choix][0]
   PacManPos[1] += L[choix][1]
   if GUM[PacManPos[1]][PacManPos[0]]==1 :
       GUM[PacManPos[1]][PacManPos[0]]=0
       Score += 100
   #deplacement Fantome
   for F in Ghosts:
      L = GhostsPossibleMove(F[0],F[1])
      choix = random.randrange(len(L))
      F[0] += L[choix][0]
      F[1] += L[choix][1]


#################################################################
##
##   GAME LOOP


# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)
   pygame.event.pump()
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
   IA()

   Dessine()

   pygame.display.flip()

    # Limit frames per second
   clock.tick(2)

# Close the window and quit.
pygame.quit()
