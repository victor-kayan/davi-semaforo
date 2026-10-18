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
pedestres e ciclistas têm duas. A borda reforçada identifica o tipo na legenda. Cada sinal tem um
rótulo curto: V para automóveis, O para ônibus, P para pedestres e C
para ciclistas, seguido do número do sinal.
A caixa gira conforme a face visível: a base fica do lado de quem vê
a luz. A seta externa aponta o sentido do trânsito, da aproximação
até o sinal. A seta dentro da lâmpada do ônibus indica sua conversão
à esquerda. As travessias continuam com um indicador para ambos os lados.
Passe o mouse sobre um sinal para ver identificação, tipo e estado.

Há seis sinais convencionais (V1–V6), um de conversão à esquerda de ônibus
(O1), quatro travessias de pedestres (P1–P4) e duas de ciclistas (C1–C2).
Cada travessia tem um único indicador simplificado.

## Configurar

Edite `config.py` para substituir os dados fictícios:

- `REFERENCIA`: data e horário local exatos do início da primeira fase.
- `SINAIS`: identificação, tipo, posição em pixels do mapa original e direção
  da face visível. Para as travessias, a direção é `None`.
- `FASES`: duração em segundos, sinais verdes e sinais amarelos, nessa ordem.
  Todos os sinais omitidos em uma fase ficam vermelhos.
- `FLUXOS`: sinal que controla o trajeto, tipo de agente, velocidade em pixels
  por segundo, intervalo de chegada em segundos e pontos do caminho.
  O segundo ponto é a posição de parada, antes da travessia.

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

## Arquivos

- `main.py`: cálculo dos estados, desenho e controles.
- `config.py`: dados editáveis dos sinais e do ciclo.
- `transito.py`: movimento dos agentes, filas e desenhos do trânsito.
- `mapa.jpeg`: imagem de fundo.
- `requirements.txt`: dependência Pygame.
