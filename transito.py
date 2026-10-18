"""Fluxos ilustrativos: trajetos, filas e desenhos feitos com formas simples."""

import pygame

from config import FLUXOS


ESPACAMENTO = {"carro": 55, "onibus": 80, "pessoa": 25, "bicicleta": 40}


class Transito:
    def __init__(self):
        self.fluxos = []
        for sinal, tipo, velocidade, intervalo, pontos in FLUXOS:
            pontos = [pygame.Vector2(ponto) for ponto in pontos]
            comprimentos = [a.distance_to(b) for a, b in zip(pontos, pontos[1:])]
            self.fluxos.append({
                "sinal": sinal, "tipo": tipo, "velocidade": velocidade,
                "intervalo": intervalo, "pontos": pontos, "comprimentos": comprimentos,
                "parada": comprimentos[0], "total": sum(comprimentos),
                "agentes": [0.0], "espera": intervalo,
            })
        self.imagens = criar_imagens()

    def atualizar(self, segundos, estados):
        for fluxo in self.fluxos:
            agentes = fluxo["agentes"]  # Do primeiro da fila até o último.
            espaco = ESPACAMENTO[fluxo["tipo"]]
            frente = fluxo["total"] + espaco
            for indice, distancia in enumerate(agentes):
                destino = distancia + fluxo["velocidade"] * segundos
                if distancia <= fluxo["parada"] and estados[fluxo["sinal"]] != "verde":
                    destino = min(destino, fluxo["parada"])
                destino = min(destino, frente - espaco)
                agentes[indice] = max(distancia, destino)
                frente = agentes[indice]
            fluxo["agentes"] = [distancia for distancia in agentes if distancia < fluxo["total"]]

            fluxo["espera"] -= segundos
            if fluxo["espera"] <= 0:
                fila = fluxo["agentes"]
                if not fila or fila[-1] >= espaco:
                    fila.append(0.0)
                    fluxo["espera"] = fluxo["intervalo"]

    def desenhar(self, tela, origem, escala, topo_recorte):
        for fluxo in self.fluxos:
            for distancia in fluxo["agentes"]:
                posicao, direcao = posicao_no_trajeto(fluxo, distancia)
                centro = (round(origem[0] + posicao.x * escala),
                          round(origem[1] + (posicao.y - topo_recorte) * escala))
                # As imagens originais apontam para a direita.
                angulo = -pygame.Vector2(1, 0).angle_to(direcao)
                imagem = pygame.transform.rotate(self.imagens[fluxo["tipo"]], angulo)
                tela.blit(imagem, imagem.get_rect(center=centro))


def posicao_no_trajeto(fluxo, distancia):
    """Percorre os segmentos até encontrar a posição e a direção atuais."""
    for indice, comprimento in enumerate(fluxo["comprimentos"]):
        inicio = fluxo["pontos"][indice]
        fim = fluxo["pontos"][indice + 1]
        if distancia <= comprimento:
            return inicio.lerp(fim, distancia / comprimento), fim - inicio
        distancia -= comprimento
    return fluxo["pontos"][-1], fim - inicio


def criar_imagens():
    """Pequenas figuras vistas de cima, sem arquivos ou bibliotecas extras."""
    imagens = {}
    for tipo, largura, cor in [("carro", 20, (245, 245, 235)),
                                ("onibus", 32, (245, 180, 55))]:
        imagem = pygame.Surface((largura, 13), pygame.SRCALPHA)
        pygame.draw.rect(imagem, (30, 35, 40), (1, 0, largura - 2, 13), border_radius=3)
        pygame.draw.rect(imagem, cor, (0, 2, largura, 9), border_radius=3)
        pygame.draw.rect(imagem, (55, 95, 120), (largura - 7, 3, 4, 7), border_radius=1)
        pygame.draw.rect(imagem, (55, 95, 120), (3, 3, 3, 7), border_radius=1)
        imagens[tipo] = imagem

    pessoa = pygame.Surface((12, 12), pygame.SRCALPHA)
    pygame.draw.line(pessoa, (35, 50, 65), (3, 2), (3, 10), 3)
    pygame.draw.circle(pessoa, (55, 125, 225), (6, 6), 4)
    pygame.draw.circle(pessoa, (245, 205, 160), (8, 6), 3)
    imagens["pessoa"] = pessoa

    bicicleta = pygame.Surface((20, 13), pygame.SRCALPHA)
    pygame.draw.circle(bicicleta, (25, 30, 35), (4, 7), 3, width=1)
    pygame.draw.circle(bicicleta, (25, 30, 35), (16, 7), 3, width=1)
    pygame.draw.line(bicicleta, (125, 65, 170), (4, 7), (16, 7), 2)
    pygame.draw.line(bicicleta, (25, 30, 35), (15, 3), (15, 10), 2)
    pygame.draw.circle(bicicleta, (185, 100, 220), (9, 5), 3)
    pygame.draw.circle(bicicleta, (245, 205, 160), (12, 5), 2)
    imagens["bicicleta"] = bicicleta
    return imagens
