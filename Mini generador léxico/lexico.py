"""""""""""""""""""""""""""""
"" TOKENS 
"""""""""""""""""""""""""""""
# TipoToken
TT_INT        = "INT"
TT_FLOAT      = "FLOAT"
TT_EQ         = "IGUAL"
TT_IDENTIFIER = "IDENTIFICADOR"
TT_ASIGN      = "ASIGNACION"

DIGIT = '0123456789'
LETTERS = 'abcdefghijklmnopqrstwxyzABCDEFGHIJKLMNOPQRSTWXYZ'

class Token:
    def __init__(self, tpe, value=None):
        self._type = tpe
        self._value = value

    def __repr__(self):
        if self._value: return f'{self._type}:{self._value}'
        return f'{self._type}' 

    # Regresa el valor del Token
    def Value(self):
        if self._value != None:
            return self._value
    # Regresa el tipo del Token
    def Type(self):
        return self._type
""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""
"" ERRORES
"""""""""""""""""""""""""""""
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self._pos_start = pos_start
        self._pos_end = pos_end
        self._error_name = error_name
        self._details = details
    
    def as_string(self):
        result  = f'{self._error_name}: {self._details}\n'
        pos = self._pos_start._ln+1
        result += f'Archivo {self._pos_start._fn}, line {pos}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Caracter Invalido', details)

# Error en la definicion de la variable
class IllegalVariableError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Declaración de variable invalida ', details)

class Position:
    def __init__(self, idx, ln, col, fn, fntxt):
        self._idx = idx
        self._ln = ln
        self._col = col
        self._fn = fn
        self._fntxt = fntxt

    def advance(self, current_char):
        self._idx += 1
        self._col += 1
        if current_char == '\n':
            self._ln += 1
            self._col += 0
        return self
    
    def copy(self):
        return Position(self._idx, self._ln, self._col, self._fn, self._fntxt)
""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""
"" Mini analizador léxico
"""""""""""""""""""""""""""""
class Lexer:
    def __init__(self, fn, text):
        self._fn = fn
        self._text = text
        self._pos = Position(-1, 0, -1, fn, text)        
        self._current_char = None
        self.advance()
    
    def advance(self):
        self._pos.advance(self._current_char)
        self._current_char = self._text[self._pos._idx] if self._pos._idx < len(self._text) else None
        
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self._current_char != None and self._current_char in DIGIT + '.':
            if self._current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self._current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

    def make_identifier(self):
        id_str = ''
        pos = self._pos.copy()
        while self._current_char != None and self._current_char in LETTERS:
            id_str += self._current_char
            self.advance()
        return Token(TT_IDENTIFIER, id_str)

    def analyze(self):
        tokens = []
        count = self._text.count('=')

        if count > 1:
            pos = self._pos.copy()
            char = self._current_char
            self.advance()
            return [], IllegalVariableError(pos, self._pos, '-> ', self._text)
        elif count == 1:
            name = self._text.split('=')[0]
            tokens.append(Token(TT_IDENTIFIER, name))
            for n in range(len(name)):
               self.advance()
            tokens.append(self.make_tokens(tokens)[0])
            return tokens, None
        else:
            tokens = self.make_tokens(tokens)[0]
            return tokens, None

    def make_tokens(self, tokens):
        # tokens = []

        while self._current_char != None:
            if self._current_char in '\t' or self._current_char == ' ':
                self.advance()
            elif self._current_char in DIGIT:
                tokens.append(self.make_number())
            elif self._current_char == '=':
                tokens.append(Token(TT_ASIGN))
                self.advance()
            else:
                pos = self._pos.copy()
                char = self._current_char
                self.advance()
                return [], IllegalCharError(pos, self._pos, "'" + char + "'")
        return tokens, None
""""""""""""""""""""""""""

def make_identifier(text):
    if ' '.join(map(str, text)).count('=') == 1:
       num = float(' '.join(map(str, text)).split('=')[-1])
    else:
        num = float(text)
    return num

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.analyze()
    return tokens, error