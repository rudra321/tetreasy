from sly import Parser
from tetrisscanner import TetrisLexer

dictofkeys = {'K_BACKSPACE': 8, 'K_TAB': 9, 'K_CLEAR': 1073741980, 'K_RETURN': 13, 'K_PAUSE': 1073741896, 'K_ESCAPE': 27, 
'K_SPACE': 32, 'K_EXCLAIM': 33, 'K_HASH': 35, 'K_QUOTEDBL': 34, 'K_DOLLAR': 36, 'K_AMPERSAND': 38, 'K_QUOTE': 39, 'K_LEFTPAREN': 40,
'K_RIGHTPAREN': 41, 'K_ASTERISK': 42, 'K_PLUS': 43, 'K_COMMA': 44, 'K_MINUS': 45, 'K_PERIOD': 46, 'K_SLASH': 47, 'K_0': 48, 'K_1': 49, 
'K_2': 50, 'K_3': 51, 'K_4': 52, 'K_5': 53, 'K_6': 54, 'K_7': 55, 'K_8': 56, 'K_9': 57, 'K_COLON': 58, 'K_SEMICOLON': 59, 'K_LESS': 60, 
'K_EQUALS': 61, 'K_GREATER': 62, 'K_QUESTION': 63, 'K_AT': 64, 'K_LEFTBRACKET': 91, 'K_RIGHTBRACKET': 93, 'K_CARET': 94, 'K_UNDERSCORE': 95, 
'K_a': 97, 'K_b': 98, 'K_c': 99, 'K_d': 100, 'K_e': 101, 'K_f': 102, 'K_g': 103, 'K_h': 104, 'K_i': 105, 'K_j': 106, 'K_k': 107, 'K_l': 108,
'K_m': 109, 'K_n': 110, 'K_o': 111, 'K_p': 112, 'K_q': 113, 'K_r': 114, 'K_s': 115, 'K_t': 116, 'K_u': 117, 'K_v': 118, 'K_w': 119, 'K_x': 120,
'K_y': 121, 'K_z': 122, 'K_DELETE': 127, 'K_UP': 1073741906, 'K_DOWN': 1073741905, 'K_RIGHT': 1073741903, 'K_LEFT': 1073741904, 'K_INSERT': 1073741897,
'K_HOME': 1073741898, 'K_END': 1073741901, 'K_PAGEUP': 1073741899, 'K_PAGEDOWN': 1073741902, 'K_NUMLOCK': 1073741907, 'K_CAPSLOCK': 1073741881,
'K_SCROLLOCK': 1073741895, 'K_RSHIFT': 1073742053, 'K_LSHIFT': 1073742049, 'K_RCTRL': 1073742052, 'K_LCTRL': 1073742048, 'K_RALT': 1073742054, 'K_LALT': 1073742050}

class TetrisParser(Parser):
    
    tokens = TetrisLexer.tokens

    def __init__(self):
        self.names = {}
        self.blocktable = [True, True, True, True, True, True, True]
        self.colortable = ["RANDOM","RANDOM","RANDOM","RANDOM","RANDOM","RANDOM","RANDOM"]

    @_('KEYWORD ASSIGNOP NUMBER DELIMITER')
    def statement(self,p):
        self.names[p.KEYWORD]=int(p.NUMBER)

    @_('BLOCK ASSIGNOP BOOLEAN DELIMITER')
    def statement(self,p):
        # self.names[p.BLOCK]=p.BOOLEAN
        if(p.BLOCK=="BLOCK1"):
            if(p.BOOLEAN=="FALSE"):
                self.blocktable[0]=False
        if(p.BLOCK=="BLOCK2"):
            if(p.BOOLEAN=="FALSE"):
                self.blocktable[1]=False
        if(p.BLOCK=="BLOCK3"):
            if(p.BOOLEAN=="FALSE"):
                self.blocktable[2]=False
        if(p.BLOCK=="BLOCK4"):
            if(p.BOOLEAN=="FALSE"):
                self.blocktable[3]=False
        if(p.BLOCK=="BLOCK5"):
            if(p.BOOLEAN=="FALSE"):
                self.blocktable[4]=False
        if(p.BLOCK=="BLOCK6"):
            if(p.BOOLEAN=="FALSE"):
                self.blocktable[5]=False
        if(p.BLOCK=="BLOCK7"):
            if(p.BOOLEAN=="FALSE"):
                self.blocktable[6]=False

    @_('BLOCK ASSIGNOP COLOR DELIMITER')
    def statement(self,p):
        if(p.BLOCK=="BLOCK1"):
            self.colortable[0]=p.COLOR
        elif(p.BLOCK=="BLOCK2"):
            self.colortable[1]=p.COLOR
        elif(p.BLOCK=="BLOCK3"):
            self.colortable[2]=p.COLOR
        elif(p.BLOCK=="BLOCK4"):
            self.colortable[3]=p.COLOR
        elif(p.BLOCK=="BLOCK5"):
            self.colortable[4]=p.COLOR
        elif(p.BLOCK=="BLOCK6"):
            self.colortable[5]=p.COLOR
        elif(p.BLOCK=="BLOCK7"):
            self.colortable[6]=p.COLOR


    @_('CONFIG MOVE ID DELIMITER')
    def statement(self,p):
        if p.ID not in dictofkeys:
            print(p.ID + " is an invalid key. Using default value")
            pass
        self.names[p.MOVE]=dictofkeys[p.ID]

    @_('DELIMITER')
    def statement(self,p):
        pass
        
    def error(self, p):
        print("Error encountered during parsing")

    # @_('NUMBER')
    # def expr(self, p):
    #     print('number is ' + p.NUMBER)
    #     self.names[p.NUMBER] = p.NUMBER
    #     print(self.names)