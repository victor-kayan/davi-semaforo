"""Execute com python main.py. Os dados ficam em config.py."""

from datetime import datetime, timedelta
from pathlib import Path

import pygame

from config import FASES, REFERENCIA, SINAIS


CORES = {
    "vermelho": (235, 65, 65),
    "amarelo": (255, 202, 55),
    "verde": (62, 215, 115),
}
TIPOS = {
    "auto": ("Automóvel", (230, 100, 100)),
    "onibus": ("Ônibus / conversão", (255, 190, 80)),
    "pedestre": ("Pedestre", (90, 170, 255)),
    "ciclista": ("Ciclista", (215, 130, 245)),
}
DURACAO_CICLO = sum(duracao for duracao, _, _ in FASES)
LIMITE = 3 * 60 * 60  # Três horas em segundos, para cada lado do slider.


def calcular_estados(horario):
    """Calcula a fase pelo relógio, sem acumular atrasos da animação."""
    posicao = (horario - REFERENCIA).total_seconds() % DURACAO_CICLO
    for numero, (duracao, verdes, amarelos) in enumerate(FASES, start=1):
        if posicao < duracao:
            estados = {}
            for identificacao, _, _, _ in SINAIS:
                if identificacao in verdes:
                    estados[identificacao] = "verde"
                elif identificacao in amarelos:
                    estados[identificacao] = "amarelo"
                else:
                    estados[identificacao] = "vermelho"
            return estados, numero
        posicao -= duracao


def main():
    pygame.init()
    tela = pygame.display.set_mode((1000, 920))
    pygame.display.set_caption("Davi Semáforo")
    fonte = pygame.font.SysFont("arial", 18)
    pequena = pygame.font.SysFont("arial", 14)
    relogio = pygame.time.Clock()

    mapa = pygame.image.load(str(Path(__file__).with_name("mapa.jpeg"))).convert()
    escala = min(620 / mapa.get_width(), 700 / mapa.get_height())
    tamanho = (round(mapa.get_width() * escala), round(mapa.get_height() * escala))
    mapa = pygame.transform.smoothscale(mapa, tamanho)
    origem = (int((640 - tamanho[0]) / 2), 105)
    slider = pygame.Rect(100, 851, 620, 8)
    botao = pygame.Rect(760, 826, 210, 42)
    deslocamento = 0
    arrastando = False
    executando = True

    def texto(conteudo, posicao, cor=(235, 238, 245), pequeno=False):
        tela.blit((pequena if pequeno else fonte).render(conteudo, True, cor), posicao)

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao.collidepoint(evento.pos):
                    deslocamento = 0
                elif slider.inflate(24, 32).collidepoint(evento.pos):
                    arrastando = True
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                arrastando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_HOME:
                deslocamento = 0

        if arrastando:
            proporcao = (pygame.mouse.get_pos()[0] - slider.left) / slider.width
            proporcao = max(0, min(1, proporcao))
            deslocamento = round((proporcao * 2 - 1) * LIMITE)

        agora = datetime.now()
        simulado = agora + timedelta(seconds=deslocamento)
        estados, fase = calcular_estados(simulado)
        tela.fill((25, 30, 40))
        texto("Davi Semáforo — dados fictícios", (25, 15))
        texto(f"Relógio real: {agora:%d/%m/%Y %H:%M:%S}", (25, 45))
        texto(f"Horário simulado: {simulado:%d/%m/%Y %H:%M:%S}", (25, 73))
        tela.blit(mapa, origem)

        texto("Sinais", (665, 110))
        texto(f"Fase {fase} / {len(FASES)} | ciclo de {DURACAO_CICLO}s", (665, 141))
        for indice, (identificacao, tipo, (x, y), direcao) in enumerate(SINAIS):
            x = origem[0] + round(x * escala)
            y = origem[1] + round(y * escala)
            # Afasta os indicadores próximos e liga-os ao ponto original.
            ajustes = {"P2": (15, -32), "V2": (20, 12), "O1": (4, 0), "P4": (-20, -18)}
            ajuste_x, ajuste_y = ajustes.get(identificacao, (0, 0))
            pygame.draw.line(tela, (70, 75, 85), (x, y), (x + ajuste_x, y + ajuste_y), 1)
            x += ajuste_x
            y += ajuste_y
            nome, borda = TIPOS[tipo]
            cor = CORES[estados[identificacao]]

            # A luz mostra o estado; a borda identifica o tipo.
            caixa = pygame.Rect(x - 13, y - 19, 26, 38)
            pygame.draw.rect(tela, (25, 30, 40), caixa, border_radius=5)
            pygame.draw.rect(tela, borda, caixa, width=2, border_radius=5)
            if tipo == "onibus":
                pygame.draw.line(tela, cor, (x - 7, y - 5), (x + 7, y - 5), 3)
                pygame.draw.polygon(tela, cor, [(x - 8, y - 5), (x, y - 11), (x, y + 1)])
            else:
                pygame.draw.circle(tela, cor, (x, y - 5), 7)
            texto(identificacao, (x - 10, y + 4), pequeno=True)

            # A seta externa aponta para o lado que vê a luz.
            if direcao:
                dx, dy = {"esquerda": (-1, 0), "cima": (0, -1), "baixo": (0, 1)}[direcao]
                inicio = (x + dx * 21, y + dy * 25)
                ponta = (x + dx * 32, y + dy * 36)
                pygame.draw.line(tela, borda, inicio, ponta, 2)
                pygame.draw.polygon(tela, borda, [
                    ponta,
                    (ponta[0] - dx * 6 + dy * 4, ponta[1] - dy * 6 - dx * 4),
                    (ponta[0] - dx * 6 - dy * 4, ponta[1] - dy * 6 + dx * 4),
                ])

            linha = 183 + indice * 40
            pygame.draw.circle(tela, cor, (675, linha + 9), 6)
            texto(f"{identificacao}  {nome}", (690, linha), borda)
            texto(estados[identificacao], (690, linha + 19), pequeno=True)

        texto("Setas: lado que vê a luz", (665, 732), pequeno=True)
        texto("O1: conversão à esquerda de ônibus", (665, 754), pequeno=True)
        texto("Posições e orientações aproximadas", (665, 776), pequeno=True)

        segundos = abs(deslocamento)
        sinal = "+" if deslocamento >= 0 else "−"
        diferenca = f"{sinal}{segundos // 3600:02}:{segundos % 3600 // 60:02}:{segundos % 60:02}"
        modo = "TEMPO REAL" if deslocamento == 0 else f"Deslocamento: {diferenca}"
        texto(modo, (100, 815))
        pygame.draw.rect(tela, (105, 115, 135), slider, border_radius=4)
        centro = slider.centerx
        pygame.draw.line(tela, (235, 238, 245), (centro, 843), (centro, 867), 2)
        cursor = slider.left + round((deslocamento + LIMITE) / (2 * LIMITE) * slider.width)
        pygame.draw.circle(tela, (90, 170, 255), (cursor, slider.centery), 11)
        texto("−3 horas", (100, 877), pequeno=True)
        texto("Agora", (centro - 19, 877), pequeno=True)
        texto("+3 horas", (665, 877), pequeno=True)
        pygame.draw.rect(tela, (55, 80, 115), botao, border_radius=6)
        texto("Voltar ao tempo real", (botao.x + 23, botao.y + 10))
        texto("Atalho: Home", (805, 878), pequeno=True)

        pygame.display.flip()
        relogio.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
