"""Confere as mudanças de cor nos horários transcritos da coleta."""

from datetime import datetime, timedelta
import unittest

from config import AVENIDA, LATERAIS, REFERENCIA
from main import DURACAO_CICLO, calcular_estados


class SincronizacaoDaColeta(unittest.TestCase):
    def test_grupos_conflitantes_nao_abrem_juntos(self):
        for decimo in range(1200):
            estados, _ = calcular_estados(REFERENCIA + timedelta(seconds=decimo / 10))
            for lateral in LATERAIS:
                for avenida in AVENIDA:
                    self.assertTrue(estados[lateral] == "vermelho" or
                                    estados[avenida] == "vermelho",
                                    f"Conflito em {decimo / 10}s: {lateral} e {avenida}")

    def test_horarios_configurados(self):
        registros = [
            (LATERAIS, "13:30:37", "verde", "vermelho"),
            (LATERAIS, "13:31:24", "amarelo", "verde"),
            (LATERAIS, "13:31:27", "vermelho", "amarelo"),
            (LATERAIS, "13:32:37", "verde", "vermelho"),
            (AVENIDA, "13:37:28", "verde", "vermelho"),
            (AVENIDA, "13:38:32", "amarelo", "verde"),
            (AVENIDA, "13:38:35", "vermelho", "amarelo"),
            (AVENIDA, "13:39:28", "verde", "vermelho"),
        ]
        for grupo, hora, depois, antes in registros:
            instante = datetime.fromisoformat(f"2026-10-20T{hora}")
            with self.subTest(hora=hora, grupo=grupo):
                atual, _ = calcular_estados(instante)
                anterior, _ = calcular_estados(instante - timedelta(microseconds=1))
                for sinal in grupo:
                    self.assertEqual(atual[sinal], depois)
                    self.assertEqual(anterior[sinal], antes)

    def test_duracoes_medidas(self):
        self.assertEqual(DURACAO_CICLO, 120)
        contagem = {sinal: {} for sinal in LATERAIS + AVENIDA}
        for segundo in range(120):
            estados, _ = calcular_estados(datetime(2026, 10, 20, 13, 30, 37) + timedelta(seconds=segundo))
            for sinal in contagem:
                cor = estados[sinal]
                contagem[sinal][cor] = contagem[sinal].get(cor, 0) + 1
        for sinal in LATERAIS:
            self.assertEqual(contagem[sinal], {"verde": 47, "amarelo": 3, "vermelho": 70})
        for sinal in AVENIDA:
            self.assertEqual(contagem[sinal], {"verde": 64, "amarelo": 3, "vermelho": 53})

    def test_travessias_inferidas(self):
        conflitos = {
            "P1": ["V3"], "P2": ["V2"],
            "P3": ["V6"], "P4": ["V4"],
            "C1": ["V1", "O1"], "C2": ["V5"],
        }
        verdes = {sinal: 0 for sinal in conflitos}
        for segundo in range(120):
            estados, _ = calcular_estados(REFERENCIA + timedelta(seconds=segundo))
            for travessia, veiculos in conflitos.items():
                if estados[travessia] == "verde":
                    verdes[travessia] += 1
                    for veiculo in veiculos:
                        self.assertEqual(estados[veiculo], "vermelho")
        self.assertTrue(all(duracao > 0 for duracao in verdes.values()))

    def test_onibus_acompanha_laterais_com_avenida_fechada(self):
        contagem = {"verde": 0, "amarelo": 0, "vermelho": 0}
        for segundo in range(120):
            estados, _ = calcular_estados(REFERENCIA + timedelta(seconds=segundo))
            contagem[estados["O1"]] += 1
            if estados["O1"] != "vermelho":
                for sinal in AVENIDA + ["C1"]:
                    self.assertEqual(estados[sinal], "vermelho")
            self.assertEqual(estados["O1"], estados["V1"])
        self.assertEqual(contagem, {"verde": 47, "amarelo": 3, "vermelho": 70})
        for segundo, esperado in [(0, "verde"), (47, "amarelo"), (50, "vermelho")]:
            estados, _ = calcular_estados(REFERENCIA + timedelta(seconds=segundo))
            self.assertEqual(estados["O1"], esperado)

    def test_repeticao_diaria_e_slider(self):
        instante = datetime(2026, 10, 20, 23, 59, 59)
        esperado, _ = calcular_estados(instante)
        for diferenca in (-10800, 10800, 86400):
            estados, _ = calcular_estados(instante + timedelta(seconds=diferenca))
            self.assertEqual(estados, esperado)


if __name__ == "__main__":
    unittest.main()
