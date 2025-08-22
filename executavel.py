import pygame
from src.tela_inicial import TelaInicial
from src.fase1 import Fase1
from src.pergunta_tela import PerguntaTela
from mvp import MVP


LARGURA, ALTURA = 960, 540
FPS = 60

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Guardiões da Água")
    clock = pygame.time.Clock()

    # Só MVP para garantir funcionamento
    telas = {
        "inicial": TelaInicial(LARGURA, ALTURA),  # Tela inicial não está implementada
        "fase1": Fase1(LARGURA, ALTURA),
        "pergunta": PerguntaTela(LARGURA, ALTURA, "Qual é a capital da França?", "Paris"),  
        "mvp": MVP(LARGURA, ALTURA) # Adiciona a tela do MVP    
    }

    estado = "inicial"  # inicia direto no MVP

    rodando = True
    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
            else:
                proximo = telas[estado].handle_event(e)
                if proximo in telas and proximo != estado:
                    estado = proximo

        proximo_draw = telas[estado].draw(tela)
        if proximo_draw in telas and proximo_draw != estado:
            estado = proximo_draw

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
    