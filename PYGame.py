import pygame
import random
from sys import exit

#Iniciar os módulos da biblioteca
pygame.init()
pygame.mixer.init()

#Music

try:
    pygame.mixer.music.load("Assets\Audio\Background_SONG.mp3")  #Música de fundo
    musica_game_over = pygame.mixer.Sound(
        "Assets\Audio\GameOver_SONG.mp3")  # Música de GameOver
except pygame.error as e:
    exit()

#Configura o volume (Opcional)
pygame.mixer.music.set_volume(0.5)
musica_game_over.set_volume(0.5)

# ------ Parâmetros | Janela & Clock (FPS) ------- #
tela_comprimento = 1200
tela_altura = 625
tela = pygame.display.set_mode((tela_comprimento, tela_altura))
clock = pygame.time.Clock()
pygame.display.set_caption("PY. Bird")

# ------ Parâmetros | Background ------- #
fundo = pygame.image.load("Assets\Pictures\PYGame.png")
fundo = pygame.transform.smoothscale(fundo, (tela_comprimento, tela_altura))

# ------ Parâmetros | Tela Inicial ------- #
tela_inicial = pygame.image.load("Assets\Pictures\Tela.png")  #Aimagem de tela inicial
tela_inicial = pygame.transform.smoothscale(tela_inicial, (tela_comprimento, tela_altura))

# ------ Parâmetros | Game Over's ------- #
game_over_surface = pygame.image.load("Assets\Pictures\Tela_Game_Over.png")
game_over_surface = pygame.transform.smoothscale(game_over_surface, (tela_comprimento, tela_altura))

# ------ Parâmetros | Personagem ------- #
personagem_surface = pygame.image.load("Assets\\Pictures\\Personagem.png")
personagem_comprimento = 65
personagem_altura = 65
personagem_surface = pygame.transform.scale(personagem_surface, (personagem_comprimento, personagem_altura))
personagem_surgimento_eixo_y = 75
personagem_surgimento_eixo_x = tela_altura / 2
personagem_rect = personagem_surface.get_rect(bottomleft=(personagem_surgimento_eixo_y, personagem_surgimento_eixo_x))

#O Personagem é criado, tal qual os tubos, utilizando-se na propriedade .rect disponível na biblioteca @PYGAME. De maneira resumida, a propriedade é utilizada para representar a área retangular de um objeto na tela (Neste caso, o personagem e os tubos), permitindo, para tanto, a manipulação da posição, tamanho, colisões e demais funções inerentes à área do objeto.

# ------ Parâmetros Funcionais | Personagem ------- #
GRAVIDADE = 0.25        # Personagem | Gravidade
FORCA_PULO = -6         # Personagem | Pulo
velocidade_y = 0.015    # Personagem | Velocidade Eixo-Y (Queda)
velocidade_x = 0        # Personagem | Velocidade Eixo-X (Aceleração) - Lógica Funcional "PY BIRD": = 0

#A criação de tubos sempre ocorre inicializando a função pelo tubo superior. Para tanto, é criado um tubo superior, de tamanho aleatório considerando a biblioteca (@random), na qual é estabelecida como parâmetro um tamanho mínimo e um tamanho máximo para sua criação. Criada o tubo superior, diante deste parâmetro, se tem a criação do tubo inferior. Para tal, considera-se o prospecto da altura da tela (Janela do Jogo) subtraída da altura que foi gerada, aleatoriamente, pelo cano superior. Após isso, é subtraída desse resultado o espaço que é definido entre os canos, evidentemente, para permitir que o personagem (usuário) possa traspor os túneis e, dessa forma, gerir a lógica do jogo. Além disso, reitera-se que, diante da estrutura do PYGAME, os tubos são adicionados à uma lista e, conforme forem passando pela tela, são removidos desta lista na finalidade de gerir a memória. 

# ------ Parâmetros Funcionais | Tubos ------- #
LARGURA_CANOS = 75  
ALTURA_CANOS = 500
ESPACO_CANOS = 200      # Espaço entre os canos (Espaço entre Cano Superior & Inferior - Não é distância entre o surgimento!!)
tubos = []              # Lista para armazenar os tubos

# ------ Parâmetros Funcionais | Imagem do Tubo ------- #
fundo_tubos = pygame.image.load("Assets\Pictures\Cano_Principal.png")
fundo_tubos = pygame.transform.scale(fundo_tubos, (LARGURA_CANOS, ALTURA_CANOS))  # Ajusta a largura, mas a altura vai variar dependendo do tubo

