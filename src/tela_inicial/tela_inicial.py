import os
import math
import pygame

TITULO = "Guardiões da Água"
SUB = "Vamos derrotar o vilão juntos!"

class TelaInicial:
    def __init__(self, largura=960, altura=540):
        self.largura = largura
        self.altura = altura

        # --- Caminhos das imagens ---
        pasta = os.path.join("src", "tela_inicial", "imagens")
        fundo_path = os.path.join(pasta, "background.png")
        fred_path = os.path.join(pasta, "persona1.png")     # Fred
        rosinha_path = os.path.join(pasta, "persona2.png")  # Rosinha
        start_path = os.path.join(pasta, "start.png")
        caixa_texto_path = os.path.join(pasta, "caixa_texto.png")

        # --- Carregamento e ajustes iniciais ---
        self.fundo = pygame.image.load(fundo_path).convert_alpha()
        self.fundo = pygame.transform.smoothscale(self.fundo, (largura, altura))

        self.fred_base = pygame.image.load(fred_path).convert_alpha()
        self.rosi_base = pygame.image.load(rosinha_path).convert_alpha()
        self.start_base = pygame.image.load(start_path).convert_alpha()
        self.caixa_base = pygame.image.load(caixa_texto_path).convert_alpha()

        #guarda mtimes pra saber quando recarregar - isso atrelado ao def 'assets'
        self._mtimes = {k: 0 for k in self.paths}
        # superfícies (vazias por enquanto)
        self.fundo = self.fred_base = self.rosi_base = self.start_base = self.caixa_base = None
        self._carregar_assets()  # primeira carga

        # Escalas base (ajuste fino se quiserem)
        fred_h = int(altura * 0.40)      # altura aproximada do Fred
        rosi_h = int(altura * 0.55)      # altura aproximada da Rosinha
        self.fred_base = self._scale_h(self.fred_base, fred_h)
        self.rosi_base = self._scale_h(self.rosi_base, rosi_h)

        start_w = int(largura * 0.22)
        self.start_base = self._scale_w(self.start_base, start_w)

        caixa_w = int(largura * 0.40)
        self.caixa_base = self._scale_w(self.caixa_base, caixa_w)

        # Retângulos de posicionamento (atualizados a cada draw)
        self.fred_rect = self.fred_base.get_rect()
        self.rosi_rect = self.rosi_base.get_rect()
        self.start_rect = self.start_base.get_rect()
        self.caixa_rect = self.caixa_base.get_rect()

        # Posições “âncora”
        self.fred_anchor = (int(largura * 0.06), int(altura * 0.35))
        self.rosi_anchor = (int(largura * 0.72), int(altura * 0.35))
        self.start_anchor = (largura // 2, int(altura * 0.46))
        self.caixa_anchor = (largura // 2, int(altura * 0.60))

        self.t0 = pygame.time.get_ticks()

    # ---------- Utilidades ----------
    def _scale_h(self, surf: pygame.Surface, new_h: int) -> pygame.Surface:
        w, h = surf.get_size()
        new_w = int(w * (new_h / h))
        return pygame.transform.smoothscale(surf, (new_w, new_h))

    def _scale_w(self, surf: pygame.Surface, new_w: int) -> pygame.Surface:
        w, h = surf.get_size()
        new_h = int(h * (new_w / w))
        return pygame.transform.smoothscale(surf, (new_w, new_h))

    # ---------- API da Tela ----------
    def handle_event(self, evento):
        """Retorna a rota 'fase1' se ENTER ou clique no botão START."""
        # ENTER
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            return "fase1"

        # Clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.start_rect.collidepoint(evento.pos):
                return "fase1"

        return None


    #Esse def é só para conseguir fazer alterações nos bonecos em tempo real,
    #sem precisar ficar rodando o jogo a cada alteração
    def _carregar_assets(self):
        # carrega/recupera cada imagem se o arquivo mudou
        for key, path in self.paths.items():
            try:
                m = os.path.getmtime(path)
                if m != self._mtimes[key]:
                    img = pygame.image.load(path).convert_alpha()
                    self._mtimes[key] = m
                    if key == "fundo":
                        self.fundo = pygame.transform.smoothscale(img, (self.largura, self.altura))
                    elif key in ("fred", "rosi"):
                        img = self._scale_h(img, int(self.altura * 0.55))
                        if key == "fred": self.fred_base = img
                        else: self.rosi_base = img
                    elif key == "start":
                        self.start_base = self._scale_w(img, int(self.largura * 0.22))
                    elif key == "caixa":
                        self.caixa_base = self._scale_w(img, int(self.largura * 0.40))
            except FileNotFoundError:
                pass  # ainda não existe? sem pânico no dev    



    def draw(self, tela, fonte_titulo, fonte_sub):
        # Fundo
        self._carregar_assets()
        tela.blit(self.fundo, (0, 0))

        # Tempo para animações
        t = (pygame.time.get_ticks() - self.t0) / 1000.0

        # -------- Fred (bobbing + leve rotação) --------
        fred_bob = int(6 * math.sin(t * 2.0))
        fred_rot = 2.0 * math.sin(t * 1.2)  # graus
        fred_img = pygame.transform.rotozoom(self.fred_base, fred_rot, 1.0)
        self.fred_rect = fred_img.get_rect()
        self.fred_rect.topleft = (self.fred_anchor[0], self.fred_anchor[1] + fred_bob)
        tela.blit(fred_img, self.fred_rect)

        # -------- Rosinha (bobbing fora de fase + leve rotação) --------
        rosi_bob = int(6 * math.sin(t * 2.0 + math.pi))
        rosi_rot = -2.0 * math.sin(t * 1.2 + 0.7)
        rosi_img = pygame.transform.rotozoom(self.rosi_base, rosi_rot, 1.0)
        self.rosi_rect = rosi_img.get_rect()
        self.rosi_rect.topleft = (self.rosi_anchor[0], self.rosi_anchor[1] + rosi_bob)
        tela.blit(rosi_img, self.rosi_rect)

        # -------- START (hover + pulso) --------
        mouse = pygame.mouse.get_pos()
        hovering = False

        # pulso suave
        pulse = 1.0 + 0.02 * math.sin(t * 5.0)

        start_img = self.start_base
        if self.start_base.get_width() > 0:
            start_img = pygame.transform.rotozoom(self.start_base, 0, pulse)

        self.start_rect = start_img.get_rect(center=self.start_anchor)

        # efeito hover (cresce +2%)
        if self.start_rect.collidepoint(mouse):
            hovering = True
            start_img = pygame.transform.rotozoom(self.start_base, 0, pulse + 0.05)
            self.start_rect = start_img.get_rect(center=self.start_anchor)

        tela.blit(start_img, self.start_rect)

        # -------- Caixa de texto --------
        self.caixa_rect = self.caixa_base.get_rect(center=self.caixa_anchor)
        tela.blit(self.caixa_base, self.caixa_rect)

        # Texto sobre a caixa
        txt = fonte_titulo.render(SUB, True, (255, 255, 255))
        txt_pos = txt.get_rect(center=self.caixa_rect.center)
        tela.blit(txt, txt_pos)

        # Dica de interação
        dica = fonte_sub.render("ENTER ou clique em START", True, (30, 30, 30))
        dica_pos = dica.get_rect(center=(self.largura // 2, self.altura - 24))
        tela.blit(dica, dica_pos)
