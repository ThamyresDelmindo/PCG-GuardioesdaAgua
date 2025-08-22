import pygame
import random

# Inicializar pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Guardiões da Água")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Classe do jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BRANCO)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTURA - 100
        self.vel_y = 0
        self.pulo = False

    def update(self):
        # Movimento automático para frente (loop infinito)
        self.rect.x += 5
        if self.rect.x > LARGURA:
            self.rect.x = -50  # volta para o início da tela

        # Gravidade
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.y >= ALTURA - 100:
            self.rect.y = ALTURA - 100
            self.vel_y = 0
            self.pulo = False

    def pular(self):
        if not self.pulo:
            self.vel_y = -15
            self.pulo = True

# Classe dos obstáculos
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(random.choice([VERMELHO, VERDE, AZUL]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Movimento dos obstáculos para esquerda
        self.rect.x -= 5
        if self.rect.x < -50:
            self.rect.x = LARGURA + random.randint(100, 300)
            self.rect.y = ALTURA - 100

# Criar grupos de sprites
todos_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()

jogador = Jogador()
todos_sprites.add(jogador)

# Criar alguns obstáculos
for i in range(5):
    obstaculo = Obstaculo(LARGURA + i*200, ALTURA - 100)
    todos_sprites.add(obstaculo)
    obstaculos.add(obstaculo)

# Loop principal
clock = pygame.time.Clock()
rodando = True
while rodando:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jogador.pular()

    # Atualizar
    todos_sprites.update()

    # Verificar colisões
    if pygame.sprite.spritecollide(jogador, obstaculos, False):
        print("Bateu!")

    # Desenhar
    tela.fill((0, 0, 0))
    todos_sprites.draw(tela)
    pygame.display.flip()

pygame.quit()
