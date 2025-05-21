import cv2
import mediapipe as mp
import winsound
import os
import json
import tkinter as tk
from tkinter import filedialog, simpledialog

# Configuração inicial
class PianoConfig:
    def __init__(self):
        self.teclas = {
            'C': "C.wav",
            'D': "D.wav",
            'E': "E.wav",
            'F': "F.wav",
            'G': "G.wav",
            'A': "A.wav",
            'B': "B.wav",
        }
        
        # Posições e tamanhos padrão (x1, y1, x2, y2)
        self.teclas_area = {
            'C': (50, 50, 150, 250),
            'D': (160, 50, 260, 250),
            'E': (270, 50, 370, 250),
            'F': (380, 50, 480, 250),
            'G': (490, 50, 590, 250),
            'A': (600, 50, 700, 250),
            'B': (710, 50, 810, 250),
        }
        
        self.largura_janela = 1280
        self.altura_janela = 720
        self.cor_tecla_normal = (0, 255, 0)  # Verde
        self.cor_tecla_acionada = (0, 0, 255)  # Vermelho
        self.cor_texto = (255, 255, 255)  # Branco
        
    def salvar_config(self, arquivo='piano_config.json'):
        config = {
            'teclas': self.teclas,
            'teclas_area': self.teclas_area,
            'largura_janela': self.largura_janela,
            'altura_janela': self.altura_janela,
            'cores': {
                'normal': self.cor_tecla_normal,
                'acionada': self.cor_tecla_acionada,
                'texto': self.cor_texto
            }
        }
        with open(arquivo, 'w') as f:
            json.dump(config, f)
    
    def carregar_config(self, arquivo='piano_config.json'):
        try:
            with open(arquivo, 'r') as f:
                config = json.load(f)
                self.teclas = config.get('teclas', self.teclas)
                self.teclas_area = config.get('teclas_area', self.teclas_area)
                self.largura_janela = config.get('largura_janela', self.largura_janela)
                self.altura_janela = config.get('altura_janela', self.altura_janela)
                
                cores = config.get('cores', {})
                self.cor_tecla_normal = tuple(cores.get('normal', self.cor_tecla_normal))
                self.cor_tecla_acionada = tuple(cores.get('acionada', self.cor_tecla_acionada))
                self.cor_texto = tuple(cores.get('texto', self.cor_texto))
        except FileNotFoundError:
            print("Arquivo de configuração não encontrado. Usando configurações padrão.")
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}. Usando configurações padrão.")

