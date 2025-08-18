import os
import math
import pygame

TITULO = "Guardiões da Água"

class TelaInicial:
    def __init__(self, largura=960, altura=540):
        self.largura = largura
        self.altura = altura

        # --- BASE DE CAMINHO: pasta deste arquivo ---
        base_dir = os.path.dirname(__file__)
        pasta_img = os.path.join(base_dir, "imagens")

        # --- Tabela de assets (NÃO carregamos aqui) ---
        self.paths = {
            "fundo":     os.path.join(pasta_img, "background.png"),
            "fred":      os.path.join(pasta_img, "persona1.png"),
            "rosi":      os.path.join(pasta_img, "persona2.png"),
            "start":     os.path.join(pasta_img, "start.png"),
            "nomejogo":  os.path.join(pasta_img, "nomejogo.png"),  # arte do título
            "caixa":     os.path.join(pasta_img, "caixa_texto.png"),
        }

        # mtimes para hot-reload
        self._mtimes = {k: 0 for k in self.paths}

        # superfícies (inicialmente None; _carregar_assets vai preencher)
        self.fundo = None
        self.fred_base = None
        self.rosi_base = None
        self.start_base = None
        self.caixa_base = None
        self.nomejogo_base = None

        # primeira carga
        self._carregar_assets()

        # retângulos de posicionamento (atualizados no draw)
        self.fred_rect = pygame.Rect(0, 0, 0, 0)
        self.rosi_rect = pygame.Rect(0, 0, 0, 0)
        self.start_rect = pygame.Rect(0, 0, 0, 0)
        self.caixa_rect = pygame.Rect(0, 0, 0, 0)
        self.nomejogo_rect = pygame.Rect(0, 0, 0, 0)

        # âncoras
        self.fred_anchor  = (int(largura * 0.06), int(altura * 0.35))
        self.rosi_anchor  = (int(largura * 0.72), int(altura * 0.35))
        self.start_anchor = (int(largura * 0.535),    int(altura * 0.60))
        self.caixa_anchor = (int(largura * 0.535),    int(altura * 0.700))
        self.nomejogo_anchor = (int(largura * 0.560), int(altura * 0.040))

        self.t0 = pygame.time.get_ticks()

    # ---------- Utilidades ----------
    def _scale_h(self, surf: pygame.Surface, new_h: int) -> pygame.Surface:
        w, h = surf.get_size()
        new_w = max(1, int(w * (new_h / h)))
        return pygame.transform.smoothscale(surf, (new_w, new_h))

    def _scale_w(self, surf: pygame.Surface, new_w: int) -> pygame.Surface:
        w, h = surf.get_size()
        new_h = max(1, int(h * (new_w / w)))
        return pygame.transform.smoothscale(surf, (new_w, new_h))

    # ---------- API ----------
    def handle_event(self, evento):
        """Retorna 'fase1' no ENTER ou clique no START."""
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            return "fase1"
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.start_rect.collidepoint(evento.pos):
                return "fase1"
        return None

    # ---------- Hot-reload de assets ----------
    def _carregar_assets(self):
        """Carrega/recarga imagens quando o arquivo muda no disco."""
        for key, path in self.paths.items():
            try:
                m = os.path.getmtime(path)
                if m != self._mtimes[key]:
                    img = pygame.image.load(path).convert_alpha()
                    self._mtimes[key] = m

                    if key == "fundo":
                        self.fundo = pygame.transform.smoothscale(img, (self.largura, self.altura))
                    elif key == "fred":
                        self.fred_base = self._scale_h(img, int(self.altura * 0.40))
                    elif key == "rosi":
                        self.rosi_base = self._scale_h(img, int(self.altura * 0.55))
                    elif key == "start":
                        self.start_base = self._scale_w(img, int(self.largura * 0.19))
                    elif key == "caixa":
                        self.caixa_base = self._scale_w(img, int(self.largura * 0.30))
                    elif key == "nomejogo":
                        # escala do logo/título (ajuste como preferir)
                        self.nomejogo_base = self._scale_w(img, int(self.largura * 0.50))
            except FileNotFoundError:
                # Em dev, se ainda não existe, ignora silenciosamente
                pass

    def draw(self, tela):
        # Recarrega se imagens mudaram
        self._carregar_assets()

        # Se algo ainda não carregou, desenha um fallback
        if self.fundo is None:
            tela.fill((10, 20, 40))
            return

        # Fundo
        tela.blit(self.fundo, (0, 0))

        # Tempo (para animações)
        t = (pygame.time.get_ticks() - self.t0) / 1000.0

        # Fred
        if self.fred_base:
            fred_bob = int(6 * math.sin(t * 2.0))
            fred_rot = 2.0 * math.sin(t * 1.2)
            fred_img = pygame.transform.rotozoom(self.fred_base, fred_rot, 1.0)
            self.fred_rect = fred_img.get_rect()
            self.fred_rect.topleft = (self.fred_anchor[0], self.fred_anchor[1] + fred_bob)
            tela.blit(fred_img, self.fred_rect)

        # Rosinha
        if self.rosi_base:
            rosi_bob = int(6 * math.sin(t * 2.0 + math.pi))
            rosi_rot = -2.0 * math.sin(t * 1.2 + 0.7)
            rosi_img = pygame.transform.rotozoom(self.rosi_base, rosi_rot, 1.0)
            self.rosi_rect = rosi_img.get_rect()
            self.rosi_rect.topleft = (self.rosi_anchor[0], self.rosi_anchor[1] + rosi_bob)
            tela.blit(rosi_img, self.rosi_rect)

        # START (pulso + hover)
        if self.start_base:
            pulse = 1.0 + 0.02 * math.sin(t * 5.0)
            start_img = pygame.transform.rotozoom(self.start_base, 0, pulse)
            self.start_rect = start_img.get_rect(center=self.start_anchor)

            if self.start_rect.collidepoint(pygame.mouse.get_pos()):
                start_img = pygame.transform.rotozoom(self.start_base, 0, pulse + 0.05)
                self.start_rect = start_img.get_rect(center=self.start_anchor)

            tela.blit(start_img, self.start_rect)

        # Caixa (APENAS a arte, sem texto)
        if self.caixa_base:
            self.caixa_rect = self.caixa_base.get_rect(midtop=self.caixa_anchor)
            tela.blit(self.caixa_base, self.caixa_rect)

        # Nome do jogo (arte do título)
        if self.nomejogo_base:
            self.nomejogo_rect = self.nomejogo_base.get_rect(midtop=self.nomejogo_anchor)
            tela.blit(self.nomejogo_base, self.nomejogo_rect)

        # (Removido) Dica "ENTER ou clique em START" em texto