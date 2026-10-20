"""Verifica os sentidos dos trajetos contra as setas do mapa de referência."""

import unittest

from config import FACES, FLUXOS, ROTAS_ALTERNATIVAS, SINAIS
from transito import ESPACAMENTO, Transito, posicao_no_trajeto


class SentidosDoMapa(unittest.TestCase):
    def test_cristovao_cruza_as_duas_pistas_da_avenida(self):
        rotas = {sinal: pontos for sinal, _, _, _, pontos in FLUXOS}
        y_cruzamento = rotas["V1"][0][1]
        for sinal in ("V2", "V3"):
            encontros = []
            for a, b in zip(rotas[sinal], rotas[sinal][1:]):
                if min(a[1], b[1]) < y_cruzamento < max(a[1], b[1]):
                    proporcao = (y_cruzamento - a[1]) / (b[1] - a[1])
                    x = a[0] + proporcao * (b[0] - a[0])
                    if 30 < x < 950:
                        encontros.append(x)
            self.assertEqual(len(encontros), 1, sinal)

    def test_aproximacoes_dos_veiculos(self):
        # Vetores em coordenadas da imagem: y cresce para baixo.
        sentidos = {
            "V1": (-1, 0),  # Cristóvão Gonçalves: direita -> esquerda.
            "V2": (0, -1),  # Faria Lima, pista direita: sobe.
            "V3": (0, 1),   # Faria Lima, pista esquerda: desce.
            "V4": (0, -1),
            "V5": (-1, 1),  # Baltazar Carrasco: aproximação diagonal.
            "V6": (0, 1),
            "O1": (0, -1),  # Ônibus vem pela Faria Lima antes de virar.
        }
        for sinal, tipo, _, _, pontos in FLUXOS:
            if tipo not in ("carro", "onibus"):
                continue
            with self.subTest(sinal=sinal):
                dx = pontos[1][0] - pontos[0][0]
                dy = pontos[1][1] - pontos[0][1]
                sx, sy = sentidos[sinal]
                self.assertGreater(dx * sx + dy * sy, 0)
                if sinal in ("V2", "V4", "O1"):
                    self.assertGreater(pontos[0][0], 420)
                elif sinal in ("V3", "V6"):
                    self.assertLess(pontos[0][0], 340)

    def test_conversao_onibus(self):
        pontos = next(f[4] for f in FLUXOS if f[0] == "O1")
        self.assertLess(pontos[-1][0], 200)
        self.assertGreater(pontos[0][1], pontos[1][1])

    def test_baltazar_tem_duas_saidas_com_mesma_aproximacao(self):
        principal = next(f[4] for f in FLUXOS if f[0] == "V5")
        alternativa = ROTAS_ALTERNATIVAS["V5"][0]
        self.assertEqual(principal[:3], alternativa[:3])
        self.assertLess(principal[-1][1], principal[2][1])
        self.assertGreater(alternativa[-1][1], alternativa[2][1])

    def test_filas_e_paradas_atras_dos_sinais_da_avenida(self):
        vermelhos = {s[0]: "vermelho" for s in SINAIS}
        verdes = {s[0]: "verde" for s in SINAIS}
        for escala in (0.35, 0.5):
            transito = Transito(escala)
            for _ in range(900):
                transito.atualizar(0.1, vermelhos)
            for fluxo in transito.fluxos:
                fila = fluxo["agentes"]
                self.assertLessEqual(fila[0]["distancia"], fluxo["parada"])
                for a, b in zip(fila, fila[1:]):
                    self.assertGreaterEqual(a["distancia"] - b["distancia"],
                                            ESPACAMENTO[fluxo["tipo"]] - 0.001)
                sinal = fluxo["sinal"]
                if sinal in ("V2", "V3", "V4", "V6"):
                    posicao, direcao = posicao_no_trajeto(fluxo["rotas"][0], fila[0]["distancia"])
                    frente_y = posicao.y + direcao.normalize().y * 10 / escala
                    faces_y = [p[1] for nome, p, _ in FACES if nome == sinal]
                    if sinal in ("V2", "V4"):
                        self.assertGreater(frente_y, max(faces_y) + 15)
                    else:
                        self.assertLess(frente_y, min(faces_y) - 15)
            baltazar = next(f for f in transito.fluxos if f["sinal"] == "V5")
            self.assertEqual({a["rota"] for a in baltazar["agentes"]}, {0, 1})
            for _ in range(1200):
                transito.atualizar(0.1, verdes)
            for fluxo in transito.fluxos:
                for agente in fluxo["agentes"]:
                    self.assertLess(agente["distancia"], fluxo["rotas"][agente["rota"]]["total"])


if __name__ == "__main__":
    unittest.main()
