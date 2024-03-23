import pygame
import random

# INICALIZACAO
pygame.init()
# CONFIGURACAO DA TELA
LARGURA_TELA, ALTURA_TELA = 600, 400
FPS = 10
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), 0, 32)
relogio = pygame.time.Clock()

# DEFININDO PLACAR

placar = 0

# Criacao da surface para movimentos
area_movimento = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
area_movimento = area_movimento.convert()

# Constantes de cores
BRANCO = "white"
VERDE = "GREEN"
VERMELHO = "RED"
PRETO = "BLACK"

# Tamanho da Grade do Jogo
GRADE_TAMANHO = 20
GRADE_LARGURA = LARGURA_TELA // GRADE_TAMANHO
GRADE_ALTURA = ALTURA_TELA // GRADE_TAMANHO

# DIRECIONAIS
CIMA = (0, -1)
BAIXO = (0, 1)
ESQUERDA = (-1, 0)
DIREITA = (1, 0)


# --------------- INICIO CLASSE COBRA
class Cobra:
    def __init__(self, tela):
        self.tamanho = 1
        self.position = [
            ((LARGURA_TELA // 2, ALTURA_TELA // 2))
        ]
        self.direcao = random.choice([CIMA, BAIXO, DIREITA, ESQUERDA])
        self.color = VERDE
        self.tela = tela
    
    def pega_direcao_cobra(self):
        return self.position[0]
    
    def virar(self, direcao):
        if self.tamanho > 1 and (
            (direcao[0] * - 1, direcao[1] * - 1) == self.direcao
        ):
            return
        else:
            self.direcao = direcao
    
    def mover(self):
        position_atual = self.pega_direcao_cobra()            
        eixo_x, eixo_y = self.direcao
        nova_direcao = (
            ((position_atual[0] + (eixo_x * GRADE_TAMANHO)) % LARGURA_TELA),
            ((position_atual[1] + (eixo_y * GRADE_TAMANHO)) % ALTURA_TELA)
        )
        
        if len(self.position) > 2 and nova_direcao in self.position[2:]:
            quit()
        else:
            # INSERIND NOVO CORPO
            self.position.insert(0, nova_direcao)
            if len(self.position) > self.tamanho:
                self.position.pop()
    
    def controlar_teclas(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self.virar(CIMA)
        elif teclas[pygame.K_DOWN]:
            self.virar(BAIXO)
        elif teclas[pygame.K_RIGHT]:
            self.virar(DIREITA)
        elif teclas[pygame.K_LEFT]:
            self.virar(ESQUERDA)
        
    def desenhar(self, area_movimento):
        for pos in self.position:
            quadrado = pygame.Rect(
                (pos[0], pos[1]),
                (GRADE_TAMANHO, GRADE_TAMANHO)
                )
            pygame.draw.rect(area_movimento, self.color, quadrado)
            pygame.draw.rect(area_movimento, PRETO, quadrado, 1)
                
                
# ----------------- FIM CLASSE COBRA

# ----------------- INICIO CLASSE COMIDA
class Comida:
    def __init__(self, snake):
        self.position = (0,0)
        self.color = VERMELHO
        self.cobra = snake
        self.posicao_aleatoria()

# ----------------- FIM CLASSE COMIDA        
        
    def posicao_aleatoria(self):
        while True:
            # GERAR A POSICAO ALEATORIA DO MEU OBJETO COMIDA
            self.position = (
                random.randint(0, GRADE_LARGURA -1) * GRADE_TAMANHO,
                random.randint(0, GRADE_ALTURA -1) * GRADE_TAMANHO
            )
            # VERIFICAR SE A COMIDA NAO ESTA NO CORPO DA COBRA
            if self.position not in self.cobra.position:
                break
            
    def desenhar(self, area_movimento):
        quadrado = pygame.Rect((self.position[0], self.position[1]), (GRADE_TAMANHO, GRADE_TAMANHO))
        pygame.draw.rect(area_movimento, self.color, quadrado)
        pygame.draw.rect(area_movimento, PRETO, quadrado, 1)

cobra = Cobra(tela)
food = Comida(cobra)

# LOOP PRINCIPAL
while True:
        # EVENTOS
        # ------- inicio do for -------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
             
             
    cobra.controlar_teclas()
    cobra.mover()
                 
    if cobra.pega_direcao_cobra() == food.position:
        cobra.tamanho += 1
        food.posicao_aleatoria()
        placar += 1
                 
    area_movimento.fill(BRANCO)
    cobra.desenhar(area_movimento)
    food.desenhar(area_movimento)
    
    
    # ATUALIZACAO
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render(f"Placar: {placar}", True, PRETO)
    area_movimento.blit(texto, (10,10))
    
    tela.fill(BRANCO)
    
    # RENDERIZACAO
    tela.blit(area_movimento, (0, 0))
    pygame.display.update()
    relogio.tick(FPS)
