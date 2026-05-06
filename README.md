# <p align="center">🎱 Bingo 75 — Ultimate Pro Edition</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyQt5-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
</p>

---

## 📺 Demonstração em Alta Performance

<p align="center">
  <a href="https://github.com/LuizIwasaki/bing-app-complete/raw/main/images/funcionamento-bingo.webm">
    <img src="images/image.png" width="80%" alt="Clique para ver o vídeo" /><br>
    <b>▶️ CLIQUE PARA ASSISTIR A DEMONSTRAÇÃO</b>
  </a>
</p>

---

## ✨ Interface de Usuário Moderna

O Bingo 75 foi projetado com foco na **UX (User Experience)**, trazendo clareza visual e feedback imediato para cada ação do globo.

<div align="center">
  <table border="0">
    <tr>
      <td>
        <p align="center"><b>Dashboard Principal</b></p>
        <img src="images/image1.png" width="400px" alt="Interface Principal" />
      </td>
      <td>
        <p align="center"><b>Sorteio & Progressão</b></p>
        <img src="images/image2.png" width="400px" alt="Sorteio em Andamento" />
      </td>
    </tr>
  </table>
</div>

---

## 🚀 Funcionalidades

### 🔮 Globo de Sorteio Inteligente
- **Modo Manual**: Controle total sobre o ritmo da partida.
- **Modo Automático**: Delay customizável para sorteios dinâmicos sem intervenção.
- **Destaque de Última Bola**: O número atual brilha em destaque para facilitar o anúncio.

### 📊 Painel de Jogadores (Live Tracking)
- **Cards Dinâmicos**: Acompanhe o progresso de cada jogador através de mini-cartelas interativas.
- **Barra de Vitória**: Visualização percentual de quão perto cada jogador está do "BINGO!".
- **Check Automático**: O sistema valida cada bola sorteada contra todas as cartelas instantaneamente.

### 🏗️ Arquitetura e Persistência
- **Engine SQLAlchemy**: Gerenciamento de dados profissional com SQLite.
- **Histórico de Auditoria**: Registre cada partida, cada número na ordem exata e o histórico de campeões.

---

## 🛠️ Stack Tecnológica

- **Core**: Python 3.x
- **UI/UX**: PyQt5 (Custom StyleSheets)
- **Database**: SQLAlchemy + SQLite
- **Workflow**: Programação Assíncrona para UI fluida

---

## 📦 Guia Rápido de Instalação

### 1. Preparar Ambiente
```bash
git clone https://github.com/LuizIwasaki/bing-app-complete.git
cd bing-app-complete
```

### 2. Instalar Dependências
```bash
pip install PyQt5 SQLAlchemy
```

### 3. Let's Play!
```bash
python main.py
```

---

## 📝 Configuração de Jogadores (`CARTELAS.TXT`)

Adicione jogadores de forma simples e rápida seguindo o padrão:

```text
# Nome do Jogador: lista de 24 números separados por vírgula
Luiz Iwasaki: 1,12,23,34,45,56,67,2,13,24,35,46,57,68,3,14,25,36,47,58,69,4,15,26
```

---

<p align="center">
  Desenvolvido com dedicação por <a href="https://github.com/LuizIwasaki"><b>Luiz Iwasaki</b></a><br>
</p>
