import pygame
from fighter import Fighter

pygame.init()

#Tamanho da tela e configuracao
WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Versus 2D")

#Frames por seg.
clock = pygame.time.Clock()
FPS = 60

#Paleta de Cores
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#Load dos Sprites
warrior_sheet = pygame.image.load('data/images/warrior/Sprites/warrior.png').convert_alpha()
wizard_sheet = pygame.image.load('data/images/wizard/Sprites/wizard.png').convert_alpha()

#Definicao das variaveis dos Guererreiros
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE]

#Definindo os quadros de cada Sprite
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1 ,8 ,8 , 3 , 7]

#Background do Game
bg_image = pygame.image.load('data/images/background/background.jpg').convert_alpha()

#funcoes do draw
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    screen.blit(scale_bg, (0, 0))

#Funcao de Sangue do Personagem
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


#Instancias do Jogador
fighter1 = Fighter(200, 310, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter2 = Fighter(700, 310, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

#GameLoop
gameLoop = True
while gameLoop:
    clock.tick(FPS)

    #draw background
    draw_bg()

    # Vida Personagem
    draw_health_bar(fighter1.health, 20, 20)
    draw_health_bar(fighter2.health, 580, 20)

    #Movimentoss do jogador
    fighter1.move(WIDTH, HEIGHT, screen, fighter2)
    # fighter2.move()

    #draw Jogadores
    fighter1.draw(screen)
    fighter2.draw(screen)

    #Evento de Fechar o Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False

    #update display
    pygame.display.update()



#saindo do PyGame
pygame.quit()