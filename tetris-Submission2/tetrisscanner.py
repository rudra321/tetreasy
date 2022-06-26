from sly import Lexer

class TetrisLexer(Lexer):
    # Set of token names. 
    tokens = { KEYWORD, NUMBER, MOVE, ASSIGNOP,BOOLEAN,DELIMITER, ID, CONFIG, BLOCK, COLOR}

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['TRUE'] = 'BOOLEAN'
    ID['FALSE'] = 'BOOLEAN'
    ID['CONFIG'] = 'CONFIG'
    ID['ROWS'] = 'KEYWORD'
    ID['COLUMNS'] = 'KEYWORD'
    ID['ORIGIN'] = 'KEYWORD'
    ID['MUSIC'] = 'KEYWORD'
    ID['SPEED'] = 'KEYWORD'
    ID['NEXTQ'] = 'KEYWORD'
    ID['BLOCK1'] = 'BLOCK'
    ID['BLOCK2'] = 'BLOCK'
    ID['BLOCK3'] = 'BLOCK'
    ID['BLOCK4'] = 'BLOCK'
    ID['BLOCK5'] = 'BLOCK'
    ID['BLOCK6'] = 'BLOCK'
    ID['BLOCK7'] = 'BLOCK'
    ID['TIMER'] = 'KEYWORD'
    ID['TIMEDGAME'] = 'KEYWORD'
    ID['RIGHT'] = 'MOVE'
    ID['LEFT'] = 'MOVE'
    ID['SOFTDROP'] = 'MOVE'
    ID['HARDDROP'] = 'MOVE'
    ID['ROTATERIGHT'] = 'MOVE'
    ID['ROTATELEFT'] = 'MOVE'
    ID['PAUSE'] = 'MOVE'
    ID['RED'] = 'COLOR'
    ID['BLUE'] = 'COLOR'
    ID['GREEN'] = 'COLOR'
    ID['YELLOW'] = 'COLOR'
    ID['ORANGE'] = 'COLOR'
    ID['INDIGO'] = 'COLOR'
    ID['VIOLET'] = 'COLOR'
    ID['BLACK'] = 'COLOR'
    ID['RANDOM'] = 'COLOR'
    NUMBER  = r'\d+'
    ASSIGNOP  = r'='
    DELIMITER = r'\n'

    @_(r'//.*')
    def COMMENT(self, t):
        pass

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
    
if __name__ == '__main__':
    program = open('program.rpj','r')
    data = program.read()
    program.close()
    lexer = TetrisLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))


# KEYWORD = r'IF|ELSE'