# Interface de configuração
class ConfigWindow:
    def __init__(self, config):
        self.config = config
        self.root = tk.Tk()
        self.root.title("Configurações do Piano")
        
        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        
        # Lista de teclas
        self.lista_teclas = tk.Listbox(self.main_frame, height=10, width=30)
        self.lista_teclas.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        self.atualizar_lista_teclas()
        
        # Botões de controle
        tk.Button(self.main_frame, text="Adicionar Tecla", command=self.adicionar_tecla).grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(self.main_frame, text="Remover Tecla", command=self.remover_tecla).grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(self.main_frame, text="Alterar Som", command=self.alterar_som).grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(self.main_frame, text="Alterar Tamanho", command=self.alterar_tamanho).grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(self.main_frame, text="Salvar Config", command=self.salvar_config).grid(row=4, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(self.main_frame, text="Carregar Config", command=self.carregar_config).grid(row=5, column=1, sticky="ew", padx=5, pady=2)
        
        # Configurações de cor
        tk.Label(self.main_frame, text="Cores:").grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        tk.Button(self.main_frame, text="Cor Normal", command=lambda: self.alterar_cor('normal')).grid(row=7, column=0, sticky="ew", padx=5, pady=2)
        tk.Button(self.main_frame, text="Cor Acionada", command=lambda: self.alterar_cor('acionada')).grid(row=7, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(self.main_frame, text="Cor Texto", command=lambda: self.alterar_cor('texto')).grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        
        # Botão para fechar
        tk.Button(self.main_frame, text="Fechar", command=self.root.destroy).grid(row=9, column=0, columnspan=2, sticky="ew", padx=5, pady=(10, 0))
    
    def atualizar_lista_teclas(self):
        self.lista_teclas.delete(0, tk.END)
        for tecla in sorted(self.config.teclas.keys()):
            self.lista_teclas.insert(tk.END, f"{tecla}: {self.config.teclas[tecla]}")
    
    def adicionar_tecla(self):
        nome = simpledialog.askstring("Nova Tecla", "Digite o nome da nova tecla:")
        if nome and nome not in self.config.teclas:
            # Posiciona a nova tecla à direita da última tecla
            ultima_tecla = max(self.config.teclas_area.items(), key=lambda x: x[1][0], default=None)
            if ultima_tecla:
                x1 = ultima_tecla[1][2] + 10
                x2 = x1 + 100
            else:
                x1, x2 = 50, 150
            
            y1, y2 = 50, 250
            
            self.config.teclas[nome] = f"{nome}.wav"
            self.config.teclas_area[nome] = (x1, y1, x2, y2)
            self.atualizar_lista_teclas()
    
    def remover_tecla(self):
        selecionado = self.lista_teclas.curselection()
        if selecionado:
            tecla = self.lista_teclas.get(selecionado[0]).split(":")[0].strip()
            if tecla in self.config.teclas:
                del self.config.teclas[tecla]
                del self.config.teclas_area[tecla]
                self.atualizar_lista_teclas()
    
    def alterar_som(self):
        selecionado = self.lista_teclas.curselection()
        if selecionado:
            tecla = self.lista_teclas.get(selecionado[0]).split(":")[0].strip()
            arquivo = filedialog.askopenfilename(title=f"Selecione o som para {tecla}", 
                                               filetypes=(("Arquivos WAV", "*.wav"), ("Todos os arquivos", "*.*")))
            if arquivo:
                self.config.teclas[tecla] = arquivo
                self.atualizar_lista_teclas()
    
    def alterar_tamanho(self):
        selecionado = self.lista_teclas.curselection()
        if selecionado:
            tecla = self.lista_teclas.get(selecionado[0]).split(":")[0].strip()
            if tecla in self.config.teclas_area:
                x1, y1, x2, y2 = self.config.teclas_area[tecla]
                
                novox1 = simpledialog.askinteger("Posição X1", f"Posição X1 para {tecla}:", initialvalue=x1)
                novoy1 = simpledialog.askinteger("Posição Y1", f"Posição Y1 para {tecla}:", initialvalue=y1)
                novox2 = simpledialog.askinteger("Posição X2", f"Posição X2 para {tecla}:", initialvalue=x2)
                novoy2 = simpledialog.askinteger("Posição Y2", f"Posição Y2 para {tecla}:", initialvalue=y2)
                
                if all(v is not None for v in [novox1, novoy1, novox2, novoy2]):
                    self.config.teclas_area[tecla] = (novox1, novoy1, novox2, novoy2)
    
    def alterar_cor(self, tipo):
        cor_atual = getattr(self.config, f'cor_tecla_{tipo}' if tipo != 'texto' else 'cor_texto')
        
        # Cria uma janela simples para selecionar cor
        cor = tk.colorchooser.askcolor(title=f"Selecione a cor {tipo}", initialcolor=cor_atual)
        if cor[1]:  # Se uma cor foi selecionada
            rgb = tuple(int(cor[1][i:i+2], 16) for i in (1, 3, 5))  # Converte hex para RGB
            if tipo == 'normal':
                self.config.cor_tecla_normal = rgb
            elif tipo == 'acionada':
                self.config.cor_tecla_acionada = rgb
            else:
                self.config.cor_texto = rgb
    
    def salvar_config(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".json", 
                                             filetypes=(("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")))
        if arquivo:
            self.config.salvar_config(arquivo)
    
    def carregar_config(self):
        arquivo = filedialog.askopenfilename(filetypes=(("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")))
        if arquivo:
            self.config.carregar_config(arquivo)
            self.atualizar_lista_teclas()
    
    def run(self):
        self.root.mainloop()

# Piano Virtual
class PianoVirtual:
    def __init__(self, config):
        self.config = config
        self.teclas_acionadas = {tecla: {'mão_esquerda': False, 'mão_direita': False} for tecla in self.config.teclas}
        
        # Inicializa o MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Inicializa a webcam
        self.cap = cv2.VideoCapture(0)
        
        # Variável para controle da janela de configurações
        self.config_window_open = False
    
    def mostrar_configuracoes(self):
        if not self.config_window_open:
            self.config_window_open = True
            config_window = ConfigWindow(self.config)
            config_window.run()
            self.config_window_open = False
    
    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Inverte a imagem horizontalmente (espelha)
            frame = cv2.flip(frame, 1)

            # Redimensiona a imagem para o tamanho da janela
            frame = cv2.resize(frame, (self.config.largura_janela, self.config.altura_janela))

            # Converte a imagem para RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Processa a imagem para detectar as mãos
            results = self.hands.process(image)

            # Converte a imagem de volta para BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Desenha as áreas das teclas na tela e adiciona os nomes das notas
            for tecla, area in self.config.teclas_area.items():
                # Define a cor da tecla
                cor = self.config.cor_tecla_normal  # Cor normal
                if self.teclas_acionadas[tecla]['mão_esquerda'] or self.teclas_acionadas[tecla]['mão_direita']:
                    cor = self.config.cor_tecla_acionada  # Cor quando acionada

                # Desenha o retângulo da tecla
                cv2.rectangle(image, (area[0], area[1]), (area[2], area[3]), cor, 2)
                
                # Adiciona o nome da nota abaixo da tecla
                texto = tecla
                tamanho_fonte = 1
                espessura = 2
                posicao_texto = (area[0] + 30, area[3] + 40)
                cv2.putText(image, texto, posicao_texto, cv2.FONT_HERSHEY_SIMPLEX, 
                           tamanho_fonte, self.config.cor_texto, espessura)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Obtém a posição da ponta do dedo indicador
                    x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image.shape[1])
                    y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image.shape[0])

                    # Verifica se a ponta do dedo está dentro de uma área de tecla
                    for tecla, area in self.config.teclas_area.items():
                        if area[0] < x < area[2] and area[1] < y < area[3]:
                            # Determina qual mão está acionando a tecla
                            handedness = results.multi_handedness[results.multi_hand_landmarks.index(hand_landmarks)].classification[0].label

                            if handedness == 'Left' and not self.teclas_acionadas[tecla]['mão_esquerda']:
                                winsound.PlaySound(self.config.teclas[tecla], winsound.SND_ASYNC)
                                self.teclas_acionadas[tecla]['mão_esquerda'] = True
                            elif handedness == 'Right' and not self.teclas_acionadas[tecla]['mão_direita']:
                                winsound.PlaySound(self.config.teclas[tecla], winsound.SND_ASYNC)
                                self.teclas_acionadas[tecla]['mão_direita'] = True
                        else:
                            # Reseta o estado da tecla para a mão correspondente
                            handedness = results.multi_handedness[results.multi_hand_landmarks.index(hand_landmarks)].classification[0].label
                            if handedness == 'Left':
                                self.teclas_acionadas[tecla]['mão_esquerda'] = False
                            elif handedness == 'Right':
                                self.teclas_acionadas[tecla]['mão_direita'] = False

                    # Desenha os landmarks da mão
                    self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # Mostra a imagem
            cv2.imshow('Piano Invisivel', image)

            # Verifica teclas de controle
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('c'):
                self.mostrar_configuracoes()

        # Libera a webcam e fecha as janelas
        self.cap.release()
        cv2.destroyAllWindows()

