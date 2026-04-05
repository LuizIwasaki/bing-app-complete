import sys
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QFrame, QScrollArea,
    QProgressBar, QDialog, QMessageBox, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    pyqtSignal, QThread, QSize
)
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QPixmap, QPainter, QLinearGradient,
    QRadialGradient, QBrush, QPen, QFontDatabase
)

from logica_bingo import JogoBingo


# ─────────────────────────── PALETA DE CORES ───────────────────────────
COR_FUNDO       = "#0d1117"
COR_MESA        = "#1a1f2e"
COR_FELTRO      = "#0f3d2e"
COR_FELTRO_BORD = "#1a6b4e"
COR_GOLD        = "#f5c842"
COR_GOLD_DARK   = "#c9a227"
COR_BOLINHA_ON  = "#ff4d4d"
COR_BOLINHA_OFF = "#2a2f3e"
COR_BOLINHA_TXT = "#ffffff"
COR_HEADER_B    = "#e74c3c"
COR_HEADER_I    = "#e67e22"
COR_HEADER_N    = "#2ecc71"
COR_HEADER_G    = "#3498db"
COR_HEADER_O    = "#9b59b6"
COR_TEXTO       = "#e8e8e8"
COR_SUBTEXTO    = "#a0a8b8"
COR_CARD_BG     = "#1e2535"
COR_CARD_BORD   = "#2e3550"
COR_ULTIMO      = "#ff6b35"

CORES_COLUNAS = {
    "B": COR_HEADER_B,
    "I": COR_HEADER_I,
    "N": COR_HEADER_N,
    "G": COR_HEADER_G,
    "O": COR_HEADER_O,
}


def estilo_global():
    return f"""
        QMainWindow, QWidget {{
            background-color: {COR_FUNDO};
            color: {COR_TEXTO};
        }}
        QScrollArea {{
            border: none;
            background: transparent;
        }}
        QScrollBar:vertical {{
            background: #1a1f2e;
            width: 8px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: #3a4060;
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """


class BolinhaBingo(QPushButton):
    """Widget de bolinha individual do bingo (1-75)"""

    def __init__(self, numero, coluna, parent=None):
        super().__init__(str(numero), parent)
        self.numero = numero
        self.coluna = coluna
        self.sorteado = False
        self.ultimo = False
        self.setFixedSize(46, 46)
        self._atualizar_estilo()

    def marcar_sorteado(self, ultimo=False):
        self.sorteado = True
        self.ultimo = ultimo
        self._atualizar_estilo()

    def desmarcar_ultimo(self):
        self.ultimo = False
        self._atualizar_estilo()

    def _atualizar_estilo(self):
        cor_coluna = CORES_COLUNAS[self.coluna]
        if self.ultimo:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qradialgradient(cx:0.5, cy:0.5, radius:0.7,
                        fx:0.3, fy:0.3,
                        stop:0 #ffffff, stop:0.4 {COR_ULTIMO}, stop:1 #cc4400);
                    color: white;
                    border: 3px solid #ffffff;
                    border-radius: 23px;
                    font-size: 13px;
                    font-weight: 900;
                }}
            """)
        elif self.sorteado:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qradialgradient(cx:0.5, cy:0.5, radius:0.7,
                        fx:0.3, fy:0.3,
                        stop:0 #ffffff, stop:0.4 {cor_coluna}, stop:1 {cor_coluna}cc);
                    color: white;
                    border: 2px solid {cor_coluna};
                    border-radius: 23px;
                    font-size: 13px;
                    font-weight: 800;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {COR_BOLINHA_OFF};
                    color: #4a5068;
                    border: 1px solid #363d52;
                    border-radius: 23px;
                    font-size: 12px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background: #333848;
                    color: #6a7088;
                }}
            """)


