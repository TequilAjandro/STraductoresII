from Errors import *
from Table import *

"""
                        **********************   TOKEN   **********************
"""


class Token:

    # El constructor recibe el tipo de token del que se trata: int, float, operador
    # Y de ser un numero o nombre de variable se asigna, de lo contrario es nulo

    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    # Se sobreescribe la manera en la que se imprime el objeto

    def __repr__(self):
        if self.value:
            return f'{self.type} -> {self.value}'
        return f'{self.type}'

    # Regresa el valor del Token

    def Value(self):
        if self.value != None:
            return self.value

    # Regresa el tipo del Token

    def Type(self):
        return self.type


"""
**********************************************************************************************************
"""

"""
                        **********************   POSITION   **********************
"""


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def back(self, current_char=None):
        self.idx -= 1
        self.col -= 1

        if current_char == '\n':
            self.ln -= 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


"""
                        **********************   LEXER   **********************
"""


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def back(self):
        self.pos.back(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx - \
            1 > 0 else None

    def analyze(self):
        tokens = []

        while self.current_char != None:
            # print(self.current_char, '-> ', self.pos.idx)
            if self.current_char == '\t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_word())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(self.make_equality())
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_SEMI, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LCBRACK, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RCBRACK, pos_start=self.pos))
                self.advance()
            elif self.current_char == '&':
                tokens.append(self.make_logical_operator())
                self.advance()
            elif self.current_char == '|':
                tokens.append(self.make_logical_operator())
                self.advance()
            elif self.current_char == '#':
                tokens.append(Token(DIRECTIVE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '"':
                tokens.append(Token(TT_DQUOTATION, pos_start=self.pos))
                self.advance()
            elif self.current_char == "'":
                tokens.append(Token(TT_SQUOTATION, pos_start=self.pos))
                self.advance()
            elif self.current_char == '<':
                tokens.append(self.make_relational_operator())
                self.advance()
            elif self.current_char == '>':
                tokens.append(self.make_relational_operator())
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MODULE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '.':
                tokens.append(Token(TT_DOT, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                tokens.append(self.make_equality())
                self.advance()
            elif self.current_char == '$':
                tokens.append(Token(TT_DOLLAR, pos_start=self.pos))
                self.advance()
            elif self.current_char == '\n':
                self.advance()
            elif self.current_char == ' ':
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_word(self):
        word = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char not in DELIMITERS and self.current_char != None and (self.current_char in LETTERS or dot_count <= 1):
            if dot_count == 0:
                if self.current_char in LETTERS:
                    word += self.current_char
                elif self.current_char == '.':
                    word += self.current_char
                    dot_count += 1
            else:
                if self.current_char == 'h':
                    word += self.current_char
            self.advance()
        if word in KEYWORD:
            return Token(TT_KEYWORD, word, pos_start, self.pos)
        elif word.endswith('.h'):
            return Token(LIBRARY, word, pos_start, self.pos)
        else:
            # self.back()
            return Token(IDENTIFIER, word, pos_start, self.pos)

    def make_equality(self):
        pos_start = self.pos.copy()

        if self.current_char == '=':
            self.advance()
            if self.current_char != None and self.current_char == '=':
                return Token(TT_EQUALITY, '==', pos_start, self.pos)
            self.back()
            return Token(ASING, '=', pos_start, self.pos)
        else:
            self.advance()
            if self.current_char != None and self.current_char == '=':
                return Token(TT_EQUALITY, '!=', pos_start, self.pos)
            self.back()
            return Token(TT_NEGATION, '!', pos_start, self.pos)

    def make_logical_operator(self):
        pos_start = self.pos.copy()

        if self.current_char == '&':
            self.advance()
            if self.current_char != None and self.current_char == '&':
                return Token(TT_AND, '&&', pos_start, self.pos)
            return Token(TT_AMPERSON, '&', pos_start, self.pos)
        else:
            self.advance()
            if self.current_char != None and self.current_char == '|':
                return Token(TT_OR, '||', pos_start, self.pos)
            return Token(TT_BAR, '|', pos_start, self.pos)

    def make_relational_operator(self):
        pos_start = self.pos.copy()

        if self.current_char == '<':
            self.advance()
            if self.current_char != None and self.current_char == '=':
                return Token(TT_RELATIONAL, '<=', pos_start, self.pos)
            return Token(TT_RELATIONAL, '<', pos_start, self.pos)
        else:
            self.advance()
            if self.current_char != None and self.current_char == '=':
                return Token(TT_RELATIONAL, '>=', pos_start, self.pos)
            return Token(TT_RELATIONAL, '>', pos_start, self.pos)


"""
**********************************************************************************************************
"""