# Ponto de entrada do programa
if __name__ == "__main__":
    # Carrega a configuração
    config = PianoConfig()
    config.carregar_config()
    
    # Inicia o piano
    piano = PianoVirtual(config)
    piano.run()
    
    # Salva a configuração ao sair
    config.salvar_config()

# import cv2
# import mediapipe as mp
# import winsound

# # Inicializa o MediaPipe Hands
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)  # Permitir até 2 mãos
# mp_drawing = mp.solutions.drawing_utils

# # Define os arquivos de som das teclas do piano
# teclas = {
#     'C': "C.wav",
#     'D': "D.wav",
#     'E': "E.wav",
#     'F': "F.wav",
#     'G': "G.wav",
#     'A': "A.wav",
#     'B': "B.wav",
# }

# # Define as áreas das teclas (x1, y1, x2, y2) - Reposicionadas para o canto superior esquerdo
# teclas_area = {
#     'C': (50, 50, 150, 250),   # Tecla C
#     'D': (160, 50, 260, 250),   # Tecla D
#     'E': (270, 50, 370, 250),   # Tecla E
#     'F': (380, 50, 480, 250),   # Tecla F
#     'G': (490, 50, 590, 250),   # Tecla G
#     'A': (600, 50, 700, 250),   # Tecla A
#     'B': (710, 50, 810, 250),   # Tecla B
# }

