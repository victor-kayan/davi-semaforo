"""Dados editáveis. Os tempos e grupos abaixo são fictícios."""

from datetime import datetime

# Horário local do início da primeira fase.
REFERENCIA = datetime(2026, 1, 1, 0, 0, 0)

# Identificação, tipo, posição em pixels do mapa original, face visível.
SINAIS = [
    ("V1", "auto", (374, 440), "esquerda"),
    ("V2", "auto", (500, 388), "cima"),
    ("V3", "auto", (260, 543), "baixo"),
    ("V4", "auto", (505, 832), "cima"),
    ("V5", "auto", (398, 1024), "esquerda"),
    ("V6", "auto", (305, 1140), "baixo"),
    ("O1", "onibus", (438, 400), "esquerda"),
    ("P1", "pedestre", (260, 322), None),
    ("P2", "pedestre", (490, 352), None),
    ("P3", "pedestre", (280, 895), None),
    ("P4", "pedestre", (490, 778), None),
    ("C1", "ciclista", (376, 351), None),
    ("C2", "ciclista", (377, 875), None),
]

# Cada fase: segundos, sinais verdes, sinais amarelos.
# Todos os sinais omitidos ficam vermelhos.
# Substitua também os grupos pelos movimentos observados na rua.
FASES = [
    (25, ["V2", "V3", "V4", "V6"], []),
    (5, [], ["V2", "V3", "V4", "V6"]),
    (2, [], []),
    (15, ["V1", "V5"], []),
    (5, [], ["V1", "V5"]),
    (2, [], []),
    (10, ["O1"], []),
    (3, [], ["O1"]),
    (2, [], []),
    (18, ["P1", "P2", "P3", "P4", "C1", "C2"], []),
    (3, [], []),
]

# Fluxos fictícios: sinal, tipo, velocidade (pixels/s), intervalo de chegada (s),
# pontos do trajeto. O SEGUNDO ponto é a parada antes da travessia.
# As coordenadas usam a mesma imagem original que SINAIS.
FLUXOS = [
    ("V1", "carro", 55, 6, [(30, 445), (330, 445), (950, 445)]),
    ("V2", "carro", 55, 7, [(515, 230), (515, 345), (520, 650)]),
    ("V3", "carro", 55, 6, [(285, 730), (280, 580), (270, 230)]),
    ("V4", "carro", 55, 7, [(535, 600), (535, 760), (550, 1230)]),
    ("V5", "carro", 50, 8, [(180, 1035), (355, 1035), (520, 1035), (800, 880)]),
    ("V6", "carro", 55, 6, [(310, 1230), (305, 1180), (295, 950)]),
    ("O1", "onibus", 40, 15, [(70, 405), (390, 405), (475, 405), (490, 340), (490, 230)]),
    ("P1", "pessoa", 20, 8, [(155, 315), (180, 315), (340, 335)]),
    ("P2", "pessoa", 20, 8, [(600, 365), (575, 365), (425, 345)]),
    ("P3", "pessoa", 20, 9, [(180, 945), (205, 930), (350, 850)]),
    ("P4", "pessoa", 20, 9, [(600, 730), (575, 745), (430, 810)]),
    ("C1", "bicicleta", 35, 10, [(375, 240), (375, 315), (375, 390)]),
    ("C2", "bicicleta", 35, 10, [(380, 980), (380, 910), (375, 820)]),
]
