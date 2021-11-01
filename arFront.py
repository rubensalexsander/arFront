import pygame
from time import time

#Utils functions:
def getPx(percents, resolution):
    place = [int(percents[0]*resolution[0]), int(percents[1]*resolution[1])]
    return place

def hasColision(area1, area2):
    area1ponto1 = area1[0]
    area1ponto2 = [area1[1][0], area1[0][1]]
    area1ponto3 = [area1[0][0], area1[1][1]]
    area1ponto4 = area1[1]
    area2ponto1 = area2[0]
    area2ponto2 = [area2[1][0], area2[0][1]]
    area2ponto3 = [area2[0][0], area2[1][1]]
    area2ponto4 = area2[1]
    if (area2ponto1[0]>=area1ponto1[0]) and (area2ponto1[1]>=area1ponto1[1]) and (area2ponto1[0]<=area1ponto4[0]) and (area2ponto1[1]<=area1ponto4[1]):
        return True
    elif (area1ponto2[0]>=area2ponto1[0]) and (area1ponto2[1]>=area2ponto1[1]) and (area1ponto2[0]<=area2ponto4[0]) and (area1ponto2[1]<=area2ponto4[1]):
        return True
    elif (area1ponto1[0]>=area2ponto1[0]) and (area1ponto1[1]>=area2ponto1[1]) and (area1ponto1[0]<=area2ponto4[0]) and (area1ponto1[1]<=area2ponto4[1]):
        return True
    elif (area2ponto2[0]>=area1ponto1[0]) and (area2ponto2[1]>=area1ponto1[1]) and (area2ponto2[0]<=area1ponto4[0]) and (area2ponto2[1]<=area1ponto4[1]):
        return True

    return False

tema_padrao = {
    'cor_back': (255,255,255),
    'cor_back_secundaria': (200, 200, 200),
    'cor_texto': (0, 0, 0),
    'cor_bt': (155,155,155),
    'cor_texto_bt': (0, 0, 0),
    'bt_radius': 2
}

universeCodeTheme = {
    'cor_back': (3, 6, 13),
    'cor_back_secundaria': (22, 27, 34),
    'cor_texto': (88, 166, 255),
    'cor_bt': (22, 27, 34),
    'cor_texto_bt': (88, 166, 255),
    'bt_radius': 5
}

