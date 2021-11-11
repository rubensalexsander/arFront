import pygame
from time import time

#Utils functions:
def get_size_surfice(string, fonte, tamanho):
    textsurface = pygame.font.SysFont(fonte, tamanho).render(string, True, (0,0,0))
    return textsurface.get_size()

def get_px(vals, resolution):
    type_form = type(vals)
    if type_form == list or type_form == tuple:
        list_return = []
        for i in range(len(vals)):
            type_val = type(vals[i])
            if type_val == float:
                val = int(vals[i]*resolution[i])
            else:
                val = vals[i]
            list_return.append(val)

        return list_return

    elif type_form == float:
        return int(type_form*resolution)

def has_colision(area1, area2):
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

def refer_adjust(lugar, tamanho, refer):
    if refer == 'nl':
        lugar_return = lugar
    elif refer == 'nr':
        lugar_return = [int(lugar[0]-tamanho[0]), int(lugar[1])]
    elif refer == 'sl':
        lugar_return = [int(lugar[0]), int(lugar[1]-tamanho[1])]
    elif refer == 'sr':
        lugar_return = [int(lugar[0]-tamanho[0]), int(lugar[1]-tamanho[1])]
    elif refer == 'c':
        lugar_return = [int(lugar[0]-(tamanho[0]/2)), int(lugar[1]-(tamanho[1]/2))]
    
    return lugar_return

tema_padrao = {
    'cor_back': (255,255,255),
    'cor_back_secundaria': (200, 200, 200),
    'cor_texto': (0, 0, 0),
    'cor_bt': (155,155,155),
    'cor_texto_bt': (0, 0, 0),
    'cor_bordas_bt': (120, 120, 120),
    'bt_radius': 2
}

universeCodeTheme = {
    'cor_back': (3, 6, 13),
    'cor_back_secundaria': (22, 27, 34),
    'cor_texto': (88, 166, 255),
    'cor_bt': (22, 27, 34),
    'cor_texto_bt': (88, 166, 255),
    'cor_bordas_bt': (88, 166, 255),
    'bt_radius': 5
}

hackingBlack = {
    'cor_back': (10, 10, 10),
    'cor_back_secundaria': (15, 15, 15),
    'cor_texto': (0, 255, 0),
    'cor_bt': (25, 25, 25),
    'cor_texto_bt': (0, 250, 0),
    'cor_bordas_bt': (0, 250, 0),
    'bt_radius': 1
}

