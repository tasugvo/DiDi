
import os
import time

try:
    import cv2
    import numpy as np
    OPENCV_DISPONIVEL = True
except ImportError:
    OPENCV_DISPONIVEL = False
    print("Aviso: A biblioteca 'opencv-python' não está instalada.")
    print("Para gerar o vídeo, instale-a com: pip install opencv-python numpy")
    print("A simulação continuará sem a geração do vídeo.")


#Comeco de ambiente 
class Ambiente:

    def __init__(self, nome_arquivo):
        if not os.path.exists(nome_arquivo):
            raise FileNotFoundError(f"O arquivo de labirinto \'{nome_arquivo}\' não foi encontrado.")
        
        with open(nome_arquivo, 'r') as f:
            self.labirinto = [list(linha.strip()) for linha in f.readlines()]

        self.linhas = len(self.labirinto)
        self.colunas = len(self.labirinto[0])
        self.posicao_agente = self._encontrar_posicao_inicial()
        self.direcao_agente = 'N'  # Direção inicial padrão
        self.comidas_totais = sum(linha.count('o') for linha in self.labirinto)

    def _encontrar_posicao_inicial(self):
        #Encontra a coordenada 'E' (Entrada) no labirinto.
        for r, linha in enumerate(self.labirinto):
            for c, celula in enumerate(linha):
                if celula == 'E':
                    return [r, c]
        raise ValueError("Não foi possível encontrar a posição de entrada 'E' no labirinto.")

    def get_sensor_data(self):
        r, c = self.posicao_agente
        sensor = [['X' for _ in range(3)] for _ in range(3)]

        # Mapeia as posições relativas ao redor do agente para a matriz do sensor
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                sensor_r, sensor_c = dr + 1, dc + 1
                mapa_r, mapa_c = r + dr, c + dc

                if 0 <= mapa_r < self.linhas and 0 <= mapa_c < self.colunas:
                    sensor[sensor_r][sensor_c] = self.labirinto[mapa_r][mapa_c]
                else:
                    sensor[sensor_r][sensor_c] = 'X' # Fora dos limites é uma parede

        # A posição (1,1) do sensor representa a direção do agente
        sensor[1][1] = self.direcao_agente
        return sensor

    def set_direction(self, nova_direcao):
        """Define a nova direção do agente."""
        if nova_direcao in ['N', 'S', 'L', 'O']:
            self.direcao_agente = nova_direcao
            return True
        return False

    def move(self):
        """
        Move o agente na direção atual. Retorna True se o movimento foi bem-sucedido.
        """
        r, c = self.posicao_agente
        direcao = self.direcao_agente
        
        proxima_pos = list(self.posicao_agente) # Cria uma cópia

        if direcao == 'N': proxima_pos[0] -= 1
        elif direcao == 'S': proxima_pos[0] += 1
        elif direcao == 'O': proxima_pos[1] -= 1
        elif direcao == 'L': proxima_pos[1] += 1

        prox_r, prox_c = proxima_pos
        
        # Verifica se o movimento é válido (dentro dos limites e não é uma parede)
        if 0 <= prox_r < self.linhas and 0 <= prox_c < self.colunas and self.labirinto[prox_r][prox_c] != 'X':
            # Verifica se a próxima posição é a saída e se todas as comidas foram coletadas
            if self.labirinto[prox_r][prox_c] == 'S':
                # O agente só pode entrar na saída se todas as comidas foram coletadas
                # Esta verificação será feita na lógica do agente antes de chamar move()
                pass # Permite o movimento, a lógica do agente decidirá se é o momento certo

            self.posicao_agente = proxima_pos
            return True
        return False

    def coletar_comida(self):
        """Se houver comida na posição atual do agente, coleta-a."""
        r, c = self.posicao_agente
        if self.labirinto[r][c] == 'o':
            self.labirinto[r][c] = '_' # Substitui a comida por um corredor
            return True
        return False

    def esta_na_saida(self):
        """Verifica se o agente está na posição 'S'."""
        r, c = self.posicao_agente
        return self.labirinto[r][c] == 'S'
## Fim de ambiente