class App:
    def __init__(self, resolucao=[800, 600], nomeJanela='Projeto arPygame', tema=tema_padrao):
        #Configurações
        self.resolucao = resolucao
        self.FPS_rate = None
        
        self.setTema(tema)

        #Variáveis
        self.fps = 0
        self.FPS = None
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.resolucao, flags=pygame.RESIZABLE)
        self.mouse = Mouse()

        #Lista de draws
        self.draws = []
        
        #Listas de objetos
        self.listBotoes = []
        self.listMenus = []
        self.listTextos = []
        self.listSquares = []

        #Definições-------
        if self.FPS_rate == None:
            self.FPS_rate = 9999
            
        pygame.init()
        pygame.display.set_caption(nomeJanela)

        #Times------------
        self.tempo_inicio = time()
        self.timeContoufps = time()
        #-----------------

        #Texto FPS
        self.txFps = self.novoTexto(string='FPS: None')
        self.txFps.lugar = [0.01, 0.01]
        self.txFps.active = False

        #Marca dagua ARTI
        self.txARTI = self.novoTexto(string='powered by ARTI.Tecnology')
        self.txARTI.lugar = [0.01, 0.95]
        self.txARTI.cor = self.cor_back_secundaria
        self.txARTI.active = False
    
    def setTema(self, tema):
        self.cor_back = tema['cor_back']
        self.cor_back_secundaria = tema['cor_back_secundaria']
        self.cor_texto = tema['cor_texto']
        self.cor_bt = tema['cor_bt']
        self.cor_texto_bt = tema['cor_texto_bt'],
        self.bt_radius = tema['bt_radius']
    
    def novoSquare(self, lugar=[0,0], cor=None, tamanho=[0.05,0.05], active=True, command=None, radius=None, bordas=0, end_draw=False):
        
        if not cor: cor = self.cor_bt
        if not radius: radius = self.bt_radius

        square = Square(lugar,cor,tamanho, active,command,radius,bordas,end_draw)
        self.listSquares.append(square)
        return square

    def novoBotao(self, lugar=[0,0], cor=None , tamanho=[0.1,0.055], active=True, command=None, string='Novo botão', corTexto=None, tamanhoTexto=None, fonteTexto=None, radius=None, bordas=0, end_draw=False):

        if not cor: cor = self.cor_bt
        if not corTexto: corTexto = self.cor_texto_bt
        if not tamanhoTexto: tamanhoTexto = 15
        if not fonteTexto: fonteTexto = 'ARIAL'
        if not radius: radius = self.bt_radius

        botao = Botao(lugar, cor, tamanho, active, command, string, corTexto, tamanhoTexto, fonteTexto, radius, bordas, end_draw)

        self.listBotoes.append(botao)
        return botao
    
    def novoMenu(self):
        menu = Menu(cor=(30,30,30), tamanho=[200, self.resolucao[1]])
        self.listMenus.append(menu)
        return menu
    
    def novoTexto(self, lugar=[0,0], cor=None, tamanho=15, active=True, command=None, string="Novo texto", fonte=None, end_draw=False):
        if not cor: cor = self.cor_texto
        if not fonte: fonte = "ARIAL"
        texto = Texto(lugar, cor, tamanho, active, command, string, fonte, end_draw)
        self.listTextos.append(texto)
        return texto
    
    def drawSquare(self, cor=(255,255,255), lugar=[0,0], tamanho=[40,40], radius=0, bordas=0, end_draw=False):
        pos = -1
        if end_draw: pos = 0
        self.draws.insert(pos, ("square", cor, lugar, tamanho, radius, bordas))
    
    def drawText(self, string="New text", cor=(0,0,0), lugar=[0,0], tamanho=15, fonte="ARIAL", end_draw=False):
        self.draws.append(("text", string, cor, lugar, tamanho, fonte))
    
    def drawCircle(self, cor=(255,255,255), lugar=[0,0], tamanho=10, end_draw=False):
        self.draws.append(("circle", cor, lugar, tamanho))
    
    def drawLine(self, ponto1=[0,0], ponto2=[20,0], cor=(255,255,255), espessura=1, end_draw=False):
        self.draws.append(("line", ponto1, ponto2, cor, espessura))
    
    def update(self):
        # Escreve end_draw
        self.screen.fill(self.cor_back)

        # Executa comandos do usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'finish'
            
            elif event.type == pygame.MOUSEBUTTONUP:
                areaClique = pygame.mouse.get_pos()

                for botao in self.listBotoes:
                    if hasColision(botao.getArea(self.screen.get_size()), self.mouse.getArea(areaClique)):
                        try:
                            return botao.command()
                        except:
                            print('Erro ao executar o comando do botão.')
                            
                        break
        
        for square in self.listSquares:
            if square.active:
                lugar_square = getPx(square.lugar, self.screen.get_size())
                tamanho_square = getPx(square.tamanho, self.screen.get_size())
                self.drawSquare(square.cor, lugar_square, tamanho_square, square.radius, square.bordas, square.end_draw)
        
        for botao in self.listBotoes:
            if botao.active:
                textsurface = pygame.font.SysFont(botao.string, botao.tamanhoTexto).render(botao.string, True, botao.corTexto)

                tamanho_surfice = textsurface.get_size()

                lugar_botao = getPx(botao.lugar, self.screen.get_size())
                tamanho_botao = getPx(botao.tamanho, self.screen.get_size())

                lugar_texto = [int((lugar_botao[0]+(tamanho_botao[0]/2))-tamanho_surfice[0]*0.55), int((lugar_botao[1]+(tamanho_botao[1]/2))-tamanho_surfice[1])]

                self.drawSquare(botao.cor, lugar_botao, tamanho_botao, botao.radius, botao.bordas, botao.end_draw)
                self.drawText(botao.string, cor=botao.corTexto, lugar=lugar_texto, tamanho=botao.tamanhoTexto, fonte=botao.fonteTexto)
        
        for menu in self.listMenus:
            if menu.active:
                if menu.aberto:
                    lugar_menu = getPx(menu.lugar, self.screen.get_size())
                    tamanho_menu = getPx(botao.tamanho, self.screen.get_size())
                    self.drawSquare(menu.cor, lugar_menu, tamanho_menu)
        
        for texto in self.listTextos:
            if texto.active:
                lugar_texto = getPx(texto.lugar, self.screen.get_size())
                self.drawText(texto.string, texto.cor, lugar_texto, texto.tamanho, texto.fonte)
        
        if self.FPS:
            self.txFps.string = f'FPS: {self.FPS}'
        
        #Desenha formas na tela:
        for form in self.draws:
            if form[0] == 'square':
                cor = form[1]
                lugar = form[2]
                tamanho = form[3]
                radius = form[4]
                bordas = form[5]

                pygame.draw.rect(self.screen, cor, (lugar[0], lugar[1], tamanho[0], tamanho[1]), width=bordas, border_radius=radius)
            
            elif form[0] == 'text':
                string = form[1]
                cor = form[2]
                lugar = form[3]
                tamanho = form[4]
                fonte = form[5]
                
                fonte = pygame.font.SysFont(fonte, int(tamanho))
                textsurface = fonte.render(string, True, cor)
                self.screen.blit(textsurface, lugar)
            
            elif form[0] == 'circle':
                cor = form[1]
                lugar = form[2]
                tamanho = form[3]
                pygame.draw.circle(self.screen, cor, lugar, tamanho)
            
            elif form[0] == 'line':
                ponto1 = form[1]
                ponto2 = form[2]
                cor = form[3]
                espessura = form[4]
                pygame.draw.line(self.screen, cor, ponto1, ponto2, espessura)

        self.draws = []

        #Define FPS
        if (time() - self.timeContoufps) >= 1:
            self.FPS = self.fps
            self.timeContoufps = time()
            self.fps = 0
        self.fps += 1
        self.clock.tick(self.FPS_rate)

        # Atualiza janela Pygame
        pygame.display.flip()

