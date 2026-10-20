"""Execute com python main.py. Os dados ficam em config.py."""

from datetime import datetime, timedelta
from pathlib import Path

import pygame

from config import AJUSTADOS, ESTIMADOS, FACES, FASES, REFERENCIA, SINAIS
from transito import Transito


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


def desenhar_semaforo(tela, posicao, tipo, estado, angulo):
    """Faces horizontais giradas sobre o mapa, conforme a imagem modelo."""
    lampadas = ["vermelho", "amarelo", "verde"]
    if tipo in ("pedestre", "ciclista"):
        lampadas = ["verde", "vermelho"]
    largura = len(lampadas) * 12 + 4
    desenho = pygame.Surface((largura, 24), pygame.SRCALPHA)
    if tipo == "pedestre":
        # Abas laterais representam as viseiras das duas faces.
        for x in (3, 15):
            pygame.draw.polygon(desenho, (38, 40, 42), [(x, 5), (x + 10, 0), (x + 10, 24), (x, 19)])
    caixa = pygame.Rect(0, 4, largura, 16)
    pygame.draw.rect(desenho, (23, 25, 28), caixa, border_radius=2)
    for indice, nome_cor in enumerate(lampadas):
        x, y = 8 + indice * 12, 12
        acesa = nome_cor == estado
        cor = CORES[nome_cor] if acesa else (56, 59, 62)
        pygame.draw.circle(desenho, (8, 10, 12), (x, y), 6)
        pygame.draw.circle(desenho, cor, (x, y), 5)
        simbolo = (15, 22, 20) if acesa else (100, 105, 108)
        if tipo == "onibus" and acesa:
            vetor = pygame.Vector2(-1, 0).rotate(angulo)
            centro = pygame.Vector2(x, y)
            lado = pygame.Vector2(-vetor.y, vetor.x)
            pygame.draw.line(desenho, simbolo, centro - vetor * 3, centro + vetor * 3, 2)
            pygame.draw.polygon(desenho, simbolo,
                                [centro + vetor * 4, centro + lado * 3, centro - lado * 3])
        elif tipo == "pedestre":
            pygame.draw.circle(desenho, simbolo, (x, y - 3), 1)
            pygame.draw.line(desenho, simbolo, (x, y - 1), (x, y + 2))
            pygame.draw.lines(desenho, simbolo, False, [(x - 2, y + 4), (x, y + 1), (x + 2, y + 4)])
            pygame.draw.line(desenho, simbolo, (x - 3, y), (x + 3, y))
        elif tipo == "ciclista":
            pygame.draw.circle(desenho, simbolo, (x - 3, y + 2), 2, 1)
            pygame.draw.circle(desenho, simbolo, (x + 3, y + 2), 2, 1)
            pygame.draw.lines(desenho, simbolo, False, [(x - 3, y + 2), (x, y - 2), (x + 3, y + 2), (x - 3, y + 2)])
            pygame.draw.circle(desenho, simbolo, (x + 1, y - 4), 1)
    if tipo in ("auto", "onibus"):
        desenho = pygame.transform.smoothscale(desenho, (30, 18))
    desenho = pygame.transform.rotate(desenho, angulo)
    area = desenho.get_rect(center=posicao)
    tela.blit(desenho, area)
    return area


