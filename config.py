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
