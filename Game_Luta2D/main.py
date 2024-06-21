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

#Background do Game
bg_image = pygame.image.load('data/images/background/background.jpg').convert_alpha()

#funcoes do draw
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    screen.blit(scale_bg, (0, 0))

#Instancias do Jogador
fighter1 = Fighter(200, 310)
fighter2 = Fighter(700, 310)

#GameLoop
gameLoop = True
while gameLoop:
    clock.tick(FPS)

    #draw background
    draw_bg()

    #Movimentoss do jogador
    fighter1.move(WIDTH, HEIGHT)
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