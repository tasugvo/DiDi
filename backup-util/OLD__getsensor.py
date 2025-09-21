# versao 1 do getsensor
def getSensor(self, ambiente):
        # pega posição e direção do agente
        ax, ay = self._posicao
        direcao = self.__direcao

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

        return 

# versao 2 
def getSensor(self, ambiente):
        # Pega posição e direção do agente
        linha_agente, coluna_agente = self._posicao
        direcao = self.__direcao
    
        linhas = len(ambiente.mapa)
        colunas = len(ambiente.mapa[0])
    
        # Cria matriz 3x3 inicial preenchida com 'X'
        sensor = [['X' for _ in range(3)] for _ in range(3)]
    
        # Percorre offsets [-1, 0, +1]
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nova_linha = linha_agente + dy
                nova_coluna = coluna_agente + dx
    
                # Posição dentro da matriz sensor
                sy = dy + 1
                sx = dx + 1
    
                # Verifica se está dentro do ambiente
                if 0 <= nova_linha < linhas and 0 <= nova_coluna < colunas:
                    sensor[sy][sx] = ambiente.mapa[nova_linha][nova_coluna]
    
        # No centro do sensor, coloca a direção do agente
        sensor[1][1] = direcao
    
        return sensor