# Começo de agente 
class Agente:
    """
    Implementa a lógica de decisão do agente, memória e atuadores.
    """
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.comidas_coletadas = 0
        self.passos_dados = 0
        self.recompensa = 0
        
        # A memória é um dicionário onde a chave é a coordenada (tupla) e o valor é o tipo de célula
        self.memoria_mapa = {}
        self.caminho_percorrido = [] # Para visualização

    def _atualizar_memoria(self):
        """Usa o sensor para atualizar o mapa mental do agente."""
        sensor = self.ambiente.get_sensor_data()
        pos_agente_mapa = tuple(self.ambiente.posicao_agente)
        
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                # Coordenada no mapa real
                mapa_r, mapa_c = pos_agente_mapa[0] + dr, pos_agente_mapa[1] + dc
                # Coordenada na visão do sensor
                sensor_r, sensor_c = dr + 1, dc + 1
                
                # Adiciona à memória apenas se for uma célula nova ou se o tipo mudou (ex: comida coletada)
                if (mapa_r, mapa_c) not in self.memoria_mapa or self.memoria_mapa[(mapa_r, mapa_c)] != sensor[sensor_r][sensor_c]:
                    # Ignora a própria posição (1,1) que contém a direção
                    if not (dr == 0 and dc == 0):
                        self.memoria_mapa[(mapa_r, mapa_c)] = sensor[sensor_r][sensor_c]
        
        # Atualiza a posição atual do agente na memória (caso tenha coletado uma comida)
        self.memoria_mapa[pos_agente_mapa] = self.ambiente.labirinto[pos_agente_mapa[0]][pos_agente_mapa[1]]


    def _busca_custo_uniforme(self, inicio, objetivo_func, evitar_saida_se_comida_pendente=False):
        fila = [(0, [inicio])]  # (custo, caminho)
        visitados = {inicio}

        while fila:
            fila.sort(key=lambda x: x[0])
            custo, caminho = fila.pop(0)
            pos_atual = caminho[-1]

            if objetivo_func(pos_atual):
                # Se o objetivo é a saída e ainda há comidas pendentes, não retorne este caminho
                if evitar_saida_se_comida_pendente and self.memoria_mapa.get(pos_atual) == 'S' and self.comidas_coletadas < self.ambiente.comidas_totais:
                    continue # Não considera este caminho como válido ainda
                return caminho

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                proxima_pos = (pos_atual[0] + dr, pos_atual[1] + dc)
                
                tipo_celula = self.memoria_mapa.get(proxima_pos, '?') # '?' para desconhecido

                # Se a próxima célula é a saída e ainda há comidas pendentes, não a considere como um caminho válido para explorar
                if evitar_saida_se_comida_pendente and tipo_celula == 'S' and self.comidas_coletadas < self.ambiente.comidas_totais:
                    continue

                if proxima_pos not in visitados and tipo_celula != 'X':
                    visitados.add(proxima_pos)
                    novo_caminho = list(caminho)
                    novo_caminho.append(proxima_pos)
                    fila.append((custo + 1, novo_caminho))
        
        return None # Caminho não encontrado

    def _mover_seguindo_caminho(self, caminho):
        """Move o agente um passo de cada vez seguindo um caminho planejado."""
        if not caminho or len(caminho) < 2:
            return False # Não há caminho para mover
        
        # Move apenas um passo por vez para permitir reavaliação a cada turno
        proxima_pos_no_plano = caminho[1]
        pos_atual_no_plano = caminho[0]
            
        dr = proxima_pos_no_plano[0] - pos_atual_no_plano[0]
        dc = proxima_pos_no_plano[1] - pos_atual_no_plano[1]

        direcao_necessaria = ''
        if dr == -1: direcao_necessaria = 'N'
        elif dr == 1: direcao_necessaria = 'S'
        elif dc == -1: direcao_necessaria = 'O'
        elif dc == 1: direcao_necessaria = 'L'

        if self.ambiente.direcao_agente != direcao_necessaria:
            self.ambiente.set_direction(direcao_necessaria)
        
        # Antes de mover, verifica se a próxima posição é a saída e se todas as comidas foram coletadas
        if self.ambiente.labirinto[proxima_pos_no_plano[0]][proxima_pos_no_plano[1]] == 'S' and \
           self.comidas_coletadas < self.ambiente.comidas_totais:
            print("Tentativa de entrar na saída com comidas pendentes. Bloqueado.")
            return False # Impede o movimento para a saída se ainda há comidas

        if self.ambiente.move():
            self.passos_dados += 1
            self.caminho_percorrido.append(list(self.ambiente.posicao_agente))
            self._atualizar_memoria() # Atualiza a memória a cada passo
            return True
        else:
            # Se um movimento planejado falhar, o mapa mental está errado. Pare e replaneje.
            print("Obstáculo inesperado encontrado. Replanejando...")
            return False

    def _encontrar_alvo(self, alvo_func, evitar_saida_se_comida_pendente=False):
        """
        Encontra o alvo mais próximo (comida, saída, etc.) e retorna o caminho até ele.
        'evitar_saida_se_comida_pendente' é passado para _busca_custo_uniforme.
        """
        pos_atual = tuple(self.ambiente.posicao_agente)
        alvos_conhecidos = [pos for pos, tipo in self.memoria_mapa.items() if alvo_func(tipo)]
        
        caminho_mais_curto = None
        
        for alvo in alvos_conhecidos:
            caminho = self._busca_custo_uniforme(pos_atual, lambda p: p == alvo, evitar_saida_se_comida_pendente)
            if caminho:
                if caminho_mais_curto is None or len(caminho) < len(caminho_mais_curto): # Prioriza o caminho mais curto
                    caminho_mais_curto = caminho
        
        return caminho_mais_curto

    def _explorar(self):
        pos_atual = tuple(self.ambiente.posicao_agente)
        
        # Prioriza ir para uma célula adjacente a uma área desconhecida
        caminho_para_explorar = self._busca_custo_uniforme(
            pos_atual,
            lambda p: self.memoria_mapa.get(p) == '?' or any(self.memoria_mapa.get((p[0]+dr, p[1]+dc)) is None for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]),
            evitar_saida_se_comida_pendente=True # Não explore a saída se ainda há comidas
        )

        if caminho_para_explorar:
            print("Nenhum alvo conhecido. Explorando a fronteira mais próxima...")
            return self._mover_seguindo_caminho(caminho_para_explorar)
        
        return False

    def executar(self):
        print("Iniciando a exploração do labirinto...")
        self._atualizar_memoria()
        self.caminho_percorrido.append(list(self.ambiente.posicao_agente))

        # Loop principal: decidir e agir
        while True:
            pos_atual_tuple = tuple(self.ambiente.posicao_agente)

            # Prioridade 1: Coletar comida se estiver sobre ela
            if self.ambiente.coletar_comida():
                self.comidas_coletadas += 1
                self.memoria_mapa[pos_atual_tuple] = '_' # Atualiza memória
                print(f"Comida coletada! Total: {self.comidas_coletadas}/{self.ambiente.comidas_totais}")
            
            # Condição de parada: todas as comidas coletadas E na saída
            if self.comidas_coletadas == self.ambiente.comidas_totais and self.ambiente.esta_na_saida():
                print("\nAgente chegou à saída com todas as comidas coletadas!")
                break

            acao_tomada = False

            # Lógica de decisão principal:
            # 1. Se ainda há comidas a coletar, priorize-as.
            # 2. Se todas as comidas foram coletadas, priorize a saída.
            # 3. Se não há alvos conhecidos (comida ou saída), explore.

            if self.comidas_coletadas < self.ambiente.comidas_totais:
                # Busca por comida, evitando a saída como objetivo intermediário
                caminho_para_comida = self._encontrar_alvo(lambda tipo: tipo == 'o', evitar_saida_se_comida_pendente=True)
                if caminho_para_comida:
                    print("Encontrado caminho para a próxima comida. Movendo...")
                    acao_tomada = self._mover_seguindo_caminho(caminho_para_comida)
                else:
                    # Se não há comidas conhecidas ou acessíveis, explore para encontrar mais
                    print("Nenhuma comida conhecida ou acessível. Explorando...")
                    acao_tomada = self._explorar()
            else: # Todas as comidas foram coletadas
                # AGORA, e somente AGORA, o agente pode buscar a saída
                # Primeiro, verifica se já está na saída
                if self.ambiente.esta_na_saida(): 
                    print("Agente já está na saída após coletar todas as comidas.")
                    break # Sai do loop principal

                print("Todas as comidas coletadas. Procurando a saída...")
                # Busca pela saída, agora sem restrições de comida
                caminho_para_saida = self._encontrar_alvo(lambda tipo: tipo == 'S')
                if caminho_para_saida:
                    acao_tomada = self._mover_seguindo_caminho(caminho_para_saida)
                else:
                    # Se a saída não é conhecida ou acessível, explore para encontrá-la
                    print("Saída não conhecida ou acessível. Explorando...")
                    acao_tomada = self._explorar()
            
            # Se nenhuma ação foi tomada (agente preso ou sem opções)
            if not acao_tomada:
                print("Agente não conseguiu tomar uma ação. Pode estar preso ou sem solução.")
                break
            
            # Adiciona um limite de passos para evitar loops infinitos em labirintos complexos ou com falhas
            if self.passos_dados > (self.ambiente.linhas * self.ambiente.colunas * 10): # Aumentei o limite
                print("Limite de passos excedido. Agente pode estar preso ou sem solução.")
                break

        self._calcular_recompensa()
        self.imprimir_resultado()

    def _calcular_recompensa(self):
        """Calcula a pontuação final."""
        self.recompensa = (self.comidas_coletadas * 10) - self.passos_dados

    def imprimir_resultado(self):
        """Exibe o resumo da execução."""
        print("\n--- Simulação Finalizada ---")
        print(f"Comidas Coletadas: {self.comidas_coletadas}")
        print(f"Total de Passos: {self.passos_dados}")
        print(f"Recompensa Final: {self.recompensa} pontos")
        print("--------------------------")
