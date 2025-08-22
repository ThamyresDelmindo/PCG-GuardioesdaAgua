import pygame

BRANCO = (255, 255, 255)

class Jogador(pygame.sprite.Sprite):
    def __init__(self, altura):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BRANCO)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = altura - 100
        self.vel_y = 0
        self.pulo = False

    def update(self):
        self.rect.x += 5
        if self.rect.x > 800:
            self.rect.x = 0
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.y > 600 - 100:
            self.rect.y = 600 - 100
            self.vel_y = 0

    def pular(self):
        if self.rect.y == 600 - 100:
            self.vel_y = -20

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -50:
            self.rect.x = 800 + 200

class Fase1:
    def __init__(self, largura=800, altura=600):
        self.largura = largura
        self.altura = altura
        self.todos_sprites = pygame.sprite.Group()
        self.obstaculos = pygame.sprite.Group()
        self.jogador = Jogador(self.altura)
        self.todos_sprites.add(self.jogador)
        for i in range(5):
            obstaculo = Obstaculo(self.largura + i*200, self.altura - 100)
            self.todos_sprites.add(obstaculo)
            self.obstaculos.add(obstaculo)
        self.bateu = False

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            self.jogador.pular()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return "inicial"  # volta para tela inicial
        return None

    def draw(self, tela):
        self.todos_sprites.update()
        if pygame.sprite.spritecollide(self.jogador, self.obstaculos, False):
            return "pergunta"  # muda para tela de pergunta
        tela.fill((0, 0, 0))
        self.todos_sprites.draw(tela)