import pygame
from pygame.math import Vector2

GRAVIDADE = 0.8
PULO = -16
VELOCIDADE = 6

class MVP:
    def __init__(self, largura=960, altura=540):
        self.largura = largura
        self.altura = altura

        # cenário
        self.chao = pygame.Rect(0, self.altura - 80, self.largura, 80)

        # jogador (quadradinho)
        self.player = pygame.Rect(120, self.altura - 160, 42, 42)
        self.vel = Vector2(0, 0)
        self.no_chao = False

        # UI
        self.fonte = pygame.font.SysFont(None, 28)

    def handle_event(self, e):
        # por enquanto, nada que mude de “tela”
        return None

    def _update(self):
        # input contínuo
        teclas = pygame.key.get_pressed()
        self.vel.x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vel.x = -VELOCIDADE
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel.x = VELOCIDADE
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and self.no_chao:
            self.vel.y = PULO

        # física básica
        self.vel.y += GRAVIDADE
        self.player.x += int(self.vel.x)
        self.player.y += int(self.vel.y)

        # colisão chão
        if self.player.colliderect(self.chao):
            self.player.bottom = self.chao.top
            self.vel.y = 0
            self.no_chao = True
        else:
            self.no_chao = False

        # limites da tela
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > self.largura:
            self.player.right = self.largura

    def draw(self, tela):
        self._update()

        # desenha
        tela.fill((18, 18, 28))
        pygame.draw.rect(tela, (30, 120, 255), self.chao)   # chão (água)
        pygame.draw.rect(tela, (240, 240, 240), self.player)  # jogador
        txt = self.fonte.render("←/→ ou A/D para andar | Espaço para pular", True, (200, 200, 200))
        tela.blit(txt, (20, 20))