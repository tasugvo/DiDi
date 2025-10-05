class Agente:
    def __init__(self, posicao, historico, score, direcao):
        self.__direcao   = direcao
        self.__posicao   = posicao
        self.__historico = historico
        self.__score     = score

    # setters
    def setPosicao(self, posicao):
        self.__posicao = posicao

    def setDirecao(self, direcao):
        self.__direcao = direcao

    def setHistorico(self, ponto):
        self.__historico.append(ponto)

    # getters
    def getPosicao(self):
        return self.__posicao

    def getDirecao(self):
        return self.__direcao

    def getHistorico(self):
        return self.__historico

    def getScore(self):
        return self.__score

    def setScore(self, valor):
        self.__score = valor

    def getSensor(self, ambiente):
        linha_agente, coluna_agente = self.__posicao
        direcao = self.__direcao

        linhas = len(ambiente.mapa)
        colunas = len(ambiente.mapa[0])

        sensor = [['X' for _ in range(3)] for _ in range(3)]

        offsets_por_direcao = {
            'N': [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),  (0, 0),  (0, 1),
                  (1, -1),  (1, 0),  (1, 1)],
            'S': [(1, 1),   (1, 0),   (1, -1),
                  (0, 1),   (0, 0),   (0, -1),
                  (-1, 1),  (-1, 0),  (-1, -1)],
            'L': [(-1, 1),  (0, 1),   (1, 1),
                  (-1, 0),  (0, 0),   (1, 0),
                  (-1, -1), (0, -1),  (1, -1)],
            'O': [(1, -1),  (0, -1),  (-1, -1),
                  (1, 0),   (0, 0),   (-1, 0),
                  (1, 1),   (0, 1),   (-1, 1)]
        }

        offsets = offsets_por_direcao[direcao]

        # varre área 3x3
        for sy in range(3):
            for sx in range(3):
                dy, dx = offsets[sy * 3 + sx]
                ny, nx = linha_agente + dy, coluna_agente + dx
                if 0 <= ny < linhas and 0 <= nx < colunas:
                    sensor[sy][sx] = ambiente.mapa[ny][nx]

        sensor[1][1] = direcao  # posição central indica orientação
        return sensor

    def move(self):
        # implementar busca por custo uniforme usando apenas o sensor
        return True