"""Verifica os sentidos dos trajetos contra as setas do mapa de referência."""

import unittest

from config import FLUXOS


class SentidosDoMapa(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
