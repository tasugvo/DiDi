class Agente:
    def __init__(self, posicao, historico, score, direcao):
        self.__direcao   = direcao       # 'N','S','L','O'                                               - private

        self.__posicao   = posicao       # Posição atual no labirinto (linha, coluna)                    - private
        self.__historico = historico     # Caminho percorrido até este nó (lista de posições)            - private
        self.__score     = score         # Pontuação baseado no calculo de comidas e caminho percorrido  - private

    def setPosicao(self, posicao):
        self.__posicao = posicao
    
    def setDirecao(self, direcao):
        self.__posicao = direcao

    def setHistorico(self, ponto):
        self._historico.append(ponto)


    def getPosicao(self):
        return self.__posicao
    
    def getDirecao(self):
        return self.__direcao


    def getSensor(self, ambiente):
        linha_agente, coluna_agente = self._posicao # armazendando atributos do estado atual da posicao
        direcao = self.__direcao                    # armazendando atributos do estado atual da direcao
    
        linhas = len(ambiente.mapa)
        colunas = len(ambiente.mapa[0])
    
        sensor = [['X' for _ in range(3)] for _ in range(3)]
    
        # tupla offsets relativos à direção do agente
        offsets_por_direcao = {
            'N': [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),  (0, 0),  (0, 1),
                (1, -1),  (1, 0),  (1, 1)
            ],
            'S': [
                (1, 1),   (1, 0),   (1, -1),
                (0, 1),   (0, 0),   (0, -1),
                (-1, 1),  (-1, 0),  (-1, -1)
            ],
            'L': [
                (-1, 1),  (0, 1),   (1, 1),
                (-1, 0),  (0, 0),   (1, 0),
                (-1, -1), (0, -1),  (1, -1)
            ],
            'O': [
                (1, -1),  (0, -1),  (-1, -1),
                (1, 0),   (0, 0),   (-1, 0),
                (1, 1),   (0, 1),   (-1, 1)
            ]
        }
    
        # Pega os offsets corretos de acordo com a direção
        offsets = offsets_por_direcao[direcao]
    
        for sy in range(3):
            for sx in range(3):
                dy, dx = offsets[sy * 3 + sx]
                nova_linha = linha_agente + dy
                nova_coluna = coluna_agente + dx
                if 0 <= nova_linha < linhas and 0 <= nova_coluna < colunas:
                    sensor[sy][sx] = ambiente.mapa[nova_linha][nova_coluna]
    
        sensor[1][1] = direcao
    
        return sensor
    
    def move(self, ambiente):
        # Criar algo utilizando busca por custo uniforme
        # Utilizar apenas a visão de getsensor
        return True