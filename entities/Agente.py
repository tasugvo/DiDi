class Agente:
    def __init__(self, posicao, caminho, score, direcao):
        self.__direcao = direcao  # 'N','S','L','O', privado
        self._posicao = posicao   # Posição atual no labirinto (linha, coluna)
        self._caminho = caminho   # Caminho percorrido até este nó (lista de posições)
        self._score = score       # Pontuação baseado no calculo de comidas e caminho percorrido

    def getSensor(self, ambiente):
        linha_agente, coluna_agente = self._posicao
        direcao = self.__direcao
    
        linhas = len(ambiente.mapa)
        colunas = len(ambiente.mapa[0])
    
        # Matriz 3x3 inicial
        sensor = [['X' for _ in range(3)] for _ in range(3)]
    
        # Dicionário com offsets relativos à direção do agente
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
    
        # Preenche sensor
        for idx, (dy, dx) in enumerate(offsets):
            sy, sx = divmod(idx, 3)
            nova_linha = linha_agente + dy
            nova_coluna = coluna_agente + dx
            if 0 <= nova_linha < linhas and 0 <= nova_coluna < colunas:
                sensor[sy][sx] = ambiente.mapa[nova_linha][nova_coluna]
    
        # Centro mostra a direção
        sensor[1][1] = direcao
    
        return sensor