class App:
    def __init__(self, resolucao=[800, 600], nomeJanela='Projeto arFront', tema=tema_padrao):
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
            self.FPS_rate = 30
            
        pygame.init()
        pygame.display.set_caption(nomeJanela)

        #Times------------
        self.tempo_inicio = time()
        self.timeContoufps = time()
        #-----------------

        #Texto FPS
        self.txFps = self.novoTexto(string='FPS: None', lugar=[0.01, 0.01])
        self.txFps.active = False

        #Marca dagua ARTI
        self.txARTI = self.novoTexto(string='powered by ARTI.Tecnology', lugar=[5, 0.975])
        self.txARTI.cor = self.cor_back_secundaria
        self.txARTI.active = True
        self.txARTI.refer = 'sl'
    
    def setTema(self, tema):
        self.cor_back = tema['cor_back']
        self.cor_back_secundaria = tema['cor_back_secundaria']
        self.cor_texto = tema['cor_texto']
        self.cor_bt = tema['cor_bt']
        self.cor_texto_bt = tema['cor_texto_bt'],
        self.cor_bordas_bt = tema['cor_bordas_bt'],
        self.bt_radius = tema['bt_radius']
    
    def novoSquare(self, lugar=[0,0], refer='nl', cor=None, tamanho=[0.05,0.05], active=True, command=None, radius=None, bordas=0, corBordas=None, end_draw=False):
        
        if not cor: cor = self.cor_bt
        if not radius: radius = self.bt_radius

        square = Square(lugar, refer, cor,tamanho, active,command,radius,bordas, corBordas, end_draw)
        self.listSquares.append(square)
        return square

    def novoBotao(self, lugar:list=[0,0], refer:str='nl', cor:tuple=None , tamanho:list=[0.1,0.055], active:bool=True, command=None, string:str='Novo botão', corTexto:tuple=None, tamanhoTexto:int=None, fonteTexto:str=None, radius:int=None, bordas:int=0, corBordas:tuple=None, end_draw:bool=False):

        if not cor: cor = self.cor_bt
        if not corTexto: corTexto = self.cor_texto_bt
        if not tamanhoTexto: tamanhoTexto = 15
        if not fonteTexto: fonteTexto = 'ARIAL'
        if not radius: radius = self.bt_radius
        
        botao = Botao(lugar, refer, cor, tamanho, active, command, string, corTexto, tamanhoTexto, fonteTexto, radius, bordas, corBordas, end_draw)

        self.listBotoes.append(botao)
        return botao
    
    def novoMenu(self):
        menu = Menu(cor=(30,30,30), tamanho=[200, self.resolucao[1]])
        self.listMenus.append(menu)
        return menu
    
    def novoTexto(self, lugar=[0,0], refer='nl', cor=None, tamanho=15, active=True, command=None, string="Novo texto", fonte=None, end_draw=False):
        if not cor: cor = self.cor_texto
        if not fonte: fonte = "ARIAL"
        texto = Texto(lugar, refer, cor, tamanho, active, command, string, fonte, end_draw)
        self.listTextos.append(texto)
        return texto
    
    def drawSquare(self, cor:tuple=(255,255,255), lugar:list=[0,0], refer="nl", tamanho:list=[40,40], radius:int=0, bordas:int=0, corBordas:tuple=None, end_draw:bool=False):
        pos = -1
        if end_draw: pos = 0
        if (not corBordas) and (bordas > 0):
            corBordas = self.cor_bordas_bt

        tamanho = get_px(tamanho, self.screen.get_size())
        lugar = get_px(lugar, self.screen.get_size())
        lugar = refer_adjust(lugar, tamanho, refer)
        

        self.draws.insert(pos, ("square", cor, lugar, tamanho, radius, bordas, corBordas))
    
    def drawText(self, string="New text", cor=(0,0,0), lugar=[0,0], refer="nl", tamanho=15, fonte="ARIAL", end_draw=False):

        tamanho_surface = get_size_surfice(string, fonte, tamanho)

        lugar = get_px(lugar, self.screen.get_size())
        lugar = refer_adjust(lugar, tamanho_surface, refer)

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
                self.mouse.lugar = pygame.mouse.get_pos()
                
                for botao in self.listBotoes:
                    if has_colision(botao.getArea(self.screen.get_size()), self.mouse.getArea(self.screen.get_size())):
                        try:
                            return botao.command()
                        except:
                            print('Erro no comando do botão.')
        
        for square in self.listSquares:
            if square.active:
                
                self.drawSquare(square.cor, square.lugar, square.refer, square.tamanho, square.radius, square.bordas, square.corBordas, square.end_draw)
        
        #Adiciona botões à lista de escrita
        for botao in self.listBotoes:
            if botao.active:
                def get_lugar_texto(lugar_botao, tamanho_botao, refer_botao):
                    if refer_botao == 'nl':
                        return [int(lugar_botao[0]+(tamanho_botao[0]/2)), int(lugar_botao[1]+(tamanho_botao[1]/2))]
                    elif refer_botao == 'nr':
                        return [int(lugar_botao[0]-(tamanho_botao[0]/2)), int(lugar_botao[1]+(tamanho_botao[1]/2))]
                    elif refer_botao == 'sl':
                        return [int(lugar_botao[0]+(tamanho_botao[0]/2)), int(lugar_botao[1]-(tamanho_botao[1]/2))]
                    elif refer_botao == 'sr':
                        return [int(lugar_botao[0]-(tamanho_botao[0]/2)), int(lugar_botao[1]-(tamanho_botao[1]/2))]
                    else:
                        return lugar_botao

                tamanho_screen = self.screen.get_size()
                lugar_botao = get_px(botao.lugar, tamanho_screen)
                tamanho_botao = get_px(botao.tamanho, tamanho_screen)
                lugar_texto = get_lugar_texto(lugar_botao, tamanho_botao, botao.refer)

                self.drawSquare(cor=botao.cor, lugar=botao.lugar, refer=botao.refer, tamanho=botao.tamanho, radius=botao.radius, bordas=botao.bordas, corBordas=botao.corBordas, end_draw=botao.end_draw)
                self.drawText(botao.string, cor=botao.corTexto, lugar=lugar_texto, tamanho=botao.tamanhoTexto, fonte=botao.fonteTexto, refer='c')
        
        for menu in self.listMenus:
            if menu.active:
                if menu.aberto:
                    self.drawSquare(menu.cor, menu.lugar, menu.tamanho, bordas=1)
        
        #Adiciona textos à lista de escrita
        for texto in self.listTextos:
            if texto.active:
                
                self.drawText(texto.string, texto.cor, texto.lugar, texto.refer, texto.tamanho, texto.fonte)
        
        #Outros updates
        self.txFps.string = f'FPS: {self.FPS}'
        
        if self.FPS:
            pass
        
        #Desenha formas na tela:
        for form in self.draws:
            if form[0] == 'square':
                cor = form[1]
                lugar = form[2]
                tamanho = form[3]
                radius = form[4]
                bordas = form[5]
                corBordas = form[6]

                if not cor[0] == -1:
                    pygame.draw.rect(self.screen, cor, (lugar[0], lugar[1], tamanho[0], tamanho[1]), width=0, border_radius=radius)
                if bordas > 0:
                    pygame.draw.rect(self.screen, corBordas, (lugar[0], lugar[1], tamanho[0], tamanho[1]), width=bordas, border_radius=radius)
            
            elif form[0] == 'text':
                string = form[1]
                cor = form[2]
                lugar = form[3]
                tamanho = form[4]
                fonte = form[5]
                
                fonte = pygame.font.SysFont(fonte, tamanho)
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
    def __init__(self, lugar, refer, cor, tamanho, active, command, end_draw):
        self.lugar = lugar
        self.refer = refer
        self.cor = cor
        self.tamanho = tamanho
        self.active = active
        self.command = command
        self.end_draw = end_draw