class PainelJogador(QFrame):
    """Card de progresso de um jogador"""

    def __init__(self, nome, numeros, parent=None):
        super().__init__(parent)
        self.nome = nome
        self.numeros = set(numeros)
        self.marcados = set()
        self._construir()

    def _construir(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background: {COR_CARD_BG};
                border: 1px solid {COR_CARD_BORD};
                border-radius: 10px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # Nome
        self.lbl_nome = QLabel(self.nome)
        self.lbl_nome.setFont(QFont("Arial", 11, QFont.Bold))
        self.lbl_nome.setStyleSheet(f"color: {COR_GOLD}; background: transparent; border: none;")
        layout.addWidget(self.lbl_nome)

        # Barra de progresso
        self.barra = QProgressBar()
        self.barra.setRange(0, 24)
        self.barra.setValue(0)
        self.barra.setTextVisible(False)
        self.barra.setFixedHeight(8)
        self.barra.setStyleSheet(f"""
            QProgressBar {{
                background: #2a2f3e;
                border-radius: 4px;
                border: none;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COR_HEADER_G}, stop:1 {COR_GOLD});
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.barra)

        # Contagem
        self.lbl_contagem = QLabel("0 / 24  —  0%")
        self.lbl_contagem.setFont(QFont("Arial", 9))
        self.lbl_contagem.setStyleSheet(f"color: {COR_SUBTEXTO}; background: transparent; border: none;")
        layout.addWidget(self.lbl_contagem)

        self.grid_mini = QGridLayout()
        self.grid_mini.setSpacing(2)
        self.mini_labels = {}
        numeros_lista = sorted(self.numeros)

        posicoes = list(range(25))
        nos_numeros = numeros_lista[:12] + ["FREE"] + numeros_lista[12:]
        if len(nos_numeros) < 25:
            nos_numeros.append("?")

        for idx, val in enumerate(nos_numeros[:25]):
            row, col = divmod(idx, 5)
            if val == "FREE":
                lbl = QLabel("★")
                lbl.setFont(QFont("Arial", 7, QFont.Bold))
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(22, 22)
                lbl.setStyleSheet(f"""
                    background: {COR_GOLD};
                    color: #1a1f2e;
                    border-radius: 3px;
                    font-size: 10px;
                """)
            else:
                lbl = QLabel(str(val))
                lbl.setFont(QFont("Arial", 7))
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(22, 22)
                lbl.setStyleSheet("""
                    background: #252b3a;
                    color: #5a6080;
                    border-radius: 3px;
                """)
                self.mini_labels[val] = lbl
            self.grid_mini.addWidget(lbl, row, col)

        layout.addLayout(self.grid_mini)

    def atualizar(self, numeros_sorteados_set):
        self.marcados = self.numeros & numeros_sorteados_set
        qtd = len(self.marcados)
        self.barra.setValue(qtd)
        pct = int((qtd / 24) * 100)
        self.lbl_contagem.setText(f"{qtd} / 24  —  {pct}%")

        for num, lbl in self.mini_labels.items():
            if num in self.marcados:
                col = self._coluna_do_numero(num)
                cor = CORES_COLUNAS.get(col, COR_GOLD)
                lbl.setStyleSheet(f"""
                    background: {cor};
                    color: white;
                    border-radius: 3px;
                    font-weight: bold;
                """)
            else:
                lbl.setStyleSheet("""
                    background: #252b3a;
                    color: #5a6080;
                    border-radius: 3px;
                """)

    def marcar_vencedor(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2a2000, stop:1 #1a3a00);
                border: 2px solid {COR_GOLD};
                border-radius: 10px;
            }}
        """)
        self.lbl_nome.setStyleSheet(f"""
            color: {COR_GOLD};
            background: transparent;
            border: none;
            font-size: 13px;
        """)

    def _coluna_do_numero(self, num):
        if 1 <= num <= 15:   return "B"
        if 16 <= num <= 30:  return "I"
        if 31 <= num <= 45:  return "N"
        if 46 <= num <= 60:  return "G"
        return "O"


class DisplayUltimoNumero(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(160, 160)
        self._construir()

    def _construir(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)

        self.lbl_letra = QLabel("–")
        self.lbl_letra.setAlignment(Qt.AlignCenter)
        self.lbl_letra.setFont(QFont("Arial Black", 18, QFont.Black))
        self.lbl_letra.setStyleSheet(f"color: {COR_GOLD}; background: transparent;")

        self.lbl_numero = QLabel("?")
        self.lbl_numero.setAlignment(Qt.AlignCenter)
        self.lbl_numero.setFont(QFont("Arial Black", 52, QFont.Black))
        self.lbl_numero.setStyleSheet("color: white; background: transparent;")

        self.lbl_total = QLabel("Aguardando...")
        self.lbl_total.setAlignment(Qt.AlignCenter)
        self.lbl_total.setFont(QFont("Arial", 9))
        self.lbl_total.setStyleSheet(f"color: {COR_SUBTEXTO}; background: transparent;")

        layout.addWidget(self.lbl_letra)
        layout.addWidget(self.lbl_numero)
        layout.addWidget(self.lbl_total)

        self.setStyleSheet(f"""
            QFrame {{
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    fx:0.5, fy:0.5,
                    stop:0 #1e2535, stop:1 #0d1117);
                border: 2px solid {COR_CARD_BORD};
                border-radius: 80px;
            }}
        """)

    def _coluna_letra(self, num):
        if 1 <= num <= 15:   return "B"
        if 16 <= num <= 30:  return "I"
        if 31 <= num <= 45:  return "N"
        if 46 <= num <= 60:  return "G"
        return "O"

    def atualizar(self, numero, total_sorteados, total_disponiveis):
        letra = self._coluna_letra(numero)
        cor = CORES_COLUNAS[letra]
        self.lbl_letra.setText(letra)
        self.lbl_letra.setStyleSheet(f"color: {cor}; background: transparent;")
        self.lbl_numero.setText(str(numero))
        self.lbl_total.setText(f"Sorteado: {total_sorteados} de 75")
        self.setStyleSheet(f"""
            QFrame {{
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    fx:0.5, fy:0.5,
                    stop:0 {cor}33, stop:0.6 #1e2535, stop:1 #0d1117);
                border: 3px solid {cor};
                border-radius: 80px;
            }}
        """)


class DialogVencedor(QDialog):
    """Diálogo de anúncio do vencedor"""

    def __init__(self, nome, total_sorteados, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🏆 BINGO!")
        self.setModal(True)
        self.setFixedSize(480, 320)
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1000, stop:0.5 #1a2a00, stop:1 #0a1a10);
            }}
        """)
        self._construir(nome, total_sorteados)

    def _construir(self, nome, total_sorteados):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Troféu
        lbl_trofeu = QLabel("🏆")
        lbl_trofeu.setAlignment(Qt.AlignCenter)
        lbl_trofeu.setStyleSheet("font-size: 64px; background: transparent;")
        layout.addWidget(lbl_trofeu)

        # BINGO!
        lbl_bingo = QLabel("B  I  N  G  O  !")
        lbl_bingo.setAlignment(Qt.AlignCenter)
        lbl_bingo.setFont(QFont("Arial Black", 30, QFont.Black))
        lbl_bingo.setStyleSheet(f"color: {COR_GOLD}; background: transparent; letter-spacing: 8px;")
        layout.addWidget(lbl_bingo)

        # Nome do vencedor
        lbl_nome = QLabel(nome)
        lbl_nome.setAlignment(Qt.AlignCenter)
        lbl_nome.setFont(QFont("Arial", 22, QFont.Bold))
        lbl_nome.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(lbl_nome)

        # Estatística
        lbl_stat = QLabel(f"Completou a cartela em {total_sorteados} números sorteados!")
        lbl_stat.setAlignment(Qt.AlignCenter)
        lbl_stat.setFont(QFont("Arial", 11))
        lbl_stat.setStyleSheet(f"color: {COR_SUBTEXTO}; background: transparent;")
        layout.addWidget(lbl_stat)

        # Botão fechar
        btn = QPushButton("Fechar")
        btn.setFont(QFont("Arial", 12, QFont.Bold))
        btn.setFixedHeight(44)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COR_GOLD_DARK}, stop:1 {COR_GOLD});
                color: #1a1000;
                border: none;
                border-radius: 22px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {COR_GOLD};
            }}
        """)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)


