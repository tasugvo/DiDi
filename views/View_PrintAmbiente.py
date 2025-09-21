from entities import Ambiente  # importa a classe que você criou

# View para testar print do ambiente
class View_PrintAmbiente:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.labirinto = None

    def carregar_labirinto(self):
        """Lê o labirinto do arquivo e armazena internamente"""
        self.labirinto = Ambiente.ler_ambiente(self.caminho_arquivo)

    def exibir_labirinto(self):
        """Exibe o labirinto no console"""
        if self.labirinto is None:
            print("Labirinto não carregado.")
            return
        print("\nPrintando Ambiente:\n")
        Ambiente.printar_ambiente(self.labirinto)

# === Exemplo de uso ===
if __name__ == "__main__":
    caminho_arquivo = "/Users/gustavoferreira/Documents/gustavo/data/projects/codes/vscode/DIDI MOCÓ/mazes/maze.txt"
    view = LabirintoView(caminho_arquivo)
    view.carregar_labirinto()
    view.exibir_labirinto()