import csv
import random
import sys

tokens = ['ILLEGAL', 'COMMENT', 'IDENT', 'DECIMAL_LIT', 'OCTAL_LIT', 'HEX_LIT', 'FLOAT_LIT', 'TICK_STRING', 'QUOTE_STRING', 'ADD', 'SUB', 'MUL', 'QUO', 'REM', 'AND', 'OR', 'XOR', 'SHL', 'SHR', 'AND_NOT', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'QUO_ASSIGN', 'REM_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN', 'SHL_ASSIGN', 'SHR_ASSIGN', 'AND_NOT_ASSIGN', 'LAND', 'LOR', 'ARROW', 'INC', 'DEC', 'EQL', 'LSS', 'GTR', 'ASSIGN', 'NOT', 'NEQ', 'LEQ', 'GEQ', 'DEFINE', 'ELLIPSIS', 'LPAREN', 'LBRACK', 'LBRACE', 'COMMA', 'PERIOD', 'RPAREN', 'RBRACK', 'RBRACE', 'SEMICOLON', 'COLON', 'FOR_COMP', 'BREAK', 'CASE', 'CHAN', 'CONST', 'CONTINUE', 'DEFAULT', 'DEFER', 'ELSE', 'FALLTHROUGH', 'FOR', 'FUNC', 'GO', 'GOTO', 'IF', 'IMPORT', 'INTERFACE', 'MAP', 'PACKAGE', 'RANGE', 'RETURN', 'SELECT', 'STRUCT', 'SWITCH', 'TYPE', 'VAR', 'NIL', 'TRUE', 'FALSE', 'UINT8', 'UINT16', 'UINT32', 'UINT64', 'INT8', 'INT16', 'INT32', 'INT64', 'FLOAT32', 'FLOAT64', 'BYTE', 'BOOL', 'UINT', 'INT', 'UINTPTR']

f = open(sys.argv[1] + '.cfg', 'w+')
cw = csv.writer(f, delimiter=',')
for i in tokens:
    cw.writerow([i]+['#%2x%2x%2x'%(random.randint(127,255), random.randint(127,255), random.randint(127,255))])
f.close()
