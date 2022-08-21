import pygame
from random import randint
import os

pygame.init()
pygame.mixer.init()
LARGEUR, HAUTEUR = 1500, 800
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('ping pong')
pygame.display.set_icon(pygame.image.load('favicon.png'))
FPS = 60

son_joueur = pygame.mixer.Sound(os.path.join("assets", "pong_joueur.wav"))
son_mur = pygame.mixer.Sound(os.path.join("assets", "pong_mur.wav"))
son_point = pygame.mixer.Sound(os.path.join("assets", "pong_point.wav"))



separateur = []
N = 10
LARGEUR_SEP = 2
HAUTEUR_SEP = HAUTEUR/N
OFFSET = 20

for i in range(N):
    x = (LARGEUR - LARGEUR_SEP)/2
    y = i*HAUTEUR_SEP + OFFSET/2
    separateur.append(pygame.Rect(x, y, LARGEUR_SEP, HAUTEUR_SEP - OFFSET))
    
VITESSE_BOULE = 7
VITESSE_BOULE_LENT = 4

class joueur:
    LARGEUR = 10
    HAUTEUR = 75
    VITESSE = 6
    FONT = pygame.font.SysFont(None, 100)
    

    
    def __init__(self, pos = (0,0)):
        self.rect = pygame.Rect(pos[0], pos[1], joueur.LARGEUR, joueur.HAUTEUR)
        self.score = 0
        
    def deplacer_haut(self):
        self.rect.y -= joueur.VITESSE
        
    def deplacer_bas(self):
        self.rect.y += joueur.VITESSE
        
    def score_surface(self):
        return joueur.FONT.render(str(self.score), True, 'white')
    
def direction_y_boule(x):
    return x*0.3
    
def gerer_collisions(boule, boule_direction, joueur_g, joueur_d):
    if boule.colliderect(joueur_g.rect): 
        changer_vitesse_boule(boule_direction, VITESSE_BOULE)
        boule_direction.x = -boule_direction.x
        boule_direction.y = direction_y_boule(boule.center[1] - joueur_g.rect.center[1])
        son_joueur.play()
        
    if boule.colliderect(joueur_d.rect):
        changer_vitesse_boule(boule_direction, VITESSE_BOULE)
        boule_direction.x = -boule_direction.x
        boule_direction.y = direction_y_boule(boule.center[1] - joueur_d.rect.center[1])
        son_joueur.play()
    
    
def initialiser_boule(boule, boule_direction):
    boule.x = LARGEUR/2
    boule.y = randint(HAUTEUR/4, HAUTEUR - HAUTEUR/4)
    changer_vitesse_boule(boule_direction, VITESSE_BOULE_LENT)
   
    
def changer_vitesse_boule(boule_direction, vitesse):
    boule_direction.x = vitesse if boule_direction.x > 0 else -vitesse
    boule_direction.y = vitesse if boule_direction.y > 0 else -vitesse
    

def deplacer_boule(boule, boule_direction):
    if boule.x <= 0:
        joueur_d.score += 1
        initialiser_boule(boule, boule_direction)
        son_point.play()
        
    if boule.x + DIM_BOULE >= LARGEUR:
        joueur_g.score += 1
        initialiser_boule(boule, boule_direction)
        son_point.play()
    
    if boule.y <= 0 or boule.y + DIM_BOULE >= HAUTEUR:
        boule_direction.y = -boule_direction.y
        son_mur.play()
   
    boule.x += boule_direction.x
    boule.y += boule_direction.y
     

def dessiner(joueur_d, joueur_g, boule):
    fenetre.fill("black")
    
    for sep in separateur:
        pygame.draw.rect(fenetre, 'white', sep)
    
    pygame.draw.rect(fenetre, 'white', joueur_g.rect)
    pygame.draw.rect(fenetre, 'white', joueur_d.rect)
    pygame.draw.rect(fenetre, 'white', boule)
    
    fenetre.blit(joueur_g.score_surface(), (LARGEUR/2 - 100, 10))
    score_surf = joueur_d.score_surface()
    fenetre.blit(score_surf, (LARGEUR/2 + 100 - score_surf.get_width(), 10))
    
    
    pygame.display.update()
    
    
    
joueur_g = joueur((5, (HAUTEUR - joueur.HAUTEUR)/2))
joueur_d = joueur((LARGEUR - joueur.LARGEUR - 5 , (HAUTEUR - joueur.HAUTEUR)/2))

DIM_BOULE = 10
boule = pygame.Rect(LARGEUR/2, HAUTEUR/2, DIM_BOULE, DIM_BOULE)
boule_direction = boule.copy()
    
def main():
    executer = True
    clock = pygame.time.Clock()
    initialiser_boule(boule, boule_direction)
    while executer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executer = False
                
        touches = pygame.key.get_pressed()
        if touches[pygame.K_1] and joueur_g.rect.y > 0:
            joueur_g.deplacer_haut()
            
        if touches[pygame.K_2] and joueur_g.rect.y + joueur.HAUTEUR < HAUTEUR:
            joueur_g.deplacer_bas()
            
        if touches[pygame.K_UP] and joueur_d.rect.y > 0:
            joueur_d.deplacer_haut()
            
        if touches[pygame.K_DOWN] and joueur_d.rect.y + joueur.HAUTEUR < HAUTEUR:
            joueur_d.deplacer_bas()
         
        gerer_collisions(boule, boule_direction, joueur_g, joueur_d)
        deplacer_boule(boule, boule_direction)      
        dessiner(joueur_d, joueur_g, boule)
        clock.tick(FPS)
        
        
    pygame.quit()
    
if __name__ == "__main__":
    main()