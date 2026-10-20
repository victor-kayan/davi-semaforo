"""Dados editáveis. Os tempos e grupos abaixo são fictícios."""

from datetime import datetime

# Horário local do início da primeira fase.
REFERENCIA = datetime(2026, 1, 1, 0, 0, 0)

# Identificação, tipo, posição em pixels do mapa original, face visível.
SINAIS = [
    ("V1", "auto", (580, 440), "direita"),
    ("V2", "auto", (515, 515), "baixo"),
    ("V3", "auto", (263, 368), "cima"),
    ("V4", "auto", (520, 1000), "baixo"),
    ("V5", "auto", (617, 847), "direita"),
    ("V6", "auto", (295, 960), "cima"),
    ("O1", "onibus", (449, 519), "baixo"),
    ("P1", "pedestre", (260, 322), None),
    ("P2", "pedestre", (490, 352), None),
    ("P3", "pedestre", (280, 895), None),
    ("P4", "pedestre", (490, 778), None),
    ("C1", "ciclista", (376, 351), None),
    ("C2", "ciclista", (377, 875), None),
]

# Faces no mapa: identificação original, posição e giro em graus.
# Faces repetidas compartilham o MESMO estado. Não são novos sinais.
# Posições aproximadas transferidas da imagem modelo para mapa.jpeg.
FACES = [
    ("V3", (230, 368), 180), ("V3", (297, 368), 180),
    ("V1", (580, 405), 90), ("V1", (580, 470), 90),
    ("O1", (449, 519), 188), ("V2", (515, 515), 8),
    ("V5", (617, 847), 270),
    ("V6", (266, 975), 205), ("V6", (324, 944), 205),
    ("V4", (495, 1008), 20), ("V4", (550, 990), 20),
    ("P1", (198, 297), 0), ("P1", (341, 304), 0),
    ("P2", (429, 315), 0), ("P2", (571, 312), 0),
    ("P3", (225, 879), 10), ("P3", (341, 823), 10),
    ("P4", (434, 777), 10), ("P4", (567, 710), 10),
    ("C1", (382, 361), 0), ("C1", (377, 550), 0),
    ("C2", (401, 893), 0), ("C2", (415, 1142), 0),
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
# pontos do trajeto. Para veículos, o SEGUNDO ponto é o início da faixa
# de pedestres; o programa recua a carroceria para manter a frente antes dela.
# Para pessoas e bicicletas, o segundo ponto é a posição de espera.
# As coordenadas usam a mesma imagem original que SINAIS.
FLUXOS = [
    # Cristóvão Gonçalves: direita -> esquerda, conforme as setas do mapa.
    ("V1", "carro", 55, 6, [(950, 445), (630, 445), (30, 445)]),
    # Faria Lima: pista direita sobe; pista esquerda desce na imagem.
    ("V2", "carro", 55, 7, [(495, 650), (490, 415), (475, 230)]),
    ("V3", "carro", 55, 6, [(270, 230), (275, 290), (290, 650)]),
    ("V4", "carro", 55, 7, [(535, 1230), (520, 850), (495, 650)]),
    # Baltazar Carrasco aproxima-se pela diagonal e entra na pista que sobe.
    ("V5", "carro", 50, 8, [(950, 600), (650, 815), (575, 875), (520, 850), (495, 650)]),
    ("V6", "carro", 55, 6, [(290, 650), (300, 820), (315, 1230)]),
    # Ônibus sobe pela faixa junto ao canteiro e vira à esquerda na Cristóvão.
    ("O1", "onibus", 40, 15, [(445, 650), (440, 525), (435, 455), (380, 430), (30, 430)]),
    ("P1", "pessoa", 20, 8, [(155, 315), (180, 315), (340, 335)]),
    ("P2", "pessoa", 20, 8, [(600, 365), (575, 365), (425, 345)]),
    ("P3", "pessoa", 20, 9, [(180, 945), (205, 930), (350, 850)]),
    ("P4", "pessoa", 20, 9, [(600, 730), (575, 745), (430, 810)]),
    ("C1", "bicicleta", 35, 10, [(375, 240), (375, 315), (375, 390)]),
    ("C2", "bicicleta", 35, 10, [(380, 980), (380, 910), (375, 820)]),
]