## Fim de agente


def gerar_video(labirinto_inicial, caminho_percorrido, nome_arquivo_saida="trajetoria_agente.mp4"):
    """
    Gera um vídeo da trajetória do agente no labirinto.
    """
    if not OPENCV_DISPONIVEL:
        return

    print(f"\nIniciando a geração do vídeo \'{nome_arquivo_saida}\'...")

    # Definição de cores (BGR)
    cores = {
        'X': (50, 50, 50),          # Parede - Cinza escuro
        '_': (255, 255, 255),       # Corredor - Branco
        'o': (0, 255, 255),         # Comida - Amarelo
        'E': (255, 0, 0),           # Entrada - Azul
        'S': (0, 0, 255),           # Saída - Vermelho
        'agente': (0, 255, 0),      # Agente - Verde
        'rastro': (220, 220, 220)   # Rastro - Cinza claro
    }
    tamanho_celula = 30
    
    altura = len(labirinto_inicial) * tamanho_celula
    largura = len(labirinto_inicial[0]) * tamanho_celula

    # Configuração do vídeo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(nome_arquivo_saida, fourcc, 10.0, (largura, altura))

    # Cria um mapa base para desenhar
    mapa_base = np.zeros((altura, largura, 3), dtype=np.uint8)
    for r, linha in enumerate(labirinto_inicial):
        for c, celula in enumerate(linha):
            cor = cores.get(celula, (0,0,0))
            cv2.rectangle(mapa_base, (c*tamanho_celula, r*tamanho_celula), 
                          ((c+1)*tamanho_celula, (r+1)*tamanho_celula), cor, -1)

    frame_com_rastro = mapa_base.copy()
    for i, pos in enumerate(caminho_percorrido):
        frame_atual = frame_com_rastro.copy()
        
        # Desenha o rastro
        if i > 0:
            r_ant, c_ant = caminho_percorrido[i-1]
            cv2.rectangle(frame_com_rastro, (c_ant*tamanho_celula, r_ant*tamanho_celula), 
                          ((c_ant+1)*tamanho_celula, (r+1)*tamanho_celula), cores['rastro'], -1)

        # Desenha a posição atual do agente por cima do rastro
        r, c = pos
        cv2.rectangle(frame_atual, (c*tamanho_celula, r*tamanho_celula), 
                      ((c+1)*tamanho_celula, (r+1)*tamanho_celula), cores['agente'], -1)
        
        video.write(frame_atual)

    # Adiciona alguns frames finais com o agente na saída
    for _ in range(20):
        video.write(frame_atual)

    video.release()
    print("Vídeo gerado com sucesso!")


