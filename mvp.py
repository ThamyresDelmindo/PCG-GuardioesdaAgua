import pygame
from pygame.math import Vector2
#Aqui coloquei um 'from' no init.py pra não ficar complicada essa exportação
#from src.tela_inicial.tela_inicial import TelaInicial 


LARGURA, ALTURA = 960, 540
FPS = 60
GRAVIDADE = 0.8
PULO = -16
VELOCIDADE = 6

def main(): 
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Guardiões da Água - MVP")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 28)

    # Cenário
    chao = pygame.Rect(0, ALTURA - 80, LARGURA, 80)

    # jOGADOR(Por enquanto um quadrado)
    player = pygame.Rect(120, ALTURA - 160,42,42)
    vel = Vector2(0, 0)
    no_chao = False

    rodando = True
    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
        # Input
        teclas = pygame.key.get_pressed()
        vel.x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            vel.x = -VELOCIDADE
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            vel.x = VELOCIDADE
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and no_chao:
            vel.y = PULO
        
        # Física básica
        vel.y += GRAVIDADE
        player.x += int(vel.x)
        player.y += int(vel.y)

        # colisão com o chão
        if player.colliderect(chao):
            player.bottom = chao.top
            vel.y = 0
            no_chao = True
        else:
            no_chao = False

        # Limites da tela
        player.left = max(player.left, 0)
        player.right = min(player.right, LARGURA)

        #Desenho
        tela.fill((18, 18, 28))
        pygame.draw.rect(tela, (30, 120, 255), chao) #chao(azul = agua/tema)
        pygame.draw.rect(tela, (240, 240, 240), player) #jogador
        txt = fonte.render("←/→ ou A/D para andar | Espaço para pular", True, (200, 200, 200))
        tela.blit(txt, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

