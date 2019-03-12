reserved = {
        'break': 	'BREAK',
        'case': 	'CASE',
        'chan': 	'CHAN',
        'const': 	'CONST',
        'continue': 	'CONTINUE',
        'default': 	'DEFAULT',
        'defer': 	'DEFER',
        'else': 	'ELSE',
        'fallthrough': 	'FALLTHROUGH',
        'for':		'FOR',
        'func': 	'FUNC',
        'go': 	 	'GO',
        'goto':		'GOTO',
        'if': 	 	'IF',
        'import': 	'IMPORT',
        'interface': 	'INTERFACE',
        'map': 	 	'MAP',
        'package': 	'PACKAGE',
        'range': 	'RANGE',
        'return': 	'RETURN',
        'select': 	'SELECT',
        'struct': 	'STRUCT',
        'switch': 	'SWITCH',
        'typecast': 'TYPECAST',
        'type': 	'TYPE',
        'var': 	 	'VAR',
        'nil':          'NIL',

        'true':         'TRUE',
        'false':        'FALSE',

        'uint8':        'UINT8',
        'uint16':       'UINT16',
        'uint32':       'UINT32',
        'uint64':       'UINT64',
        'int8':         'INT8',
        'int16':        'INT16',
        'int32':        'INT32',
        'int64':        'INT64',
        'float32':      'FLOAT32',
        'float64':      'FLOAT64',
        'byte':         'BYTE',
        'bool':         'BOOL',
        'uint':         'UINT',
        'int':          'INT',
        'uintptr':      'UINTPTR',
        'string':       'STRING'
}

operators = ['ADD', 'SUB', 'MUL', 'QUO', 'REM', 'AND', 'OR', 'XOR', 'SHL', 'SHR', 'AND_NOT', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'QUO_ASSIGN', 'REM_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN', 'SHL_ASSIGN', 'SHR_ASSIGN', 'AND_NOT_ASSIGN', 'LAND', 'LOR', 'ARROW', 'INC', 'DEC', 'EQL', 'LSS', 'GTR', 'ASSIGN', 'NOT', 'NEQ', 'LEQ', 'GEQ', 'DEFINE', 'ELLIPSIS', 'LPAREN', 'LBRACK', 'LBRACE', 'COMMA', 'PERIOD', 'RPAREN', 'RBRACK', 'RBRACE', 'SEMICOLON', 'COLON', 'FOR_COMP']

literals_ = ['IDENT', 'DECIMAL_LIT', 'OCTAL_LIT', 'HEX_LIT', 'FLOAT_LIT', 'TICK_STRING', 'QUOTE_STRING', 'STRING_LIT', 'RBANANA_BRACE', 'LBANANA_BRACE']

#special_tokens = ['ILLEGAL', 'EOF', 'COMMENT']
special_tokens = ['ILLEGAL', 'COMMENT']

tokens = special_tokens + literals_ + operators + list(reserved.values())

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_QUO = r'/'
t_REM = r'%'

t_AND = r'&'
t_OR =  r'\|'
t_XOR = r'\^'
t_SHL = r'(<<)'
t_SHR = r'(>>)'
t_AND_NOT = r'(&\^)'

t_ADD_ASSIGN = r'(\+=)'
t_SUB_ASSIGN = r'(-=)'
t_MUL_ASSIGN = r'(\*=)'
t_QUO_ASSIGN = r'(/=)'
t_REM_ASSIGN = r'(%=)'

t_AND_ASSIGN = r'(&=)'
t_OR_ASSIGN = r'(\|=)'
t_XOR_ASSIGN = r'(\^=)'
t_SHL_ASSIGN = r'(<<=)'
t_SHR_ASSIGN = r'(>>=)'
t_AND_NOT_ASSIGN = r'(&\^=)'

t_LAND = r'(&&)'
t_LOR = r'(\|\|)'
t_ARROW = r'(<-)'
t_INC = r'(\+\+)'
t_DEC = r'(--)'

t_EQL = r'(==)'
t_LSS = r'<'
t_GTR = r'>'
t_ASSIGN = r'='
t_NOT = r'!'

t_NEQ = r'(!=)'
t_LEQ = r'(<=)'
t_GEQ = r'(>=)'
t_DEFINE = r'(:=)'
t_ELLIPSIS = r'(\.\.\.)'

t_LPAREN = r'\('
t_LBRACK = r'\['
t_LBRACE = r'\{'
t_COMMA =  r','
t_PERIOD = r'\.'

t_RPAREN = r'\)'
t_RBRACK = r'\]'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COLON = r'\:'

# t_RBANANA_BRACE = r'\)\]'
# t_LBANANA_BRACE = r'\[\('

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
