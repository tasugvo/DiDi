class Ambiente:
    @staticmethod
    def ler_ambiente(nome_arquivo):
        matriz_ambiente = []
        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                matriz_ambiente.append(list(linha.strip()))
        return matriz_ambiente

    @staticmethod
    def printar_ambiente(ambiente):
        copia = [linha[:] for linha in ambiente]
        for i in range(len(copia)):
            for j in range(len(copia[0])):
                if copia[i][j] == '_':
                    copia[i][j] = ' '
        for linha in copia:
            print(' '.join(linha))

    @staticmethod
    def printar_agenteIn_ambiente(ambiente, agente):
        copia = [linha[:] for linha in ambiente]
        y, x = agente.getPosicao()
        copia[y][x] = '◆'
        for i in range(len(copia)):
            for j in range(len(copia[0])):
                if copia[i][j] == '_':
                    copia[i][j] = ' '
        for linha in copia:
            print(' '.join(linha))
    
    @staticmethod
    def getEntrada(mapa):
        for i in range(len(mapa)):
            for j in range(len(mapa[0])):
                if mapa[i][j] == 'E':
                    return (i, j)
        return None

    @staticmethod
    def getSaida(mapa):
        for i in range(len(mapa)):
            for j in range(len(mapa[0])):
                if mapa[i][j] == 'S':
                    return (i, j)
        return None