def main():
    pygame.init()
    altura = min(720, pygame.display.Info().current_h - 80)
    largura = 760
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Davi Semáforo")
    fonte = pygame.font.SysFont("arial", 18)
    pequena = pygame.font.SysFont("arial", 14)
    relogio = pygame.time.Clock()

    mapa = pygame.image.load(str(Path(__file__).with_name("mapa.jpeg"))).convert()
    # Recorta apenas as margens sem sinais para aproveitar melhor a tela.
    recorte = pygame.Rect(0, 230, mapa.get_width(), 1030)
    mapa = mapa.subsurface(recorte)
    escala = min((largura - 40) / mapa.get_width(), (altura - 190) / mapa.get_height())
    tamanho = (round(mapa.get_width() * escala), round(mapa.get_height() * escala))
    mapa = pygame.transform.smoothscale(mapa, tamanho)
    origem = ((largura - tamanho[0]) // 2, 70)
    slider = pygame.Rect(30, altura - 49, largura - 250, 6)
    botao = pygame.Rect(largura - 185, altura - 66, 155, 36)
    deslocamento = 0
    arrastando = False
    executando = True
    transito = Transito(escala)
    deslocamento_anterior = 0

    def texto(conteudo, posicao, cor=(225, 230, 238), pequeno=False):
        tela.blit((pequena if pequeno else fonte).render(conteudo, True, cor), posicao)

    while executando:
        segundos = min(relogio.tick(30) / 1000, 0.1)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao.collidepoint(evento.pos):
                    deslocamento = 0
                elif slider.inflate(20, 30).collidepoint(evento.pos):
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
        estados, _ = calcular_estados(simulado)
        # Ao buscar outro horário, começa um novo fluxo naquele instante.
        if deslocamento != deslocamento_anterior:
            transito = Transito(escala)
            deslocamento_anterior = deslocamento
        transito.atualizar(segundos, estados)
        tela.fill((25, 30, 40))
        texto("Davi Semáforo", (25, 12))
        texto("Coleta + ajustes", (largura - 120, 16), (150, 160, 175), pequeno=True)
        texto(f"Relógio real  {agora:%H:%M:%S}", (25, 39))
        texto(f"Simulação  {simulado:%H:%M:%S}", (largura - 210, 39))
        tela.blit(mapa, origem)
        tela.set_clip(pygame.Rect(origem, tamanho))
        transito.desenhar(tela, origem, escala, recorte.top)
        tela.set_clip(None)

        detalhes = None
        mouse = pygame.mouse.get_pos()
        tipos_sinais = {identificacao: tipo for identificacao, tipo, _, _ in SINAIS}
        for identificacao, (x, y), angulo in FACES:
            tipo = tipos_sinais[identificacao]
            x = origem[0] + round(x * escala)
            y = origem[1] + round((y - recorte.top) * escala)
            nome, cor_tipo = TIPOS[tipo]
            area = desenhar_semaforo(tela, (x, y), tipo, estados[identificacao], angulo)
            if area.collidepoint(mouse):
                detalhes = f"{identificacao} | {nome} | {estados[identificacao]}"
                if identificacao in ESTIMADOS:
                    detalhes += " | estimado"
                elif identificacao in AJUSTADOS:
                    detalhes += " | medido, horário +15 s"
                else:
                    detalhes += " | medido"
                pygame.draw.rect(tela, cor_tipo, area.inflate(4, 4), width=1, border_radius=3)

        # Os detalhes aparecem apenas ao passar o mouse sobre um sinal.
        if detalhes:
            pygame.draw.rect(tela, (25, 30, 40), (20, altura - 153, 610, 26), border_radius=4)
            texto(detalhes, (25, altura - 148), pequeno=True)

        for indice, (tipo, (nome, cor)) in enumerate(TIPOS.items()):
            x = 30 + indice * 180
            prefixo = {"auto": "V", "onibus": "O", "pedestre": "P", "ciclista": "C"}[tipo]
            texto(f"{prefixo} · {nome}", (x, altura - 120), cor, pequeno=True)

        segundos = abs(deslocamento)
        sinal = "+" if deslocamento >= 0 else "−"
        diferenca = f"{sinal}{segundos // 3600:02}:{segundos % 3600 // 60:02}:{segundos % 60:02}"
        modo = "Tempo real" if deslocamento == 0 else f"Deslocamento {diferenca}"
        texto(modo, (30, altura - 88), pequeno=True)
        pygame.draw.rect(tela, (80, 90, 110), slider, border_radius=3)
        pygame.draw.line(tela, (160, 170, 185), (slider.centerx, slider.y - 4),
                         (slider.centerx, slider.bottom + 4))
        cursor = slider.left + round((deslocamento + LIMITE) / (2 * LIMITE) * slider.width)
        pygame.draw.circle(tela, (115, 175, 235), (cursor, slider.centery), 8)
        texto("−3 h", (slider.left, altura - 30), pequeno=True)
        texto("Agora", (slider.centerx - 18, altura - 30), pequeno=True)
        texto("+3 h", (slider.right - 28, altura - 30), pequeno=True)
        pygame.draw.rect(tela, (45, 60, 80), botao, border_radius=6)
        texto("Voltar ao tempo real", (botao.x + 19, botao.y + 9), pequeno=True)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


