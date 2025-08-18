import pygame
from src.tela_inicial import TelaInicial
# from src.fase1 import Fase1
# from src.perguntas import Perguntas
from mvp import MVP

LARGURA, ALTURA = 960, 540
FPS = 60

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Guardiões da Água")
    clock = pygame.time.Clock()

    # rotas → cada classe numa “página”
    telas = {
        "tela_inicial": TelaInicial(LARGURA, ALTURA),
        #"fase1": Fase1(LARGURA, ALTURA),
        # "perguntas": Perguntas(LARGURA, ALTURA),
        "fase1": MVP(LARGURA, ALTURA),
    }

    estado = "tela_inicial"  # rota inicial

    rodando = True
    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                rodando = False
            else:
                proximo = telas[estado].handle_event(e)
                if proximo in telas:
                    estado = proximo

        # draw agora não recebe fontes
        telas[estado].draw(tela)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()