class object:
    def __init__(self, lugar, cor, tamanho, active, command, end_draw):
        self.lugar = lugar
        self.cor = cor
        self.tamanho = tamanho
        self.active = active
        self.command = command
        self.end_draw = end_draw

class Square(object):
    def __init__(self, lugar, cor, tamanho, active, command, radius, bordas, end_draw):
        super().__init__(lugar, cor, tamanho, active, command, end_draw)
        self.radius = radius
        self.bordas = bordas
    
    def getArea(self, resolution):
        lugar = getPx(self.lugar, resolution)
        tamanho = getPx(self.tamanho, resolution)
        return [
            [lugar[0], lugar[1]],
            [lugar[0] + tamanho[0], lugar[1] + tamanho[1]]
        ]

class Botao(Square):
    def __init__(self, lugar, cor, tamanho, active, command, string, corTexto, tamanhoTexto, fonteTexto, radius, bordas, end_draw):
        super().__init__(lugar, cor, tamanho, active, command, radius, bordas, end_draw)
        self.string = string
        self.corTexto = corTexto
        self.tamanhoTexto = tamanhoTexto
        self.fonteTexto = fonteTexto

class Menu(Square):
    def __init__(self, lugar, cor, tamanho, active, command, radius, bordas, aberto, end_draw):
        super().__init__(lugar, cor, tamanho, active, command, radius, bordas, end_draw)
        self.aberto = aberto

class Texto(object):
    def __init__(self, lugar, cor, tamanho, active, command, string, fonte, end_draw):
        super().__init__(lugar, cor, tamanho, active, command, end_draw)
        self.string = string
        self.fonte = fonte

class Mouse:
    def __init__(self, areaDeclique=[2, 2]):
        self.areaDeclique = areaDeclique

    def getArea(self, posicaoMouse):
        ponto1 = [int((posicaoMouse[0] - (self.areaDeclique[0] / 2))), int((posicaoMouse[1] - (self.areaDeclique[1] / 2))),
                  self.areaDeclique[0], self.areaDeclique[1]]
        return [ponto1, [ponto1[0] + self.areaDeclique[0], ponto1[1] + self.areaDeclique[1]]]

if __name__ == '__main__':
    arApp = App()

    def funcaoBotao():
        print('finish')

    bt1 = arApp.novoBotao()
    bt1.lugar = [0.5, 0.5]
    bt1.command = funcaoBotao
    #bt1.cor = (arApp.corTextoSecundaria)
    #bt1.tamanho = [80,45]

    def sair():
        return 'finish'

    btSair = arApp.novoBotao()
    btSair.string = 'x'
    btSair.lugar = [0.925, 0.025]
    btSair.tamanho = [0.05, 0.07]
    btSair.corTexto = (255,0,0)
    btSair.tamanhoTexto = 30
    btSair.command = sair

    txMouse = arApp.novoTexto()
    txMouse.lugar = [0.025, 0.025]

    #menu1 = arApp.novoMenu()
    #menu1.tamanho = [int(arApp.resolucao[0]*0.25), arApp.resolucao[1]]

    #sq1 = arApp.novoSquare()
    #sq1.active = False

    running = True
    while running:

        #arApp.drawSquare(lugar=[20, 500])
        arApp.drawCircle(lugar=[100,300], cor=(0,0,0))
        #arApp.drawLine(ponto1=[100,100], ponto2=[350,350], cor=(0,255,0))

        txMouse.string = str(pygame.mouse.get_pos())
        
        saida = arApp.update()
        
        if saida == 'finish':
            running = False
