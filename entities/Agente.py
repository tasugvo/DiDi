class Agente:
    def __init__(self, posicao, caminho, score, direcao):
        self.__direcao = direcao  # 'N','S','L','O'

        self._posicao = posicao  # Posição atual no labirinto (linha, coluna)
        self._caminho = caminho  # Caminho percorrido até este nó (lista de posições)
        self._score = score      # Pontuação baseado no calculo de comidas e caminho percorrido
        
        def getSensor(self, ambiente):
        # pega posição e direção do agente
            ax, ay = self.posicao
            direcao = self.direcao

            linhas = len(ambiente.mapa)
            colunas = len(ambiente.mapa[0])

            # cria matriz 3x3 inicial preenchida com 'X'
            sensor = [['X' for _ in range(3)] for _ in range(3)]

            # percorre offsets [-1, 0, +1]
            for dy in range(-1, 2):
                 for dx in range(-1, 2):
                    mx = ax + dx   # posição real no mapa
                    my = ay + dy
                    sx = dx + 1    # posição dentro da matriz sensor
                    sy = dy + 1

                    # verifica se está dentro do ambiente
                    if 0 <= my < linhas and 0 <= mx < colunas:
                        sensor[sy][sx] = ambiente.mapa[my][mx]

        # no centro do sensor, coloca a direção do agente
        sensor[1][1] = direcao

        return sensor