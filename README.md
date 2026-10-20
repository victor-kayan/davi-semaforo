# Davi Semáforo

Simulação simples em Python e Pygame dos sinais de um cruzamento sobre o mapa.
**Durações dos automóveis baseadas na coleta real, com a defasagem da Faria
Lima corrigida na simulação.** Pedestres, ciclistas e ônibus usam tempos
inferidos. Os fluxos continuam ilustrativos.

## Executar

Requer Python 3.10 ou superior. No terminal, dentro da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python main.py
```

## Usar

- O topo mostra o relógio real e o horário usado na simulação.
- Arraste o slider para deslocar o horário entre −3 e +3 horas.
- Ao soltar o slider, o horário continua avançando com o deslocamento escolhido.
- Use **1x**, **2x** ou **3x** para acelerar o relógio simulado, os ciclos
  dos sinais e o movimento de todos os agentes juntos. O relógio real não muda.
- Voltar a **1x** mantém o horário alcançado, avançando em velocidade normal.
- Clique em **Voltar ao tempo real**, ou pressione **Home**, para zerar o
  deslocamento e restaurar **1x**.
- Feche a janela para sair.

A janela tem no máximo 720 pixels de altura e se ajusta a telas menores.
O mapa exibe apenas a região dos sinais, com as margens vazias recortadas.
Em 2x e 3x, o deslocamento em relação ao relógio real cresce automaticamente.
Ao alcançar +3 horas, a velocidade volta a 1x para respeitar o limite do slider.

Os sinais de veículos têm três lâmpadas, com apenas a atual acesa;
pedestres e ciclistas têm duas, com símbolos próprios. As caixas são
posicionadas e giradas conforme a imagem modelo, com faces repetidas nos
pontos indicados. Faces do mesmo sinal sempre mostram o mesmo estado.
A seta dentro da lâmpada do ônibus indica sua conversão à esquerda.
Passe o mouse sobre um sinal para ver identificação, tipo e estado.

Há seis sinais convencionais (V1–V6), um de conversão à esquerda de ônibus
(O1), quatro travessias de pedestres (P1–P4) e duas de ciclistas (C1–C2).
São 13 sinais lógicos, apresentados em 23 faces no mapa.

## Configurar

Edite `config.py` para ajustar os dados:

- `REFERENCIA`: data e horário local exatos do início da primeira fase.
- `SINAIS`: identificação, tipo, posição em pixels do mapa original e direção
  da referência original. Para as travessias, a direção é `None`.
- `FACES`: identificação do sinal, posição visual em pixels do mapa original
  e giro em graus. Altere esta lista para ajustar a disposição dos desenhos.
  Repetir uma identificação adiciona outra face do mesmo sinal.
- `FASES`: duração em segundos, sinais verdes e sinais amarelos, nessa ordem.
  Sinais omitidos ficam vermelhos.
- `ESTIMADOS`: identifica os sinais com tempos inferidos. Ao passar o mouse,
  a interface distingue “estimado” de “medido”.
- `AJUSTADOS`: sinais com durações medidas e horários deslocados. A interface
  identifica a correção de +15 s da avenida.
- `FLUXOS`: sinal que controla o trajeto, tipo de agente, velocidade em pixels
  por segundo, intervalo de chegada em segundos e pontos do caminho.
  Para carros e ônibus, o segundo ponto indica a linha de parada.
  Na Faria Lima ela fica atrás dos sinais, antes das faixas; nas laterais,
  fica antes da faixa. A parada considera metade do comprimento do veículo
  e uma margem adicional de 4 pixels na tela.
  Para pessoas e bicicletas, esse ponto indica a posição de espera.
- `ROTAS_ALTERNATIVAS`: outros destinos para o mesmo fluxo, com os mesmos
  pontos de aproximação e parada. Os agentes alternam entre os destinos.

Por exemplo, `(25, ["V2", "V3"], [])` deixa V2 e V3 verdes por 25 segundos,
com todos os demais vermelhos. `(2, [], [])` deixa todos vermelhos por 2 segundos.
A duração do ciclo é a soma das fases.

## Horários da coleta

| Grupo | Verde | Amarelo | Vermelho | Próximo verde |
| --- | --- | --- | --- | --- |
| V1 e V5: Cristóvão Gonçalves / Baltazar Carrasco | 13:30:37 | 13:31:24 | 13:31:27 | 13:32:37 |
| V2, V3, V4 e V6: Faria Lima | 13:37:13 | 13:38:17 | 13:38:20 | 13:39:13 |

Ambos os ciclos duram **120 segundos**. Nas laterais são 47 s de verde,
3 s de amarelo e 70 s de vermelho. Na avenida são 64 s de verde,
3 s de amarelo e 53 s de vermelho.

Os horários absolutos informados produzem **11 segundos de verde simultâneo**
entre os dois grupos a cada ciclo, mais 3 s de amarelo lateral com avenida
verde. Os trajetos confirmam o conflito: a Cristóvão Gonçalves cruza as duas
pistas da Faria Lima, e a saída da Baltazar converge com a avenida.

Para eliminar a sobreposição, todos os horários da Faria Lima foram
**atrasados em 15 segundos**, preservando as durações e os horários laterais:

| Grupo ajustado | Verde | Amarelo | Vermelho | Próximo verde |
| --- | --- | --- | --- | --- |
| Faria Lima | 13:37:28 | 13:38:32 | 13:38:35 | 13:39:28 |

A sequência agora é: 47 s laterais verdes, 3 s laterais amarelas, 1 s todos
vermelhos, 64 s avenida verde, 3 s avenida amarela e 2 s todos vermelhos.
O ciclo continua com 120 s. A correção da defasagem é uma hipótese autorizada
para a simulação, não uma nova medição do horário real. Os intervalos de
1 s e 2 s não são um cálculo de engenharia do tempo de desocupação.

A data da coleta não aparece na imagem. A referência usa uma data-base
às 13:30:37, no horário local do computador. Como 120 segundos divide
exatamente 24 horas, a fase é a mesma nesse horário em qualquer dia.
Isso pressupõe que o ciclo e sua sincronização se mantenham entre os dias,
sem reinícios do controlador ou programas diferentes por horário.

### Tempos inferidos

As travessias abrem quando os sinais dos veículos que cruzam estão vermelhos:

- P1 acompanha o vermelho de V3; P2, de V2.
- P3 acompanha o vermelho de V6; P4, de V4.
- C1 acompanha o vermelho de V1; C2, de V5.

O ônibus não foi monitorado. Após corrigir a sobreposição, restam apenas
3 segundos de todos os carros vermelhos; não cabe uma fase exclusiva de
ônibus preservando as durações medidas e o ciclo de 120 s. Por isso ele
acompanha as laterais (47 s verde, 3 s amarelo), com a avenida fechada.
Sua conversão converge no mesmo sentido da Cristóvão, e C1 fica fechado.
Os trajetos de P1 e P2 ficam acima da conversão, sem cruzá-la no modelo.
O espaçamento entre veículos de fluxos diferentes nessa convergência ainda
não é resolvido pelo modelo de filas.

Essas regras são hipóteses simplificadas, autorizadas para a simulação.
Não representam tempos medidos de pedestres, bicicletas ou ônibus e não
incluem vermelho piscante ou cálculo do tempo de desocupação das travessias.

Para verificar os instantes de mudança e as durações:

```powershell
.\.venv\Scripts\python -m unittest test_sincronizacao test_transito
```

O programa calcula `(horário simulado - referência) % duração do ciclo`.
Abrir o programa em outro momento não reinicia o ciclo. O relógio usado é o do
computador, no horário local; mantenha-o sincronizado para comparar com a rua.

## Trânsito animado

Carros, ônibus, pessoas e bicicletas percorrem trajetos fixos e fictícios.
Os desenhos são feitos no Pygame, sem imagens externas ou novas dependências.
Cada trajeto é uma sequência de segmentos entre os pontos de `FLUXOS`.

Os agentes param antes da travessia no vermelho ou amarelo, mantendo espaço
para quem está à frente. No verde, a fila avança. Quem já passou do ponto de
parada continua até concluir o trajeto, mesmo se o sinal mudar.
O ônibus tem um caminho com conversão à esquerda.

Na Baltazar Carrasco, os carros alternam entre subir e descer a Faria Lima
(divisão ilustrativa de 50% para cada destino). A aproximação tem uma única
fila compartilhada, sem duplicar a chegada de veículos. A saída que desce
atravessa o vão entre os canteiros; os tempos dos sinais são os mesmos para
os dois destinos.

Ao alterar o deslocamento pelo slider ou voltar ao tempo real, os fluxos
reiniciam. O slider muda o horário dos sinais; não reproduz um histórico de
veículos. Quantidades, velocidades e trajetos são ilustrativos. O modelo
mantém distância dentro de cada fila, sem resolver conflitos entre trajetos.

## Sentidos dos trajetos

Os trajetos seguem as setas da imagem de fundo, em coordenadas da tela:

| Sinal | Rua / movimento | Sentido na imagem |
| --- | --- | --- |
| V1 | Cristóvão Gonçalves | Direita para esquerda |
| V2 e V4 | Faria Lima, pista à direita do canteiro | De baixo para cima |
| V3 e V6 | Faria Lima, pista à esquerda do canteiro | De cima para baixo |
| V5 | Baltazar Carrasco | Diagonal da direita para baixo e esquerda |
| O1 | Faria Lima para Cristóvão Gonçalves | Sobe e vira à esquerda |

A revisão corrigiu trajetos que estavam invertidos e um fluxo horizontal
que atravessava a região do canteiro no trecho inferior. As faces dos sinais
continuam na disposição da imagem modelo; o giro do desenho não determina
o sentido dos agentes. Os pontos de `FLUXOS` determinam esse sentido.

Os nomes e conexões foram pesquisados em publicações oficiais. A Prefeitura
registra a sequência Faria Lima → Cristóvão Gonçalves → Chopin Tavares de Lima
em um [itinerário de ônibus de 2020](https://prefeitura.sp.gov.br/w/noticia/estacionamento-de-guindaste-altera-itinerario-de-cinco-linhas-na-regiao-de-pinheiros-1).
Essa referência histórica não confirma todas as conversões permitidas hoje.
A entrada ilustrativa da Baltazar Carrasco na Faria Lima e a faixa exclusiva
do ônibus ainda precisam de confirmação local; não há cadastro viário atual
integrado ao programa.

Para verificar os sentidos e a conversão do ônibus:

```powershell
.\.venv\Scripts\python -m unittest test_transito
```

## Arquivos

- `main.py`: cálculo dos estados, desenho e controles.
- `config.py`: dados editáveis dos sinais e do ciclo.
- `transito.py`: movimento dos agentes, filas e desenhos do trânsito.
- `test_transito.py`: regressão dos sentidos dos trajetos.
- `test_sincronizacao.py`: horários e durações registrados na coleta.
- `mapa.jpeg`: imagem de fundo.
- `requirements.txt`: dependência Pygame.
