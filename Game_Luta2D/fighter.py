import pygame


class Fighter():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:Parado, 1: Correr, 2: Pular, 3: Ataque1, 4: Ataque2, 5: Colisao, 6: Vida
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
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
        self.running = False
        self.attack_type = 0

        #Eventos de botao:
        key = pygame.key.get_pressed()

        #Perfomance dos Ataques
        if self.attacking == False:
            #Movimentos:
            if key[pygame.K_a]:
                dx = -SPEED
                self.running = True
            if key[pygame.K_d]:
                dx = SPEED
                self.running = True
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
        #Aplicando o Cooldown do Ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #Update da posicao do jogador
        self.rect.x += dx
        self.rect.y += dy

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        #Checando ações do Jogador
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) #6: Morto
        elif self.hit == True:
            self.update_action(5) #5: hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) #3: Ataque1
            elif self.attack_type == 2:
                self.update_action(4) #4: Ataque 2
        elif self.jump == True:
            self.update_action(2)#2: Pulando
        elif self.running == True:
            self.update_action(1)#1: Andando
        else:
            self.update_action(0)

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #Checando se o ataque foi executado
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #Checando o Dano ao Personagem
                if self.action == 5:
                    self.hit = False
                    #interrompe o ataque ao acertar o alvo
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, 'red', self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

