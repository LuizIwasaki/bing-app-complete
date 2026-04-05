# 🎱 Bingo 75 — Sistema Completo em Python + PyQt5 + SQLAlchemy

## Estrutura do Projeto

```
bingo/
├── main.py            # Interface gráfica principal (mesa de bingo)
├── logica_bingo.py    # Lógica do jogo (sorteio, verificação, vencedor)
├── models.py          # Modelos SQLAlchemy (banco de dados SQLite)
├── CARTELAS.TXT       # Arquivo com os jogadores e seus 24 números
├── requirements.txt   # Dependências Python
└── README.md          # Este arquivo
```

## Instalação

```bash
pip install PyQt5 SQLAlchemy
```

## Como Executar

```bash
cd bingo
python main.py
```

O banco de dados `bingo.db` (SQLite) será criado automaticamente na primeira execução.

---

## Arquivo CARTELAS.TXT

### Formato:
```
# Comentários começam com #
Nome do Jogador: num1,num2,...,num24
```

### Regras:
- Cada jogador deve ter **exatamente 24 números**
- Os números devem estar entre **1 e 75**
- Não pode haver **números duplicados** na mesma cartela
- A posição FREE (centro da cartela 5×5) é gerenciada automaticamente

### Exemplo:
```
Maria Silva: 3,12,18,24,31,42,48,55,61,70,7,15,22,38,45,52,63,9,27,34,50,67,73,1
João Souza:  5,14,19,28,35,44,51,58,66,72,8,17,23,32,41,47,54,62,69,11,26,39,56,74
```

---

## Como Funciona

### Mesa de Bingo
- **75 bolinhas** organizadas em 5 colunas (B·I·N·G·O)
  - **B**: 1–15 (vermelho)
  - **I**: 16–30 (laranja)
  - **N**: 31–45 (verde)
  - **G**: 46–60 (azul)
  - **O**: 61–75 (roxo)
- Números sorteados ficam **iluminados** na cor da coluna
- O **último número** sorteado fica destacado em laranja brilhante

### Sorteio
- **Manual**: Clique em "SORTEAR NÚMERO" para sortear um por vez
- **Automático**: Ative "SORTEIO AUTOMÁTICO" para sortear a cada 2 segundos

### Jogadores
- Cada jogador tem um **card** mostrando sua cartela em miniatura (5×5)
- A **barra de progresso** mostra quantos números foram marcados
- Os números marcados ficam coloridos na mini-cartela

### Vencedor
- Quando um jogador acerta todos os 24 números, aparece uma janela anunciando o vencedor
- O card do vencedor fica destacado com bordas douradas

---

## Banco de Dados (SQLAlchemy + SQLite)

O arquivo `bingo.db` registra automaticamente:

| Tabela | Dados |
|--------|-------|
| `partidas` | Cada partida jogada, data de início/fim, vencedor |
| `numeros_sorteados` | Cada número sorteado e sua ordem |
| `jogadores` | Cada jogador, sua cartela e se venceu |

---

## Personalizando

### Adicionar mais jogadores
Basta adicionar linhas no `CARTELAS.TXT`.

### Alterar velocidade do sorteio automático
Em `main.py`, procure:
```python
self.timer_sorteio.start(2000)  # 2000ms = 2 segundos
```
Altere o valor em milissegundos.

### Gerar cartelas aleatórias
Adicione ao `logica_bingo.py`:
```python
import random
def gerar_cartela():
    return random.sample(range(1, 76), 24)
```
