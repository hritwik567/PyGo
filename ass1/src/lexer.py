import numpy as np
import argparse
import sys
import os
import ply.lex as lex
import re
import csv
from yattag import Doc, indent

#parsing arguments
parser = argparse.ArgumentParser(description='Configuration and Output filename')

parser.add_argument('--cfg', type=str, default='../tests/cfg1/1.cfg',
                    help='Path to seen data file')
parser.add_argument('--out', type=str, default=None,
                    help='Output html filename')
args, infile = parser.parse_known_args()

if len(infile)!=1:
    print('usage: provide 1 input file')

infile = infile[0]

if args.out == None:
    args.out = os.path.basename(infile).split('.')[0] + '.html'

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
        'uintptr':      'UINTPTR'
}

operators = ['ADD', 'SUB', 'MUL', 'QUO', 'REM', 'AND', 'OR', 'XOR', 'SHL', 'SHR', 'AND_NOT', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'QUO_ASSIGN', 'REM_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN', 'SHL_ASSIGN', 'SHR_ASSIGN', 'AND_NOT_ASSIGN', 'LAND', 'LOR', 'ARROW', 'INC', 'DEC', 'EQL', 'LSS', 'GTR', 'ASSIGN', 'NOT', 'NEQ', 'LEQ', 'GEQ', 'DEFINE', 'ELLIPSIS', 'LPAREN', 'LBRACK', 'LBRACE', 'COMMA', 'PERIOD', 'RPAREN', 'RBRACK', 'RBRACE', 'SEMICOLON', 'COLON']

literals_ = ['IDENT', 'DECIMAL_LIT', 'OCTAL_LIT', 'HEX_LIT', 'FLOAT_LIT', 'TICK_STRING', 'QUOTE_STRING']

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

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENT')    # Check for reserved words
    return t

t_HEX_LIT = r'0[xX][0-9a-fA-F]+'

def t_FLOAT_LIT(t):
    r'(?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    if re.match(r'^0[0-7]+$', t.value):
        t.type = 'OCTAL_LIT'
        return t
    elif t.value == '0' or re.match(r'^[1-9][0-9]*$', t.value):
        t.type = 'DECIMAL_LIT'
        return t
    elif re.match(r'^0[0-9]+$', t.value):
        t.type = 'ILLEGAL'
        return t
    else:
        return t

def t_TICK_STRING(t):
    r'\`([^`])*\`'
    return t

def t_QUOTE_STRING(t):
    r'\"([^\"])*\"'
    if '\n' in t.value:
        t.type = 'ILLEGAL'
        return t
    return t

def t_COMMENT(t):
    r'(/\*([^*]|\n|(\*+([^*/]|\n)))*\*+/)|(//.*)'
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Build the lexer
lexer = lex.lex()

# data = """
# package main;

# import "fmt";

# func main() {
#         fmt.Println("Hello,
#         wow");
# }

# """
f = open(infile)
data = f.read()
f.close()

# Give the lexer some input
lexer.input(data)
# print(data)


# HTML Generator

config = dict([(r[0],r[1]) for r in csv.reader(open(args.cfg), delimiter=',')])

whitespace = '&nbsp;'
cum_length = 0          # cumuative length of program as string
prev_line_no = 1


doc, tag, text = Doc().tagtext()
with tag('html'):
    with tag('body'):
        with tag('div', style = 'display: flex;'):
            with tag('div', style = 'flex: 50%;'):
                with tag('span', klass = 'code'):
                    while True:
                        tok = lexer.token()
                        if not tok:
                            break
                        with tag('span', style = 'color: ' + config[tok.type]):
                            for i in range(tok.lineno - prev_line_no):
                                doc.stag('br')
                            for i in range(tok.lexpos - cum_length - (tok.lineno - prev_line_no)):
                                doc.asis('&nbsp;')
                            tok.value = tok.value.replace('\n', '<br>')
                            tok.value = tok.value.replace(' ', '&nbsp;')
                            doc.asis(tok.value)
                        prev_line_no = tok.lineno
                        cum_length = tok.lexpos + len(tok.value)
            with tag('div', style = 'flex: 50%;'): 
                with tag('table'):
                    with tag('tr'):
                        with tag('th'):
                            text('TOKEN')
                        with tag('th'):
                            text('COLOR')
                    for i in config:
                        with tag('tr'):
                            with tag('td'):
                                text(i)
                            with tag('td'):
                                doc.attr(bgcolor = config[i])
f = open(args.out, 'w+')
f.write(indent(doc.getvalue()))
f.close()