class JanelaBingo(QMainWindow):
    """Janela principal da mesa de Bingo"""

    def __init__(self):
        super().__init__()
        self.jogo = None
        self.bolinhas = {}
        self.paineis_jogadores = {}
        self.ultimo_sorteado = None
        self.timer_sorteio = QTimer()
        self.timer_sorteio.timeout.connect(self._sortear_proximo)
        self._construir_ui()
        self._carregar_jogo()

    def _construir_ui(self):
        self.setWindowTitle("🎱 Mesa de Bingo — 75 Números")
        self.setMinimumSize(1200, 750)
        self.setStyleSheet(estilo_global())

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(16)

        # ── LADO ESQUERDO: Painel de controle + Jogadores ──
        lado_esq = QVBoxLayout()
        lado_esq.setSpacing(12)

        # Título
        lbl_titulo = QLabel("🎱 BINGO")
        lbl_titulo.setFont(QFont("Arial Black", 22, QFont.Black))
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet(f"color: {COR_GOLD}; letter-spacing: 6px;")
        lado_esq.addWidget(lbl_titulo)

        lbl_sub = QLabel("75 Números · Cartela 5×5")
        lbl_sub.setFont(QFont("Arial", 9))
        lbl_sub.setAlignment(Qt.AlignCenter)
        lbl_sub.setStyleSheet(f"color: {COR_SUBTEXTO};")
        lado_esq.addWidget(lbl_sub)

        # Display do último número
        self.display_numero = DisplayUltimoNumero()
        cont_display = QHBoxLayout()
        cont_display.setAlignment(Qt.AlignCenter)
        cont_display.addWidget(self.display_numero)
        lado_esq.addLayout(cont_display)

        # Botões de controle
        self.btn_sortear = QPushButton("▶  SORTEAR NÚMERO")
        self.btn_sortear.setFont(QFont("Arial", 11, QFont.Bold))
        self.btn_sortear.setFixedHeight(48)
        self.btn_sortear.setCursor(Qt.PointingHandCursor)
        self.btn_sortear.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #16a085, stop:1 #1abc9c);
                color: white;
                border: none;
                border-radius: 24px;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{ background: #1abc9c; }}
            QPushButton:pressed {{ background: #0e8a74; }}
            QPushButton:disabled {{ background: #2a2f3e; color: #4a5068; }}
        """)
        self.btn_sortear.clicked.connect(self._sortear_manual)
        lado_esq.addWidget(self.btn_sortear)

        self.btn_auto = QPushButton("⚡  SORTEIO AUTOMÁTICO")
        self.btn_auto.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_auto.setFixedHeight(40)
        self.btn_auto.setCursor(Qt.PointingHandCursor)
        self.btn_auto.setCheckable(True)
        self.btn_auto.setStyleSheet(f"""
            QPushButton {{
                background: #1e2535;
                color: {COR_SUBTEXTO};
                border: 1px solid {COR_CARD_BORD};
                border-radius: 20px;
                font-size: 10px;
            }}
            QPushButton:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7b2d8b, stop:1 #9b59b6);
                color: white;
                border: none;
            }}
            QPushButton:hover:!checked {{ background: #252b3a; }}
            QPushButton:disabled {{ background: #1a1f2e; color: #3a4060; border: none; }}
        """)
        self.btn_auto.toggled.connect(self._toggle_automatico)
        lado_esq.addWidget(self.btn_auto)

        btn_reiniciar = QPushButton("↺  Nova Partida")
        btn_reiniciar.setFont(QFont("Arial", 9))
        btn_reiniciar.setFixedHeight(34)
        btn_reiniciar.setCursor(Qt.PointingHandCursor)
        btn_reiniciar.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COR_SUBTEXTO};
                border: 1px solid #2e3550;
                border-radius: 17px;
            }}
            QPushButton:hover {{
                border-color: {COR_GOLD};
                color: {COR_GOLD};
            }}
        """)
        btn_reiniciar.clicked.connect(self._reiniciar)
        lado_esq.addWidget(btn_reiniciar)

        # Contador
        self.lbl_contador = QLabel("Sorteados: 0 / 75")
        self.lbl_contador.setAlignment(Qt.AlignCenter)
        self.lbl_contador.setFont(QFont("Arial", 10))
        self.lbl_contador.setStyleSheet(f"color: {COR_SUBTEXTO};")
        lado_esq.addWidget(self.lbl_contador)

        lado_esq.addSpacing(8)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {COR_CARD_BORD};")
        lado_esq.addWidget(sep)

        # Título jogadores
        lbl_jog = QLabel("JOGADORES")
        lbl_jog.setFont(QFont("Arial", 9, QFont.Bold))
        lbl_jog.setStyleSheet(f"color: {COR_SUBTEXTO}; letter-spacing: 3px;")
        lado_esq.addWidget(lbl_jog)

        # Scroll de jogadores
        scroll_jog = QScrollArea()
        scroll_jog.setWidgetResizable(True)
        scroll_jog.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.container_jogadores = QWidget()
        self.layout_jogadores = QVBoxLayout(self.container_jogadores)
        self.layout_jogadores.setSpacing(8)
        self.layout_jogadores.setContentsMargins(0, 0, 0, 0)
        self.layout_jogadores.addStretch()
        scroll_jog.setWidget(self.container_jogadores)
        scroll_jog.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.container_jogadores.setStyleSheet("background: transparent;")
        lado_esq.addWidget(scroll_jog, 1)

        # ── LADO DIREITO: Mesa de Bingo ──
        lado_dir = QVBoxLayout()
        lado_dir.setSpacing(10)

        lbl_mesa = QLabel("MESA DE BINGO")
        lbl_mesa.setFont(QFont("Arial", 10, QFont.Bold))
        lbl_mesa.setAlignment(Qt.AlignCenter)
        lbl_mesa.setStyleSheet(f"color: {COR_SUBTEXTO}; letter-spacing: 4px;")
        lado_dir.addWidget(lbl_mesa)

        # Frame da mesa (filtro verde)
        mesa_frame = QFrame()
        mesa_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f3d2e, stop:0.5 #0d3326, stop:1 #0b2d21);
                border: 3px solid {COR_FELTRO_BORD};
                border-radius: 16px;
            }}
        """)
        layout_mesa = QVBoxLayout(mesa_frame)
        layout_mesa.setContentsMargins(20, 16, 20, 16)
        layout_mesa.setSpacing(8)

        # Colunas BINGO
        self.grid_bingo = self._criar_grade_bingo()
        layout_mesa.addLayout(self.grid_bingo)

        lado_dir.addWidget(mesa_frame, 1)

        # Legenda de cores
        legenda = QHBoxLayout()
        legenda.setSpacing(16)
        legenda.setAlignment(Qt.AlignCenter)
        for col, cor in CORES_COLUNAS.items():
            faixa = f"  {col}: {col == 'B' and '1–15' or col == 'I' and '16–30' or col == 'N' and '31–45' or col == 'G' and '46–60' or '61–75'}  "
            lbl = QLabel(faixa)
            lbl.setFont(QFont("Arial", 8, QFont.Bold))
            lbl.setStyleSheet(f"""
                background: {cor}33;
                color: {cor};
                border: 1px solid {cor}66;
                border-radius: 6px;
                padding: 2px 6px;
            """)
            legenda.addWidget(lbl)
        lado_dir.addLayout(legenda)

        # Montar layout principal
        cont_esq = QWidget()
        cont_esq.setLayout(lado_esq)
        cont_esq.setFixedWidth(280)
        cont_esq.setStyleSheet("background: transparent;")

        cont_dir = QWidget()
        cont_dir.setLayout(lado_dir)
        cont_dir.setStyleSheet("background: transparent;")

        layout_principal.addWidget(cont_esq)
        layout_principal.addWidget(cont_dir, 1)

    def _criar_grade_bingo(self):
        """Cria o grid de 75 bolinhas organizadas em colunas B-I-N-G-O"""
        colunas_layout = QHBoxLayout()
        colunas_layout.setSpacing(10)

        colunas = {
            "B": range(1, 16),
            "I": range(16, 31),
            "N": range(31, 46),
            "G": range(46, 61),
            "O": range(61, 76),
        }

        for letra, nums in colunas.items():
            col_widget = QVBoxLayout()
            col_widget.setSpacing(5)
            col_widget.setAlignment(Qt.AlignTop)

            # Header da coluna
            lbl_col = QLabel(letra)
            lbl_col.setAlignment(Qt.AlignCenter)
            lbl_col.setFont(QFont("Arial Black", 22, QFont.Black))
            lbl_col.setFixedHeight(44)
            cor = CORES_COLUNAS[letra]
            lbl_col.setStyleSheet(f"""
                color: {cor};
                background: {cor}22;
                border-radius: 8px;
                border-bottom: 3px solid {cor};
            """)
            col_widget.addWidget(lbl_col)

            # Bolinhas
            for num in nums:
                bolinha = BolinhaBingo(num, letra)
                self.bolinhas[num] = bolinha
                col_widget.addWidget(bolinha, alignment=Qt.AlignHCenter)

            colunas_layout.addLayout(col_widget)

        return colunas_layout

    def _carregar_jogo(self):
        """Inicializa o jogo lendo CARTELAS.TXT"""
        self.jogo = JogoBingo("CARTELAS.TXT")
        if not self.jogo.jogadores:
            QMessageBox.warning(
                self, "Atenção",
                "Nenhum jogador carregado.\nVerifique o arquivo CARTELAS.TXT."
            )
            return
        self._popular_jogadores()

    def _popular_jogadores(self):
        """Cria os painéis de cada jogador"""
        # Limpa anteriores
        for i in reversed(range(self.layout_jogadores.count())):
            item = self.layout_jogadores.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        self.paineis_jogadores = {}
        for j in self.jogo.jogadores:
            painel = PainelJogador(j["nome"], j["numeros"])
            self.paineis_jogadores[j["nome"]] = painel
            self.layout_jogadores.insertWidget(
                self.layout_jogadores.count() - 1, painel
            )

    def _sortear_manual(self):
        self._executar_sorteio()

    def _toggle_automatico(self, ativo):
        if ativo:
            self.btn_sortear.setEnabled(False)
            self.timer_sorteio.start(2000)  # a cada 2 segundos
        else:
            self.btn_sortear.setEnabled(True)
            self.timer_sorteio.stop()

    def _sortear_proximo(self):
        self._executar_sorteio()

    def _executar_sorteio(self):
        if not self.jogo or self.jogo.encerrado:
            self.timer_sorteio.stop()
            self.btn_auto.setChecked(False)
            return

        # Desmarca o último
        if self.ultimo_sorteado is not None:
            self.bolinhas[self.ultimo_sorteado].desmarcar_ultimo()
            self.bolinhas[self.ultimo_sorteado].marcar_sorteado(ultimo=False)

        numero = self.jogo.sortear()
        if numero is None:
            self.timer_sorteio.stop()
            self.btn_auto.setChecked(False)
            self.btn_sortear.setEnabled(False)
            QMessageBox.information(self, "Fim de Jogo", "Todos os 75 números foram sorteados!")
            return

        self.ultimo_sorteado = numero

        # Atualiza bolinha na mesa
        self.bolinhas[numero].marcar_sorteado(ultimo=True)

        # Atualiza display
        total = len(self.jogo.numeros_sorteados)
        self.display_numero.atualizar(numero, total, 75 - total)
        self.lbl_contador.setText(f"Sorteados: {total} / 75")

        # Atualiza painéis de jogadores
        set_sorteados = set(self.jogo.numeros_sorteados)
        for nome, painel in self.paineis_jogadores.items():
            painel.atualizar(set_sorteados)

        # Verifica vencedor
        if self.jogo.vencedor:
            self.timer_sorteio.stop()
            self.btn_auto.setChecked(False)
            self.btn_sortear.setEnabled(False)
            self.btn_auto.setEnabled(False)

            # Marca painel do vencedor
            if self.jogo.vencedor in self.paineis_jogadores:
                self.paineis_jogadores[self.jogo.vencedor].marcar_vencedor()

            # Exibe diálogo
            QTimer.singleShot(400, lambda: self._anunciar_vencedor(self.jogo.vencedor, total))

    def _anunciar_vencedor(self, nome, total_sorteados):
        dlg = DialogVencedor(nome, total_sorteados, self)
        dlg.exec_()

    def _reiniciar(self):
        resposta = QMessageBox.question(
            self, "Nova Partida",
            "Deseja iniciar uma nova partida?\nO progresso atual será perdido.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            self.timer_sorteio.stop()
            self.btn_auto.setChecked(False)
            self.btn_sortear.setEnabled(True)
            self.btn_auto.setEnabled(True)
            self.ultimo_sorteado = None

            # Reseta bolinhas
            for bolinha in self.bolinhas.values():
                bolinha.sorteado = False
                bolinha.ultimo = False
                bolinha._atualizar_estilo()

            # Reseta display
            self.display_numero.lbl_letra.setText("–")
            self.display_numero.lbl_numero.setText("?")
            self.display_numero.lbl_total.setText("Aguardando...")
            self.display_numero.setStyleSheet(f"""
                QFrame {{
                    background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                        fx:0.5, fy:0.5,
                        stop:0 #1e2535, stop:1 #0d1117);
                    border: 2px solid {COR_CARD_BORD};
                    border-radius: 80px;
                }}
            """)
            self.lbl_contador.setText("Sorteados: 0 / 75")

            # Recarrega jogo
            self._carregar_jogo()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Bingo 75")

    # Tenta carregar fonte diferenciada
    janela = JanelaBingo()
    janela.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
