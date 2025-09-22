def ler_ambiente(nome_arquivo):

    matriz_ambiente = []

    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            matriz_ambiente.append(list(linha.strip()))
    return matriz_ambiente

# strip() - remove os espaços da linha
# list() - transforma a linha/ string em uma lista de caracteres
# append() - esta adicionando um elemento no final da lista "matriz_ambiente"

def printar_ambiente(ambiente):      
    for i in range(len(ambiente)):
        for j in range(len(ambiente[0])):
                if ambiente[i][j] == '_':
                    ambiente[i][j] = ' '
    
    for linha in ambiente:
        print(' '.join(linha))

# join() - contacetar elementos de uma string
# range(n) - tranforma valor em range

def printar_agenteIn_ambiente(ambiente, agente):
        copia = [linha[:] for linha in ambiente]

        # Marca agente
        y, x = agente._posicao
        copia[y][x] = '○'

        # Substitui "_" por espaço
        for i in range(len(copia)):
            for j in range(len(copia[0])):
                if copia[i][j] == '_':
                    copia[i][j] = ' '

        for linha in copia:
            print(' '.join(linha))
