

#{'type':'string','chars':[],'line':lineno, 'col':colno}
class Token:
    def __init__(self,type=None,line=None,col=None,chars=None):
        self.type = type
        self.line = line
        self.col = col # column
        self.chars = chars if chars is not None else []
        
    def __repr__(self):
        st = ''.join(self.chars)
        return self.type.upper() + '{' + st + '}'

class TokenList:
    def __init__(self):
        self.tokens = []
    def append(self, token):
        assert type(token) is Token
        self.tokens.append(token)    
    def __repr__(self):        
        st = ''
        for t in self.tokens:
           st += t.__repr__()
           st += '\n'
        return st