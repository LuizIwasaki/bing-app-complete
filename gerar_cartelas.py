"""
gerar_cartelas.py - Gera cartelas aleatórias válidas para o CARTELAS.TXT
Execute este script para criar novos jogadores automaticamente.

Uso:
    python gerar_cartelas.py

Ou com argumentos:
    python gerar_cartelas.py --jogadores 10 --saida CARTELAS.TXT
"""
import random
import argparse


NOMES_EXEMPLO = [
    "Alice Ferreira", "Bruno Carvalho", "Carla Nascimento",
    "Daniel Oliveira", "Eduarda Martins", "Felipe Alves",
    "Gabriela Souza", "Henrique Lima", "Isabela Costa",
    "Jorge Pereira", "Kamila Santos", "Leonardo Rocha",
    "Mariana Silva", "Nicolas Gomes", "Olívia Ribeiro",
    "Paulo Mendes", "Quezia Dias", "Rafael Cunha",
    "Sabrina Nunes", "Thiago Barbosa",
]


def gerar_cartela(nome):
    """Gera 24 números aleatórios únicos entre 1 e 75"""
    numeros = random.sample(range(1, 76), 24)
    return f"{nome}: {','.join(map(str, numeros))}"


def main():
    parser = argparse.ArgumentParser(description="Gera cartelas de bingo aleatórias")
    parser.add_argument("--jogadores", type=int, default=6, help="Número de jogadores (padrão: 6)")
    parser.add_argument("--saida", type=str, default="CARTELAS.TXT", help="Arquivo de saída")
    args = parser.parse_args()

    qtd = min(args.jogadores, len(NOMES_EXEMPLO))
    nomes = random.sample(NOMES_EXEMPLO, qtd)

    linhas = [
        "# Arquivo de Cartelas do Bingo",
        "# Formato: NOME_DO_JOGADOR: num1,num2,...,num24",
        "# Cada jogador deve ter exatamente 24 números únicos entre 1 e 75",
        "# A linha FREE (centro da cartela 5x5) é gerenciada automaticamente",
        "",
    ]

    for nome in nomes:
        linhas.append(gerar_cartela(nome))

    with open(args.saida, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")

    print(f"✅ {qtd} cartelas geradas em '{args.saida}'")
    for nome in nomes:
        print(f"   · {nome}")


if __name__ == "__main__":
    main()
