import pygame


class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0


    def move(self, width, heigth):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        #Eventos de botao:
        key = pygame.key.get_pressed()

        #Movimentos:
        if key[pygame.K_a]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED
        #Pulo
        if key[pygame.K_w]:
            self.vel_y = -30

        #Gravidade
        self.vel_y += GRAVITY
        dy += self.vel_y

        #Garantindo jogador fique dentro da tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > width:
            dx = width - self.rect.right
        if self.rect.bottom + dy > heigth - 110:
            self.vel_y = 0
            dy = heigth - 110 - self.rect.bottom

        #Update da posicao do jogador
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, 'red', self.rect)

