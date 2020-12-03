"""
                        **********************   TOKENS   **********************
"""

DIGITS = '0123456789'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWYXZabcdefghijklmnopqrstuvwxyz'
ASING = 'ASSIGNMENT'
IDENTIFIER = 'ID'
DIRECTIVE = '#'
LIBRARY = 'LIBRARY'
DELIMITERS = [' ', ',', ';']
KEYWORD = ['return', 'int', 'float', 'string', 'char', 'stack', 'list', 'queue', 'tuple',
           'sort', 'cout', 'printf', 'scanf', 'include', 'void', 'public', 'private', 'class',
           'null', 'scanf_s', 'array', 'vector', 'define', 'extern', 'for', 'while', 'if', 'else', 'switch',
           'case', 'default', 'do', 'continue', 'getchar', 'cout', 'cin', 'gets', 'true', 'false']

TT_KEYWORD = 'KEYWORD'
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MULTIPLICATION'
TT_DIV = 'DIVISION'
TT_EXP = 'POWER'
TT_LPAREN = 'LEFT PARENTESIS'
TT_RPAREN = 'RIGHT PARENTESIS'
TT_COMA = 'COMA'
TT_SEMI = 'SEMICOLON'
TT_LCBRACK = 'LEFT CURVY BRACKET'
TT_RCBRACK = 'RIGHT CURVY BRACKET'
TT_AMPERSON = 'AMPERSON'
TT_BAR = 'VERTICAL BAR'
TT_DQUOTATION = 'DOUBLE QUOTATION MARKS'
TT_SQUOTATION = 'SIMPLE QUOTATION MARKS'
TT_LESSTHAN = 'LESS THAN'
TT_GREATERTHAN = 'GREATER THAN'
TT_MODULE = 'MODULE OPERATOR'
TT_DOLLAR = 'DOLLAR SIGN'
TT_RELATIONAL = 'RELATIONAL OPERATOR'
TT_NEGATION = 'NEGATION OPERATOR'
TT_EQUALITY = 'EQUALITY OPERATOR'
TT_OR = 'OR OPERATOR'
TT_AND = 'AND OPERATOR'
TT_DOT = 'DOT'
TT_EOF = 'EOF'
