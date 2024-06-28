import pygame


class Fighter():
    def __init__(self, x, y, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:Parado, 1: Correr, 2: Pular, 3: Ataque1, 4: Ataque2, 5: Colisao, 6: Vida
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        self.flip = False

    def load_images(self, sprite_sheet, animation_steps):
        #Extraindo imagens separadas dos Sprites
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list



    def move(self, width, heigth, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        #Eventos de botao:
        key = pygame.key.get_pressed()

        #Perfomance dos Ataques
        if self.attacking == False:
            #Movimentos:
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED
            #Pulo
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            #Ataques
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                #Determinando o tipo de ataque
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

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
            self.jump = False

        #Sempre de frente para o oponente
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #Update da posicao do jogador
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, 'red', self.rect)
        surface.blit(self.image, (self.rect.x, self.rect.y))

