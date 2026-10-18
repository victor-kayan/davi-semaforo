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

    def texto(conteudo, posicao, cor=(225, 230, 238), pequeno=False):
        tela.blit((pequena if pequeno else fonte).render(conteudo, True, cor), posicao)

    while executando:
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
        tela.fill((25, 30, 40))
        texto("Davi Semáforo", (25, 12))
        texto("Dados fictícios", (largura - 112, 16), (150, 160, 175), pequeno=True)
        texto(f"Relógio real  {agora:%H:%M:%S}", (25, 39))
        texto(f"Simulação  {simulado:%H:%M:%S}", (largura - 210, 39))
        tela.blit(mapa, origem)

        detalhes = None
        mouse = pygame.mouse.get_pos()
        for identificacao, tipo, (x, y), direcao in SINAIS:
            x = origem[0] + round(x * escala)
            y = origem[1] + round((y - recorte.top) * escala)
            # Separa o par de sinais mais próximo sem alterar a configuração.
            if identificacao == "P2":
                y -= 5
            elif identificacao == "V2":
                y += 3
            nome, borda = TIPOS[tipo]
            cor = CORES[estados[identificacao]]
            pygame.draw.circle(tela, (25, 30, 40), (x, y), 12)
            pygame.draw.circle(tela, borda, (x, y), 12, width=2)
            if tipo == "onibus":
                pygame.draw.line(tela, cor, (x - 6, y), (x + 6, y), 3)
                pygame.draw.polygon(tela, cor, [(x - 7, y), (x, y - 5), (x, y + 5)])
            else:
                pygame.draw.circle(tela, cor, (x, y), 7)

            # Uma pequena marca indica o lado que vê a luz.
            if direcao:
                dx, dy = {"esquerda": (-1, 0), "cima": (0, -1), "baixo": (0, 1)}[direcao]
                pygame.draw.line(tela, borda, (x + dx * 12, y + dy * 12),
                                 (x + dx * 17, y + dy * 17), 3)
            if pygame.Rect(x - 14, y - 14, 28, 28).collidepoint(mouse):
                detalhes = f"{identificacao} · {nome} · {estados[identificacao]}"

        # Os nomes e estados aparecem apenas ao passar o mouse sobre um sinal.
        if detalhes:
            pygame.draw.rect(tela, (25, 30, 40), (20, altura - 153, 440, 26), border_radius=4)
            texto(detalhes, (25, altura - 148), pequeno=True)

        for indice, (nome, cor) in enumerate(TIPOS.values()):
            x = 30 + indice * 180
            pygame.draw.circle(tela, cor, (x, altura - 111), 4)
            texto(nome, (x + 11, altura - 120), pequeno=True)

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
        relogio.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()


