class Agente:
    def __init__(self, posicao, historico, score, direcao):
        self.__direcao = direcao    # 'N','S','L','O'                                               - private

        self._posicao   = posicao     # Posição atual no labirinto (linha, coluna)                    - protected
        self._historico = historico # Caminho percorrido até este nó (lista de posições)            - protected
        self._score     = score         # Pontuação baseado no calculo de comidas e caminho percorrido  - protected

    def setHistorico(self, ponto):
        self._historico.append(ponto)


    def getSensor(self, ambiente):
        linha_agente, coluna_agente = self._posicao # armazendando atributos do estado atual da posicao
        direcao = self.__direcao                    # armazendando atributos do estado atual da direcao
    
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
    
        # Preenche sensor (2 fors em vez de enumerate)
        for sy in range(3):
            for sx in range(3):
                dy, dx = offsets[sy * 3 + sx]
                nova_linha = linha_agente + dy
                nova_coluna = coluna_agente + dx
                if 0 <= nova_linha < linhas and 0 <= nova_coluna < colunas:
                    sensor[sy][sx] = ambiente.mapa[nova_linha][nova_coluna]
    
        # Centro mostra a direção
        sensor[1][1] = direcao
    
        return sensor
    
    def move(self, ambiente):
        sensor = self.getSensor(ambiente)
        direcoes = ['N', 'S', 'O', 'L']  # possíveis direções

        # Mapear posições relativas do sensor para movimentação (dy, dx)
        mapa_offsets = {
            'N': [(-1,0), (1,0), (0,-1), (0,1)],  # frente, trás, esquerda, direita
            'S': [(1,0), (-1,0), (0,1), (0,-1)],
            'L': [(0,1), (0,-1), (-1,0), (1,0)],
            'O': [(0,-1), (0,1), (1,0), (-1,0)]
        }

        # 1️⃣ Verifica se há comida adjacente no sensor
        posicoes = mapa_offsets[self.__direcao]
        for dy, dx in posicoes:
            y, x = self._posicao[0] + dy, self._posicao[1] + dx
            if 0 <= y < len(ambiente.mapa) and 0 <= x < len(ambiente.mapa[0]):
                if ambiente.mapa[y][x] == 'o':
                    # Move diretamente para a comida
                    self.setHistorico(self._posicao)
                    self._posicao = (y, x)
                    self._score += 9  # -1 passo + 10 comida
                    ambiente.mapa[y][x] = '_'
                    return True

        # 2️⃣ Se não houver comida, usa BFS para encontrar a mais próxima
        # Mantemos a lógica antiga de BFS
        def obter_vizinhos(pos):
            direcoes = [(-1,0), (1,0), (0,-1), (0,1)]
            vizinhos = []
            for d in direcoes:
                ny, nx = pos[0]+d[0], pos[1]+d[1]
                if 0 <= ny < len(ambiente.mapa) and 0 <= nx < len(ambiente.mapa[0]):
                    if ambiente.mapa[ny][nx] != 'X':
                        vizinhos.append((ny, nx))
            return vizinhos

        inicio = self._posicao
        fila = [(inicio, [])]
        visitados = [inicio]
        alvo = None
        caminho_ate_alvo = None

        while len(fila) > 0:
            pos, caminho = fila[0]
            fila = fila[1:]
            if ambiente.mapa[pos[0]][pos[1]] == 'o':
                alvo = pos
                caminho_ate_alvo = caminho + [pos]
                break
            for viz in obter_vizinhos(pos):
                if viz not in visitados:
                    fila.append((viz, caminho + [viz]))
                    visitados.append(viz)

        # Se não encontrou comida, procura a saída
        if alvo is None:
            fila = [(inicio, [])]
            visitados = [inicio]
            while len(fila) > 0:
                pos, caminho = fila[0]
                fila = fila[1:]
                if ambiente.mapa[pos[0]][pos[1]] == 'S':
                    alvo = pos
                    caminho_ate_alvo = caminho + [pos]
                    break
                for viz in obter_vizinhos(pos):
                    if viz not in visitados:
                        fila.append((viz, caminho + [viz]))
                        visitados.append(viz)

        if caminho_ate_alvo is None:
            return False

        #Move o agente para o primeiro passo do caminho encontrado
        proxima_posicao = caminho_ate_alvo[0]
        self.setHistorico(self._posicao)
        self._posicao = proxima_posicao
        self._score -= 1  # -1 ponto por passo
        if ambiente.mapa[proxima_posicao[0]][proxima_posicao[1]] == 'o':
            self._score += 10
            ambiente.mapa[proxima_posicao[0]][proxima_posicao[1]] = '_'

        return True