# # Inicializa a webcam
# cap = cv2.VideoCapture(0)

# # Define o tamanho da janela (largura, altura)
# largura_janela = 1280
# altura_janela = 720

# # Dicionário para rastrear se uma tecla já foi acionada por cada mão
# teclas_acionadas = {tecla: {'mão_esquerda': False, 'mão_direita': False} for tecla in teclas}

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Inverte a imagem horizontalmente (espelha)
#     frame = cv2.flip(frame, 1)

#     # Redimensiona a imagem para o tamanho da janela
#     frame = cv2.resize(frame, (largura_janela, altura_janela))

#     # Converte a imagem para RGB
#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     image.flags.writeable = False

#     # Processa a imagem para detectar as mãos
#     results = hands.process(image)

#     # Converte a imagem de volta para BGR
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#     # Desenha as áreas das teclas na tela e adiciona os nomes das notas
#     for tecla, area in teclas_area.items():
#         # Define a cor da tecla (verde se não acionada, vermelha se acionada)
#         cor = (0, 255, 0)  # Verde
#         if teclas_acionadas[tecla]['mão_esquerda'] or teclas_acionadas[tecla]['mão_direita']:
#             cor = (0, 0, 255)  # Vermelho

#         # Desenha o retângulo da tecla
#         cv2.rectangle(image, (area[0], area[1]), (area[2], area[3]), cor, 2)
        
#         # Adiciona o nome da nota abaixo da tecla
#         texto = tecla
#         tamanho_fonte = 1
#         espessura = 2
#         cor_texto = (255, 255, 255)  # Branco
#         posicao_texto = (area[0] + 30, area[3] + 40)  # Ajuste a posição do texto
#         cv2.putText(image, texto, posicao_texto, cv2.FONT_HERSHEY_SIMPLEX, tamanho_fonte, cor_texto, espessura)

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Obtém a posição da ponta do dedo indicador
#             x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image.shape[1])
#             y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image.shape[0])

#             # Verifica se a ponta do dedo está dentro de uma área de tecla
#             for tecla, area in teclas_area.items():
#                 if area[0] < x < area[2] and area[1] < y < area[3]:
#                     # Determina qual mão está acionando a tecla (esquerda ou direita)
#                     handedness = results.multi_handedness[results.multi_hand_landmarks.index(hand_landmarks)].classification[0].label

#                     if handedness == 'Left' and not teclas_acionadas[tecla]['mão_esquerda']:
#                         winsound.PlaySound(teclas[tecla], winsound.SND_ASYNC)
#                         teclas_acionadas[tecla]['mão_esquerda'] = True
#                     elif handedness == 'Right' and not teclas_acionadas[tecla]['mão_direita']:
#                         winsound.PlaySound(teclas[tecla], winsound.SND_ASYNC)
#                         teclas_acionadas[tecla]['mão_direita'] = True
#                 else:
#                     # Reseta o estado da tecla para a mão correspondente
#                     handedness = results.multi_handedness[results.multi_hand_landmarks.index(hand_landmarks)].classification[0].label
#                     if handedness == 'Left':
#                         teclas_acionadas[tecla]['mão_esquerda'] = False
#                     elif handedness == 'Right':
#                         teclas_acionadas[tecla]['mão_direita'] = False

#             # Desenha os landmarks da mão
#             mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#     # Mostra a imagem
#     cv2.imshow('Piano Invisivel', image)

#     # Sai do loop se a tecla 'q' for pressionada
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Libera a webcam e fecha as janelas
# cap.release()
# cv2.destroyAllWindows()