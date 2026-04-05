"""
models.py - Modelos SQLAlchemy para o Bingo
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


class Partida(Base):
    """Representa uma partida de bingo"""
    __tablename__ = "partidas"

    id = Column(Integer, primary_key=True)
    data_inicio = Column(DateTime, default=datetime.now)
    data_fim = Column(DateTime, nullable=True)
    vencedor = Column(String(100), nullable=True)
    total_numeros_sorteados = Column(Integer, default=0)
    encerrada = Column(Boolean, default=False)

    numeros_sorteados = relationship("NumeroSorteado", back_populates="partida", cascade="all, delete-orphan")
    jogadores = relationship("Jogador", back_populates="partida", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Partida id={self.id} vencedor={self.vencedor}>"


class NumeroSorteado(Base):
    """Registra cada número sorteado numa partida"""
    __tablename__ = "numeros_sorteados"

    id = Column(Integer, primary_key=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"))
    numero = Column(Integer, nullable=False)
    ordem = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    partida = relationship("Partida", back_populates="numeros_sorteados")

    def __repr__(self):
        return f"<NumeroSorteado numero={self.numero} ordem={self.ordem}>"


class Jogador(Base):
    """Representa um jogador numa partida"""
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"))
    nome = Column(String(100), nullable=False)
    numeros_cartela = Column(Text, nullable=False)  # JSON dos 24 números
    venceu = Column(Boolean, default=False)

    partida = relationship("Partida", back_populates="jogadores")

    def __repr__(self):
        return f"<Jogador nome={self.nome}>"


def criar_banco():
    engine = create_engine("sqlite:///bingo.db", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session


def get_session():
    engine, Session = criar_banco()
    return Session()
