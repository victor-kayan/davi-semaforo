"""Durações medidas; defasagem da avenida ajustada para eliminar conflitos."""

from datetime import datetime

# Referência local: abertura das ruas laterais registrada às 13:30:37.
# A data da coleta não foi informada. Como 120 s divide um dia inteiro,
# usar uma data-base preserva a mesma fase em cada horário de todos os dias.
REFERENCIA = datetime(2026, 1, 1, 13, 30, 37)

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

# Coleta nas ruas laterais: V1 (Cristóvão) e V5 (Baltazar).
# Verde 13:30:37; amarelo 13:31:24; vermelho 13:31:27; verde 13:32:37.
LATERAIS = ["V1", "V5"]

# Coleta na Faria Lima: verde 13:37:13; amarelo 13:38:17;
# vermelho 13:38:20; verde 13:39:13.
AVENIDA = ["V2", "V3", "V4", "V6"]
# Correção inferida: +15 s em TODOS os instantes da avenida.
# Verde 13:37:28; amarelo 13:38:32; vermelho 13:38:35; verde 13:39:28.
AJUSTADOS = AVENIDA

# Tempos inferidos, não medidos: travessias e conversão exclusiva do ônibus.
ESTIMADOS = ["O1", "P1", "P2", "P3", "P4", "C1", "C2"]
PEDESTRES = ["P1", "P2", "P3", "P4"]

# Cada fase: segundos, sinais verdes, sinais amarelos.
# A avenida abre 51 s após a referência: 47 s laterais verdes + 3 s amarelas
# + 1 s todos vermelhos. Seus 64 s verdes + 3 s amarelos deixam 2 s finais.
# Mantém as durações da coleta e 120 s de ciclo, sem liberações conflitantes.
# Pedestres cruzam a avenida no vermelho dela; ciclistas cruzam as laterais
# no vermelho delas. O ônibus acompanha as laterais, convergindo para o mesmo
# sentido da Cristóvão, com os carros da avenida fechados. É uma estimativa.
# Não há tempo para uma fase exclusiva adicional de ônibus neste ciclo.
FASES = [
    (47, LATERAIS + ["O1"] + PEDESTRES, []),
    (3, PEDESTRES, LATERAIS + ["O1"]),
    (1, PEDESTRES + ["C1", "C2"], []),
    (64, AVENIDA + ["C1", "C2"], []),
    (3, ["C1", "C2"], AVENIDA),
    (2, PEDESTRES + ["C1", "C2"], []),
]

# Fluxos fictícios: sinal, tipo, velocidade (pixels/s), intervalo de chegada (s),
# pontos do trajeto. Para veículos, o SEGUNDO ponto é a linha de parada.
# Na Faria Lima ela fica antes do sinal; nas laterais, antes da faixa.
# Para pessoas e bicicletas, o segundo ponto é a posição de espera.
# As coordenadas usam a mesma imagem original que SINAIS.
FLUXOS = [
    # Cristóvão Gonçalves: direita -> esquerda, conforme as setas do mapa.
    ("V1", "carro", 55, 6, [(950, 445), (630, 445), (30, 445)]),
    # Faria Lima: pista direita sobe; pista esquerda desce na imagem.
    ("V2", "carro", 55, 7, [(495, 650), (492, 550), (490, 415), (475, 230)]),
    ("V3", "carro", 55, 6, [(270, 230), (275, 290), (290, 650)]),
    ("V4", "carro", 55, 7, [(535, 1230), (526, 1040), (520, 850), (495, 650)]),
    # Baltazar: mesma fila de entrada, alternando os dois destinos abaixo.
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

# Saídas alternativas após a MESMA aproximação e linha de parada.
# Os carros alternam entre o trajeto principal e este: metade sobe, metade desce.
# A saída que desce cruza o vão entre os canteiros, sem cortar a área verde.
ROTAS_ALTERNATIVAS = {
    "V5": [[(950, 600), (650, 815), (575, 875), (550, 970),
             (440, 1040), (340, 1045), (315, 1100), (320, 1230)]],
}
