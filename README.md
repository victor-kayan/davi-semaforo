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

Cada indicador mostra uma luz com a cor atual. A borda identifica o tipo,
conforme a legenda abaixo do mapa. Passe o mouse sobre um sinal para ver
sua identificação, tipo e estado. A pequena marca na borda indica o lado
que vê a luz; o sinal de ônibus usa uma seta luminosa à esquerda.

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

Por exemplo, `(25, ["V2", "V3"], [])` deixa V2 e V3 verdes por 25 segundos,
com todos os demais vermelhos. `(2, [], [])` deixa todos vermelhos por 2 segundos.
A duração do ciclo é a soma das fases.

Os grupos fictícios não foram validados contra os movimentos reais do cruzamento.
Ao coletar os dados, substitua também os grupos de sinais que mudam juntos.

O programa calcula `(horário simulado - referência) % duração do ciclo`.
Abrir o programa em outro momento não reinicia o ciclo. O relógio usado é o do
computador, no horário local; mantenha-o sincronizado para comparar com a rua.

## Arquivos

- `main.py`: cálculo dos estados, desenho e controles.
- `config.py`: dados editáveis dos sinais e do ciclo.
- `mapa.jpeg`: imagem de fundo.
- `requirements.txt`: dependência Pygame.
