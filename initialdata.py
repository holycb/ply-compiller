import re as re

reserved = {
    'if': 'IF',
    'for': 'FOR',
    'else': 'ELSE',
    'while': 'WHILE',
    'elif': 'ELIF',
    'struct': 'STRUCT',
    'goto': "GOTO",
    'function': "FUNCTION",
    'skip': "SKIP",
    'return': "RETURN",
    'do': "DO",
    'boolean': "DECL_BOOLEAN",
    'float': "DECL_FLOAT",
    'int': "DECL_INTEGER",
    'string': "DECL_STRING",
    'array': "DECL_ARRAY"
}

tokens = [
    # Literals (identifier, integer constant, float constant, string constant)
    'ID', 'CONST_INTEGER', 'CONST_FLOAT', 'CONST_STRING', 'NULL', 'CONST_BOOLEAN',

    # Data type declaration
    'DATATYPE',

    # Comments
    'COMMENT',

    # Operators (+, -, *, /, %, %%, ||, |, &&, &, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'IDIVIDE',
    'LOR', 'BOR', 'LAND', 'BAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=)
    'ASSIGN',

    # Increment/decrement (++,--)
    'INCREMENT', 'DECREMENT',

    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'DOT', 'SEMI', 'COLON',

    # Other
    'NEWLINE'
] + list(reserved.values())

# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_IDIVIDE          = r'%'
t_MODULO           = r'%%'
t_BOR               = r'\|'
t_LOR              = r'\|\|'
t_BAND              = r'&'
t_LAND              = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Assignment operator

t_ASSIGN           = r'='

# Increment/decrement
t_INCREMENT        = r'\+\+'
t_DECREMENT        = r'--'

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_DOT              = r'\.'
t_SEMI             = r';'
t_COLON            = r':'

def t_CONST_BOOLEAN(t):
    r'\b(true|false)\b'
    return t

# Identifiers
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Integer literal
t_CONST_INTEGER = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Null literal
t_NULL = r'null'

# Floating literal
t_CONST_FLOAT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# Comment
def t_COMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
    return t
 
# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.value = None
    return t

def t_CONST_STRING(t):
    r'(\"|\')([^\\\n]|(\\.))*?(\"|\')'
    t.value = t.value[1:len(t.value) - 1]
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)