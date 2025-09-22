import os
import time
from entities.Ambiente import Ambiente
from entities.Agente import Agente

class Main:
    def run():
        caminho_arquivo = "/Users/gustavoferreira/Documents/gustavo/data/projects/codes/vscode/DIDI_MOCO/mazes/maze.txt"
        labirinto = Ambiente.ler_ambiente(caminho_arquivo)

        # cria "wrapper" para consistência com o agente
        class TempAmbiente:
            def __init__(self, mapa):
                self.mapa = mapa

        ambiente = TempAmbiente(labirinto)

        # posição inicial e saída usando métodos do Ambiente
        pos_inicio = Ambiente.getEntrada(ambiente.mapa)
        pos_saida = Ambiente.getSaida(ambiente.mapa)

        if not pos_inicio or not pos_saida:
            print("Erro: labirinto deve ter entrada 'E' e saída 'S'")
            return

        # cria agente na posição de entrada
        agente = Agente(posicao=pos_inicio, historico=[], score=0, direcao='L')

        # loop de execução
        while True:
            # limpa a tela antes de imprimir
            os.system('clear')  # use 'cls' no Windows

            print("\n--- Estado Atual ---\n")
            Ambiente.printar_agenteIn_ambiente(ambiente.mapa, agente)

            # espera 1 segundo
            time.sleep(1)

            # conta comida restante
            comida_restante = any('o' in linha for linha in ambiente.mapa)

            # verifica se o agente chegou na saída e não há mais comida
            y, x = agente._posicao
            if (y, x) == pos_saida and not comida_restante:
                print("\n FIM | O agente encontrou a saída")
                print(f"Score final: {agente._score}")
                break

            # move agente
            moved = agente.move(ambiente)
            if not moved:
                print("\n FIM | O agente não pode mais se mover")
                print(f"Score final: {agente._score}")
                break

            # imprime score atual
            print(f"\nScore: {agente._score}")

if __name__ == "__main__":
    Main.run()