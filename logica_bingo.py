"""
logica_bingo.py - Lógica central do jogo de Bingo
"""
import random
import json
from models import get_session, Partida, NumeroSorteado, Jogador
from datetime import datetime

def ler_cartelas(caminho="CARTELAS.TXT"):
    """
    Lê o arquivo CARTELAS.TXT e retorna lista de dicionários com nome e números.
    Formato esperado:
        Nome do Jogador: num1,num2,...,num24
    Linhas começando com # são comentários.
    """
    jogadores = []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#"):
                    continue
                if ":" not in linha:
                    continue
                nome, numeros_str = linha.split(":", 1)
                nome = nome.strip()
                try:
                    numeros = [int(n.strip()) for n in numeros_str.split(",") if n.strip()]
                    if len(numeros) != 24:
                        print(f"[AVISO] Jogador '{nome}' tem {len(numeros)} números (esperado: 24). Pulando.")
                        continue
                    invalidos = [n for n in numeros if n < 1 or n > 75]
                    if invalidos:
                        print(f"[AVISO] Jogador '{nome}' tem números inválidos: {invalidos}. Pulando.")
                        continue
                    if len(set(numeros)) != 24:
                        print(f"[AVISO] Jogador '{nome}' tem números duplicados. Pulando.")
                        continue
                    jogadores.append({"nome": nome, "numeros": numeros, "marcados": set()})
                except ValueError:
                    print(f"[AVISO] Erro ao ler números de '{nome}'. Pulando.")
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{caminho}' não encontrado.")
    return jogadores


class JogoBingo:
    """Gerencia o estado e a lógica de uma partida de Bingo"""

    def __init__(self, caminho_cartelas="CARTELAS.TXT"):
        self.jogadores = ler_cartelas(caminho_cartelas)
        self.numeros_disponiveis = list(range(1, 76))
        self.numeros_sorteados = []
        self.vencedor = None
        self.encerrado = False
        self.partida_db = None
        self.session = None
        self._iniciar_banco()

    def _iniciar_banco(self):
        """Registra a partida no banco de dados"""
        try:
            self.session = get_session()
            self.partida_db = Partida()
            self.session.add(self.partida_db)
            for j in self.jogadores:
                jogador_db = Jogador(
                    partida=self.partida_db,
                    nome=j["nome"],
                    numeros_cartela=json.dumps(j["numeros"])
                )
                self.session.add(jogador_db)
            self.session.commit()
        except Exception as e:
            print(f"[DB] Erro ao iniciar banco: {e}")

    def sortear(self):
        """
        Sorteia um número ainda não sorteado.
        Retorna o número sorteado, ou None se todos já foram sorteados.
        """
        if self.encerrado or not self.numeros_disponiveis:
            return None

        numero = random.choice(self.numeros_disponiveis)
        self.numeros_disponiveis.remove(numero)
        self.numeros_sorteados.append(numero)

        # Marca nas cartelas dos jogadores
        for j in self.jogadores:
            if numero in j["numeros"]:
                j["marcados"].add(numero)

        # Registra no banco
        try:
            ns = NumeroSorteado(
                partida=self.partida_db,
                numero=numero,
                ordem=len(self.numeros_sorteados)
            )
            self.session.add(ns)
            self.partida_db.total_numeros_sorteados = len(self.numeros_sorteados)
            self.session.commit()
        except Exception as e:
            print(f"[DB] Erro ao salvar número: {e}")

        # Verifica vencedor
        self._verificar_vencedor()
        return numero

    def _verificar_vencedor(self):
        """Verifica se algum jogador completou a cartela"""
        for j in self.jogadores:
            if len(j["marcados"]) == 24:
                self.vencedor = j["nome"]
                self.encerrado = True
                # Atualiza banco
                try:
                    self.partida_db.vencedor = self.vencedor
                    self.partida_db.encerrada = True
                    self.partida_db.data_fim = datetime.now()
                    # Marca jogador vencedor
                    for jdb in self.partida_db.jogadores:
                        if jdb.nome == self.vencedor:
                            jdb.venceu = True
                    self.session.commit()
                except Exception as e:
                    print(f"[DB] Erro ao registrar vencedor: {e}")
                break

    def progresso_jogadores(self):
        """
        Retorna lista de dicionários com progresso de cada jogador.
        """
        resultado = []
        for j in self.jogadores:
            resultado.append({
                "nome": j["nome"],
                "marcados": len(j["marcados"]),
                "total": 24,
                "porcentagem": int((len(j["marcados"]) / 24) * 100),
                "numeros": j["numeros"],
                "set_marcados": j["marcados"],
            })
        # Ordena por mais perto de ganhar
        resultado.sort(key=lambda x: x["marcados"], reverse=True)
        return resultado

    def numeros_por_coluna(self):
        """
        Retorna dict com as 5 colunas B,I,N,G,O e seus números (padrão bingo 75).
        B: 1-15, I: 16-30, N: 31-45, G: 46-60, O: 61-75
        """
        return {
            "B": list(range(1, 16)),
            "I": list(range(16, 31)),
            "N": list(range(31, 46)),
            "G": list(range(46, 61)),
            "O": list(range(61, 76)),
        }

    def encerrar(self):
        """Encerra a partida manualmente"""
        self.encerrado = True
        try:
            self.partida_db.encerrada = True
            self.session.commit()
        except Exception:
            pass