if __name__ == "__main__":
    ARQUIVO_LABIRINTO = "labirinto.txt"
    
    try:
        # Cria um arquivo de labirinto de exemplo se ele não existir
        if not os.path.exists(ARQUIVO_LABIRINTO):
            print(f"Arquivo \'{ARQUIVO_LABIRINTO}\' não encontrado. Criando um labirinto de exemplo.")
            with open(ARQUIVO_LABIRINTO, "w") as f:
                f.write("XXXXXXXXXXXXX\n")
                f.write("XE__________X\n")
                f.write("X_XXXXX_XXX_X\n")
                f.write("X_____X_____X\n")
                f.write("XXXX_XX_XXXXX\n")
                f.write("X_o_____o___X\n")
                f.write("X_X_XXXXX_X_X\n")
                f.write("X___X___X___X\n")
                f.write("XXX_X_o_X_XXX\n")
                f.write("X_______X___X\n")
                f.write("X_XXXXXXX_X_X\n")
                f.write("X_________o_X\n")
                f.write("X_XXXXX_XXX_X\n")
                f.write("X______S____X\n")
                f.write("XXXXXXXXXXXXX\n")

        # Execução principal
        ambiente = Ambiente(ARQUIVO_LABIRINTO)
        agente = Agente(ambiente)
        
        # Guarda o estado inicial do labirinto para o vídeo
        labirinto_original = [list(linha) for linha in ambiente.labirinto]

        agente.executar()
        
        # Geração do vídeo
        gerar_video(labirinto_original, agente.caminho_percorrido)

    except (FileNotFoundError, ValueError) as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")