from entities import Ambiente  # importa a classe que você criou

class Main:
    
    def run():
        
        caminho_arquivo = "/Users/gustavoferreira/Documents/gustavo/data/projects/codes/vscode/DIDI MOCÓ/mazes/maze.txt"
        labirinto = Ambiente.ler_ambiente(caminho_arquivo)

        print("\nPrintando Ambiente:\n")
        Ambiente.printar_ambiente(labirinto)


if __name__ == "__main__":
    Main.run()