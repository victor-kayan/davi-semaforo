# Davi Semáforo

Simulação simples em Python e Pygame dos sinais de um cruzamento sobre o mapa.
**Os tempos e grupos atuais são fictícios.**

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
- Clique em **Voltar ao tempo real**, ou pressione **Home**, para zerá-lo.
- Feche a janela para sair.

A janela tem no máximo 720 pixels de altura e se ajusta a telas menores.
O mapa exibe apenas a região dos sinais, com as margens vazias recortadas.

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

Edite `config.py` para substituir os dados fictícios:

- `REFERENCIA`: data e horário local exatos do início da primeira fase.
- `SINAIS`: identificação, tipo, posição em pixels do mapa original e direção
  da referência original. Para as travessias, a direção é `None`.
- `FACES`: identificação do sinal, posição visual em pixels do mapa original
  e giro em graus. Altere esta lista para ajustar a disposição dos desenhos.
  Repetir uma identificação adiciona outra face do mesmo sinal.
- `FASES`: duração em segundos, sinais verdes e sinais amarelos, nessa ordem.
  Todos os sinais omitidos em uma fase ficam vermelhos.
- `FLUXOS`: sinal que controla o trajeto, tipo de agente, velocidade em pixels
  por segundo, intervalo de chegada em segundos e pontos do caminho.
  Para carros e ônibus, o segundo ponto indica a borda de entrada da faixa
  de pedestres. A parada considera metade do comprimento do veículo e uma
  margem de 4 pixels na tela, deixando sua frente antes da faixa.
  Para pessoas e bicicletas, esse ponto indica a posição de espera.

Por exemplo, `(25, ["V2", "V3"], [])` deixa V2 e V3 verdes por 25 segundos,
com todos os demais vermelhos. `(2, [], [])` deixa todos vermelhos por 2 segundos.
A duração do ciclo é a soma das fases.

Os grupos fictícios não foram validados contra os movimentos reais do cruzamento.
Ao coletar os dados, substitua também os grupos de sinais que mudam juntos.

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
- `mapa.jpeg`: imagem de fundo.
- `requirements.txt`: dependência Pygame.
