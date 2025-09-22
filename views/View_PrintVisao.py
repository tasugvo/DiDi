from entities import Ambiente   # módulo Ambiente.py
from entities.Agente import Agente  # importa a classe Agente dentro de Agente.py

class Main:
    
    # @staticmethod
    def run():
        caminho_arquivo = "/Users/gustavoferreira/Documents/gustavo/data/projects/codes/vscode/DIDI_MOCO/mazes/maze.txt"
        labirinto = Ambiente.ler_ambiente(caminho_arquivo)

        print("\nPrintando Ambiente:\n")
        Ambiente.printar_ambiente(labirinto)

        # ===== TESTE DO AGENTE =====
        print("\nTestando sensor do agente:\n")

        # cria "instância" de Ambiente (simples) com a matriz lida
        class TempAmbiente:
            def __init__(self, mapa):
                self.mapa = mapa

        ambiente = TempAmbiente(labirinto)

        # cria agente
        agente = Agente(posicao=(1, 3), caminho=[], score=0, direcao='L')

        # chama o sensor
        visao = agente.getSensor(ambiente)

        # printa a visão 3x3
        for linha in visao:
            print(linha)


if __name__ == "__main__":
    Main.run()