class Square(object):
    def __init__(self, lugar, refer, cor, tamanho, active, command, radius, bordas, corBordas, end_draw):
        super().__init__(lugar, refer, cor, tamanho, active, command, end_draw)
        self.radius = radius
        self.bordas = bordas
        self.corBordas = corBordas
    
    def getArea(self, resolution):
        tamanho = get_px(self.tamanho, resolution)
        lugar = get_px(self.lugar, resolution)
        lugar = refer_adjust(lugar, tamanho, self.refer)
        
        return [
            [lugar[0], lugar[1]],
            [lugar[0] + tamanho[0], lugar[1] + tamanho[1]]
        ]

class Botao(Square):
    def __init__(self, lugar, refer, cor, tamanho, active, command, string, corTexto, tamanhoTexto, fonteTexto, radius, bordas, corBordas, end_draw):
        super().__init__(lugar, refer, cor, tamanho, active, command, radius, bordas, corBordas, end_draw)
        self.string = string
        self.corTexto = corTexto
        self.tamanhoTexto = tamanhoTexto
        self.fonteTexto = fonteTexto

class Menu(Square):
    def __init__(self, lugar, refer, cor, tamanho, active, command, radius, bordas, corBordas, aberto, end_draw):
        super().__init__(lugar, refer, cor, tamanho, active, command, radius, bordas, corBordas, end_draw)
        self.aberto = aberto

class Texto(object):
    def __init__(self, lugar, refer, cor, tamanho, active, command, string, fonte, end_draw):
        super().__init__(lugar, refer, cor, tamanho, active, command, end_draw)

        self.string = string
        self.fonte = fonte

class Mouse(Square):
    def __init__(self, areaDeclique=[2, 2], refer='nl'):
        self.tamanho = areaDeclique
        self.refer = refer

if __name__ == '__main__':
    arApp = App(tema=hackingBlack)

    arApp.txFps.active = True

    def funcaoBotao():
        print('AAAAAAAAA')

    bt1 = arApp.novoBotao()
    bt1.tamanho = [0.3, 0.2]
    bt1.lugar = [0.5, 0.5]
    bt1.command = funcaoBotao
    bt1.refer = 'c'
    bt1.radius = 6
    #bt1.bordas = 1
    #bt1.cor = (-1, -1, -1)
    #bt1.cor = (arApp.corTextoSecundaria)
    #bt1.tamanho = [80,45]

    def sair():
        return 'finish'

    btSair = arApp.novoBotao()
    btSair.string = 'x'
    btSair.lugar = [0.99, 0.01]
    btSair.tamanho = [40, 40]
    btSair.corTexto = (255,0,0)
    btSair.tamanhoTexto = 30
    btSair.refer = 'nr'
    btSair.bordas = 1
    btSair.corBordas = (255,0,0)
    btSair.command = sair

    txMouse = arApp.novoTexto()
    txMouse.lugar = [0.5, 0.65]
    txMouse.refer = 'c'

    sq1 = arApp.novoSquare(
        lugar=[0.25, 0.25],
        tamanho=[0.5, 0.5]
    )
    sq1.active = False

    running = True
    while running:

        #arApp.drawSquare(lugar=[20, 500])
        #arApp.drawCircle(lugar=[100,300], cor=(0,0,0))
        #arApp.drawLine(ponto1=[100,100], ponto2=[350,350], cor=(0,255,0))

        txMouse.string = str(pygame.mouse.get_pos())
        
        saida = arApp.update()
        
        if saida == 'finish':
            running = False
