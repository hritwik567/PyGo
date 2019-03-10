import numpy as np
import argparse
import sys
import os
import ply.lex as lex
import re
import csv
from lexer_tokens import *

def t_FOR_COMP(t):
    r'\|\|\|'
    return t

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENT')    # Check for reserved words
    return t

def t_FLOAT_LIT(t):
    r'(?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    if re.match(r'^0[0-7]+$', t.value):
        t.type = 'OCTAL_LIT'
        t.value = int(t.value, 8)
        return t
    elif t.value == '0' or re.match(r'^[1-9][0-9]*$', t.value):
        t.type = 'DECIMAL_LIT'
        t.value = int(t.value)
        return t
    elif re.match(r'^0[0-9]+$', t.value):
        t.type = 'ILLEGAL'
        return t
    else:
        t.value = float(t.value)
        return t

def t_HEX_LIT(t):
    r'0[xX][0-9a-fA-F]+'
    t.value = int(t[2:], 16)
    return t

def t_TICK_STRING(t):
    r'\`([^`])*\`'
    t.type = 'STRING_LIT'
    return t

def t_QUOTE_STRING(t):
    r'\"[^\"\\]*(?:\\.[^\"\\]*)*\"'
    if '\n' in t.value:
        t.type = 'ILLEGAL'
        return t
    t.type = 'STRING_LIT'
    return t

def t_COMMENT(t):
    r'(/\*([^*]|\n|(\*+([^*/]|\n)))*\*+/)|(//.*)'
    pass

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Build the lexer
lex.lex()

if __name__ == '__main__':
    f = open(sys.argv[1])
    data = f.read()
    f.close()

    lex.input(data)

    while True:
        tok = lex.token()
        if not tok:
            break      # No more input
        print(tok)