# ------ Parâmetros Funcionais | Tubos (Criação) ------- #
tamanho_minimo = 100
tamanho_maximo = 350
def criar_tubo(): 
    altura_canotopo = random.randint(tamanho_minimo, tamanho_maximo)    # Altura | Cano Superior
    altura_canoinferior = tela_altura - altura_canotopo - ESPACO_CANOS  # Altura | Cano Inferior
    # OBS.: A altura do cano inferior sempre considerará a altura da tela subtraída da altura do cano superior & espaço necessário entre canos!
    cano_topo = pygame.Rect(tela_comprimento, 0, LARGURA_CANOS, altura_canotopo) 
    cano_inferior = pygame.Rect(tela_comprimento, altura_canotopo + ESPACO_CANOS, LARGURA_CANOS, altura_canoinferior)
    return cano_topo, cano_inferior

# ------ Parâmetros Funcionais | Tubos (Movimentos) ------- #
velocidade_cano = 5
def mover_tubos():
    for cano in tubos:
        cano[0].x -= velocidade_cano  # Mov. | Cano Superior (Direita -> Esquerda)
        cano[1].x -= velocidade_cano  # Mov. | Cano Inferior (Direita -> Esquerda)

# ------ Parâmetros Funcionais | Tubos (Remover Tubos Fora da Tela) ------- #
def remover_tubos():
    global tubos
    tubos = [cano for cano in tubos if cano[0].x > -LARGURA_CANOS]

# ------ Parâmetros Funcionais | Colisões ------- #
def verificar_colisao():
    for cano in tubos:
        if personagem_rect.colliderect(cano[0]) or personagem_rect.colliderect(cano[1]):
            return True
    return False

# ------ Parâmetros Funcionais | Score (Tempo) ------- #
Oxanium = "Assets\Font's\Oxanium-ExtraBold.ttf"
PressStart = "Assets\Font's\PressStart2P.ttf"
fonte = pygame.font.Font(Oxanium, 40)
tempo_inicio = 0
pontuacao_final = 0  # Variável para armazenar a pontuação final
def score():
    tempo_atual = (pygame.time.get_ticks() - tempo_inicio) // 1000
    score_surface = fonte.render(str(tempo_atual), True, (240,240,240))
    score_rect = score_surface.get_rect(center=(tela_comprimento / 2, 50))
    tela.blit(score_surface, score_rect)
    pygame.draw.rect(tela, (240, 240, 240), score_rect.inflate(20,10).move(0,-1), 5, 2)
    return tempo_atual #Retorna a pontuação

# ------ Parâmetros Funcionais | Funcionamento do Jogo ------- #
ESTADO_JOGO = "INICIAL" #Define o estado inicial do Jogo p/ Controle/Incialização
game_over_music_played = False

