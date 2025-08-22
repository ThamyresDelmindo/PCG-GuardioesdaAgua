import pygame

class PerguntaTela:
    def __init__(self, largura, altura, pergunta, resposta_correta):
        # Aqui é a estrutura básica da tela de pergunta, largura, altura, pergunta e resposta correta
        self.largura = largura
        self.altura = altura
        self.pergunta = pergunta
        self.resposta_correta = resposta_correta
        self.fonte = pygame.font.SysFont(None, 32)
        self.input_text = ""
        self.resultado = None

    def handle_event(self, e):
        #Aqui lidamos com os eventos, como digitar a resposta e pressionar Enter    
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return "inicial"  # Retorna para a tela inicial
            elif e.key == pygame.K_RETURN:
                if self.input_text.lower() == self.resposta_correta.lower():
                    self.resultado = "correto"
                else:
                    self.resultado = "errado"
                return "fase1"  # volta para o jogo
            elif e.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                char = e.unicode
                if char.isprintable():
                    self.input_text += char
        return None

    def draw(self, tela):
        #Aqui desenhamos a tela de pergunta, a pergunta em si, o input do usuário e o resultado se houver
        tela.fill((30, 30, 60))
        bateu_render = self.fonte.render("Bateu", True, (255, 255, 255))
        tela.blit(bateu_render, (50, 50))
        pergunta_render = self.fonte.render(self.pergunta, True, (255, 255, 255))
        tela.blit(pergunta_render, (50, 100))
        input_render = self.fonte.render(self.input_text, True, (255, 255, 0))
        tela.blit(input_render, (50, 150))
        if self.resultado:
            resultado_render = self.fonte.render(self.resultado, True, (0, 255, 0) if self.resultado == "correto" else (255, 0, 0))
            tela.blit(resultado_render, (50, 200))