class Agente:
    def __init__(self, point, caminho, score):
        self.point = point      # Posição atual no labirinto (linha, coluna)
        self.caminho = caminho  # Caminho percorrido até este nó (lista de posições)
        self.score = score      # Pontuação baseado no calculo de comidas e caminho percorrido