# Loop | Jogo
while True:
    # ------ JOGO| TELA INICIAL ------- #
    if ESTADO_JOGO == "INICIAL":
        # ------ Tela Inicial | Imagem & Texto ------- #
        tela.blit(tela_inicial, (0, 0))  
        fonte_tela_inicial = pygame.font.Font(None, 50)
        texto_iniciar = fonte_tela_inicial.render("", False, 'White')
        texto_rect = texto_iniciar.get_rect(center=(tela_comprimento / 2, tela_altura / 2 + 100))
        tela.blit(texto_iniciar, texto_rect)

        # ------ Tela Inicial | Funçao QUIT (Não Excluir!) ------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ------ Tela Inicial | Inciialização 'ESPAÇO' ------- #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ESTADO_JOGO = "RUNNING"                 #Ao pressionar 'ESPAÇO' é alterado o estado do Jogo =D
                    tempo_inicio = pygame.time.get_ticks()  #Incializa o Tempo
                    tubos = []                              #Starta os tubos (Limpando eventuais remanscentes)
                    personagem_rect.bottomleft = (personagem_surgimento_eixo_y, personagem_surgimento_eixo_x)  #Reseta Personagem

        pygame.display.update()
        clock.tick(60)

    # ------ JOGO | RUNNING ------- #
    if ESTADO_JOGO == "RUNNING":
        # ------ Jogo | Funçao QUIT (Não Excluir!) ------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Inicia a música de fundo se não estiver tocando
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)  # -1 para tocar em loop

            # ------ Jogo | Mov. de Pulo 'ESPAÇO' or 'SETA PRA CIMA' or 'W' ------- #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w: 
                    velocidade_y = FORCA_PULO
                    pulo = True
        
        # ------ Aspecto Funcional | Personagem ------- #
        personagem_rect.x += velocidade_x
        velocidade_y += GRAVIDADE
        personagem_rect.y += velocidade_y

        # ------ Jogo | Delimitando o Personagem na Tela ------- #
        if personagem_rect.right >= tela_comprimento:
            personagem_rect.right = tela_comprimento
        if personagem_rect.bottom >= tela_altura:
            personagem_rect.bottom = tela_altura
        if personagem_rect.left <= 0:
            personagem_rect.left = 0
        if personagem_rect.top <= 0:
            personagem_rect.top = 0

        # ------ Aspecto Funcional | Tubos ------- #
        distancia_tubos = 300
        if len(tubos) == 0 or tubos[-1][0].x < tela_comprimento - distancia_tubos: # Cria Tubo 'SE' Lista = 0 'OR' a distância for atendida! 
            tubos.append(criar_tubo())
        mover_tubos()
        remover_tubos()

        # ------ Aspecto Funcional | Colisão ------- #
        if verificar_colisao():
            pontuacao_final = score() # Armazenando a Pontuação Final
            ESTADO_JOGO = "GAME_OVER"  # Game Over

        # ------ Aspecto Funcional | Asset's Game ------- #
        tela.blit(fundo, (0, 0))

        # ------ Aspecto Funcional | Desenhando & Implementando Imagem In Tubo ------- #
        for cano in tubos:
            # Implementando Tubo Superior | Desenho & Imagem (Cano[0])
            altura_tubo_superior = cano[0].height
            imagem_tubo_superior = pygame.transform.scale(fundo_tubos, (LARGURA_CANOS, altura_tubo_superior))  
            tela.blit(imagem_tubo_superior, (cano[0].x, cano[0].y))  

            # Implementando Tubo Inferior | Desenho & Imagem (Cano[1])
            altura_tubo_inferior = cano[1].height
            imagem_tubo_inferior = pygame.transform.scale(fundo_tubos, (LARGURA_CANOS, altura_tubo_inferior))  
            tela.blit(imagem_tubo_inferior, (cano[1].x, cano[1].y))  

        # Desenhando o Personagem
        tela.blit(personagem_surface, personagem_rect)

        # Desenhando o Score
        score()

        # ------ Jogo | Atualização de Tela & FPS (Não excluir!!) ------- #
        pygame.display.update()
        clock.tick(60)

    # ------ JOGO | GAMEOVER's ------- #
    if ESTADO_JOGO == "GAME_OVER": 

        # Toca a música de game over apenas uma vez
        if not game_over_music_played:
            pygame.mixer.music.stop()  # Para a música de fundo
            musica_game_over.play()  # Toca a música de game over
            game_over_music_played = True

        tela.blit(game_over_surface, (0, 0))

        # ---- GameOver's | Pontuação Final do Usuário ----#
        fonte_game_over = pygame.font.Font(PressStart, 30)
        game_over_text = fonte_game_over.render(f'Pontuação: {pontuacao_final}', False, (253,253,253))
        game_over_rect = game_over_text.get_rect(center=(tela_comprimento / 2, tela_altura / 2 + 100))
        tela.blit(game_over_text, game_over_rect)

        fonte_restart = pygame.font.Font(None, 40)
        texto_restart = fonte_restart.render("", False, 'White')
        texto_restart_rect = texto_restart.get_rect(center=(tela_comprimento / 2, tela_altura / 2 + 100))
        tela.blit(texto_restart, texto_restart_rect)

        # ------ Jogo | Funçao QUIT (Não Excluir!) ------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ------ Tela Inicial | Reinicialização ('ESPAÇO') ou Saída do Jogo ('ESC') ------- #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #Reinicia o jogo
                    ESTADO_JOGO = "RUNNING"
                    pontuacao_final = 0
                    tempo_inicio = pygame.time.get_ticks()
                    personagem_rect.bottomleft = (personagem_surgimento_eixo_y, personagem_surgimento_eixo_x)
                    GRAVIDADE = 0.25
                    FORCA_PULO = -6         # Personagem | Pulo
                    velocidade_y = 0.015    # Personagem | Velocidade Eixo-Y (Queda)
                    velocidade_x = 0   
                    tubos = []  #Limpa os tubos

                    # Reinicia a música de fundo
                    pygame.mixer.music.play(-1)
                    game_over_music_played = False  # Reinicia a variável de controle

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        # ------ Jogo | Atualização de Tela & FPS (Não excluir!!) ------- #
        pygame.display.update()
        clock.tick(60)
