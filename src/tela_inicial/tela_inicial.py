import pygame

TITULO = "Guardioes da Agua"
SUB = "Pressione 'Enter' para iniciar o jogo"

class TelaInicial:
    def __init__(self, largura=960, altura=540):
        self.largura = largura
        self.altura = altura
        self.logo_color = (30, 120, 255) #cor azul da agua
        self.ticks_base = pygame.time.get_ticks()

    def handle_event(self, evento):
        """Retorna True quando ENTER for pressionado
        (vai para a próxima tela no futuro)"""
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            return "fase1" #Aqui o executável vai entender o que rodar
        return None
    
    def draw(self, tela, fonte_titulo, fonte_sub):
        #fundo da tela
        tela.fill((10, 20, 40))

        #logo do jogo (gotinha)
        center = (self.largura // 2, 180)
        pygame.draw.circle(tela, self.logo_color, center, 70)
        pygame.draw.polygon(
            tela, (10, 20, 40),
            [(center[0], center[1]-80), (center[0]-20, center[1]-20),
            (center[0]+20, center[1]-20)],
        )

        #textos estilização
        t1 = fonte_titulo.render(TITULO, True, (235, 245, 255))
        tela.blit(t1, (center[0] - t1.get_width() // 2, 270))

        #efeito especial no subtitulo
        elapsed = pygame.time.get_ticks() - self.ticks_base
        if (elapsed // 500) % 2 == 0:
            t2 = fonte_sub.render(SUB, True, (210, 220, 235))
            tela.blit(t2, (center[0] - t2.get_width() // 2, 320))

        #créditos/atalhos discretos
        hint = fonte_sub.render("Use ENTER|ESC para sair", True, (160, 170, 185))
        tela.blit(hint, (self.largura - hint.get_width() -16, self.altura - hint.get_height() -12))
