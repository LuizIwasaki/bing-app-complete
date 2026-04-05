# 🎱 Bingo 75 — Sistema Profissional em Python

![Capa do Bingo](images/image.png)

Um sistema completo de Bingo de 75 bolas, desenvolvido com **Python**, **PyQt5** e **SQLAlchemy**. O projeto oferece uma experiência visual moderna e funcional para gerenciar partidas de bingo com múltiplos jogadores.

---

## 📸 Demonstração Visual

### Interface Principal e Mesa de Sorteio
O sistema apresenta uma mesa organizada com as 75 bolas, destacando cada coluna (B-I-N-G-O) com cores específicas e facilitando a visualização dos números já sorteados.

<div align="center">
  <img src="images/image1.png" width="45%" alt="Interface Principal" />
  <img src="images/image2.png" width="45%" alt="Sorteio em Andamento" />
</div>

### 📽️ Funcionamento em Vídeo
Confira o app em ação (Sorteio manual e automático):
[Clique aqui para ver o vídeo](https://github.com/LuizIwasaki/bing-app-complete/raw/main/images/funcionamento-bingo.webm)

---

## 🚀 Funcionalidades principais

- **Sorteio Inteligente**: Escolha entre o sorteio manual (um a um) ou o modo automático com tempo configurável.
- **Mesa de Bingo Cromática**: Bolas organizadas por cores (Vermelho, Laranja, Verde, Azul e Roxo) para rápida identificação.
- **Painel de Jogadores Dinâmico**: Cada jogador tem um card individual que mostra:
  - Mini-cartela 5x5 atualizada em tempo real.
  - Barra de progresso indicando quão perto o jogador está de completar o bingo.
- **Persistência de Dados**: Todas as partidas, jogadores e números sorteados são salvos automaticamente no banco de dados SQLite (`bingo.db`).
- **Identificação de Vencedor**: O sistema detecta automaticamente quando uma cartela é completada e destaca o vencedor visualmente.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**: Linguagem base.
- **PyQt5**: Interface gráfica avançada e responsiva.
- **SQLAlchemy**: ORM para gerenciamento robusto do banco de dados SQLite.

---

## 📦 Como Instalar e Executar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/LuizIwasaki/bing-app-complete.git
   cd bing-app-complete
   ```

2. **Instale as dependências**:
   ```bash
   pip install PyQt5 SQLAlchemy
   ```

3. **Execute o projeto**:
   ```bash
   python main.py
   ```

---

## 📄 Arquivo CARTELAS.TXT

O sistema carrega os participantes a partir deste arquivo. 

**Formato:**
```text
Nome do Jogador: num1,num2,num3...num24
```
*Observação: A posição central (FREE) é gerenciada automaticamente pelo sistema.*

---

<p align="center">Desenvolvido por <a href="https://github.com/LuizIwasaki">LuizIwasaki</a></p>
