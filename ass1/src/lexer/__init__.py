import numpy as np
import argparse
import sys
import os
import ply.lex as lex
import re
import csv
from yattag import Doc, indent
from .lexer_tokens import *

def main():
    #parsing arguments
    parser = argparse.ArgumentParser(description='Configuration and Output filename')
    
    parser.add_argument('--cfg', type=str, default='../tests/cfg1/1.cfg',
                        help='Path to seen data file')
    parser.add_argument('--output', type=str, default=None,
                        help='Output html filename')
    args, infile = parser.parse_known_args()
    
    
    if len(infile)!=1:
        print('usage: provide 1 input file')
    
    infile = infile[0]
    
    if args.output == None:
        args.output = os.path.basename(infile).split('.')[0] + '.html'
    
    def t_FOR_COMP(t):
        r'\|\|\|'
        return t
    
    def t_IDENT(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'IDENT')    # Check for reserved words
        return t
    
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
        r'\"[^\"\\]*(?:\\.[^\"\\]*)*\"'
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
    
    # Build the lexer
    lexer = lex.lex()
    
    f = open(infile)
    data = f.read()
    f.close()
    
    # Give the lexer some input
    lexer.input(data)
    
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
                                for i in tok.value:
                                    if i == '\n':
                                        doc.stag('br')
                                    elif i == ' ':
                                        doc.asis('&nbsp;')
                                    else:
                                        text(i)
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
    
    f = open(args.output, 'w+')
    f.write(indent(doc.getvalue()))
    f.close()

if __name__ == "__main__":
    main()
