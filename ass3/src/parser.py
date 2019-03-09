#!/usr/bin/env python3
import ply.yacc as yacc
import sys
import argparse
import lexer
import os
from symbol_table import SymbolTable
from node import Node
tokens = lexer.tokens

#parsing arguments
parser = argparse.ArgumentParser(description = "Output filename")
parser.add_argument("--out", type=str, default=None,
                    help="Output IR filename")

args, infile = parser.parse_known_args()

if len(infile)!=1:
    print('usage: provide 1 input file')

infile = infile[0]

if args.out == None:
    args.out = os.path.basename(infile).split('.')[0] + ".ir"


#-------------------SYMBOL TABLE STUFF-----------------------------
scopes_ctr = 0
scopes = [SymbolTable()]
current_scope = 0
scope_stack = [0]
root_node = None
import_dict = dict()
#------------------------------------------------------------------

def add_to_import_table(package, ident):
    global import_dict
    if package in import_dict:
        if ident in import_dict[package]:
            raise NameError(ident + " already imported from " + package)
        else:
            import_dict[package] += ident
    else:
        import_dict[package] = [ident]

def in_scope(ident):
    global scope_stack, scopes
    for scope in scope_stack[::-1]:
        if scopes[scope].look_up(ident):
            return True
    return False

def add_scope():
    global scope_stack, scopes, current_scope, scopes_ctr
    scopes_ctr += 1
    previous_scope = current_scope
    current_scope = scopes_ctr
    scope_stack += [current_scope]
    scopes += [SymbolTable()]
    scopes[current_scope].set_parent(previous_scope)

def end_scope():
    global scope_stack, current_scope
    scope_stack.pop()
    current_scope = scope_stack[-1]

def find_scope(ident):
    global scope_stack, scopes
    for scope in scope_stack[::-1]:
        if scopes[scope].look_up(ident):
            return scope
    raise NameError("Identifier " + ident + " is not in any scope")

def find_info(ident, scope = None):
    global scope_stack, scopes
    if scope != None:
        temp = scopes[scope].get_info(ident)
        if temp != None:
            return temp
        raise NameError("Identifier " + ident + " is not in this scope")

    for scope in scope_stack[::-1]:
        if scopes[scope].look_up(ident):
            return scopes[scope].get_info(ident)
    raise NameError("Identifier " + ident + " is not in any scope")


def mytuple(arr):
    return tuple(arr)

def p_epsilon(p):
    '''epsilon : '''
    p[0] = Node()

def p_package_name(p):
    '''package_name : IDENT'''
    p[0] = Node()
    p[0].id_list += [p[1]]


def p_package_clause(p):
    '''package_clause : PACKAGE package_name'''
    p[0] = p[2]


def p_import_path(p):
    '''import_path : STRING_LIT'''
    p[0] = Node()
    p[0].id_list += [p[1]]
    #TODO: should also add to type_list

def p_import_spec(p):
    '''import_spec  : import_path
                    | PERIOD import_path
                    | package_name import_path'''
    global scopes, current_scope
    if len(p) == 2:
        p[0] = p[1]
        if in_scope(p[1].id_list[0]):
            raise NameError("Package " + p[1].id_list[0] + " already imported")
        else:
            add_to_import_table(p[1].id_list[0], None)
            scopes[current_scope].insert(p[1].id_list[0], "package")

    elif p[1] == ".":
        p[0] = Node()
        # p[0].id_list += [p[1] + " " + p[2].id_list[0]]
        add_to_import_table(p[2].id_list[0], ".")
    else:
        p[0] = p[1]
        # p[0].id_list = [p[0].id_list[0] + " " + p[2].id_list[0]]
        if in_scope(p[0].id_list[0]):
            raise NameError("Package " + p[0].id_list[0] + " already imported")
        else:
            add_to_import_table(p[2].id_list[0], p[0].id_list[0])
            scopes[current_scope].insert(p[0].id_list[0], "package")


def p_import_spec_rep(p):
    '''import_spec_rep  : import_spec_rep import_spec semicolon_opt
                        | epsilon'''
    p[0] = p[1]
    # if len(p) == 4:
        # p[0].id_list += p[2].id_list

def p_import_decl(p):
    '''import_decl  : IMPORT import_spec
                    | IMPORT LPAREN import_spec_rep RPAREN'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[3]

def p_import_decl_rep(p):
    '''import_decl_rep  : import_decl_rep import_decl semicolon_opt
                        | epsilon'''
    p[0] = p[1]
    if len(p) == 4:
        p[0].code += p[2].code

def p_top_level_decl_rep(p):
    '''top_level_decl_rep   : top_level_decl_rep top_level_decl semicolon_opt
                            | epsilon'''
    p[0] = p[1]
    if len(p) == 4:
        p[0].code += p[2].code


def p_source_file(p):
    '''source_file  : package_clause semicolon_opt import_decl_rep top_level_decl_rep'''
    p[0] = p[1]
    p[0].code += p[3].code
    p[0].code += p[4].code

######################################################## SACRED #############################################################################
def p_add_scope(p):
    '''add_scope    :'''
    add_scope()

def p_end_scope(p):
    '''end_scope    :'''
    end_scope()

def p_add_scope_with_lbrace(p):
    '''add_scope_with_lbrace    : LBRACE'''
    add_scope()

def p_end_scope_with_rbrace(p):
    '''end_scope_with_rbrace    : RBRACE'''
    end_scope()

def p_semicolon_opt(p):
    '''semicolon_opt    : SEMICOLON
                        | epsilon'''

def p_type_token(p):
    '''type_token   : UINT8
                    | UINT16
                    | UINT32
                    | UINT64
                    | INT8
                    | INT16
                    | INT32
                    | INT64
                    | FLOAT32
                    | FLOAT64
                    | BYTE
                    | BOOL
                    | UINT
                    | INT
                    | UINTPTR'''
    p[0] = mytuple(["type_token"] + p[1:])



def p_type(p):
    '''type : type_token
            | type_lit
            | TYPE IDENT'''
    # check_shivansh
    # Arpit LPAREN type RPAREN removed from RHS
    p[0] = mytuple(["type"] + p[1:])

def p_operand_name(p):
    '''operand_name : IDENT'''
    p[0] = mytuple(["operand_name"] + p[1:])

def p_type_name(p):
    '''type_name    : IDENT'''
    # check_shivansh
    #Hritvik remove qualified_ident from type_name
    p[0] = mytuple(["type_name"] + p[1:])

def p_type_lit(p):
    '''type_lit : array_type
                | struct_type
                | pointer_type
                | function_type
                | interface_type
                | slice_type
                | map_type'''
    p[0] = mytuple(["type_lit"] + p[1:])

def p_array_type(p):
    '''array_type   : LBRACK array_length RBRACK element_type'''
    p[0] = mytuple(["array_type"] + p[1:])

def p_array_length(p):
    '''array_length : expression'''
    p[0] = mytuple(["array_length"] + p[1:])

def p_element_type(p):
    '''element_type : type'''
    p[0] = mytuple(["element_type"] + p[1:])

def p_slice_type(p):
    '''slice_type   : LBRACK RBRACK element_type'''
    p[0] = mytuple(["slice_type"] + p[1:])

def p_struct_type(p):
    '''struct_type  : STRUCT LBRACE field_decl_rep RBRACE'''
    p[0] = mytuple(["struct_type"] + p[1:])

def p_field_decl_rep(p):
    '''field_decl_rep   : field_decl_rep field_decl semicolon_opt
                        | epsilon'''
    p[0] = mytuple(["field_decl_rep"] + p[1:])

def p_field_decl(p):
    '''field_decl   : embedded_field
                    | identifier_list type'''
    p[0] = mytuple(["field_decl"] + p[1:])

def p_embedded_field(p):
    '''embedded_field   : MUL type_name
                        | type_name'''
    p[0] = mytuple(["embedded_field"] + p[1:])

def p_pointer_type(p):
    '''pointer_type : MUL base_type'''
    p[0] = mytuple(["pointer_type"] + p[1:])

def p_base_type(p):
    '''base_type    : type'''
    p[0] = mytuple(["base_type"] + p[1:])

def p_function_type(p):
    '''function_type    : FUNC signature'''
    p[0] = mytuple(["function_type"] + p[1:])

def p_signature(p):
    '''signature    : parameters result'''
    p[0] = mytuple(["signature"] + p[1:])

def p_result(p):
    '''result   : parameters
                | type'''
    p[0] = mytuple(["result"] + p[1:])

def p_parameters(p):
    '''parameters   : LPAREN RPAREN
                    | LPAREN parameter_list comma_opt RPAREN'''
    p[0] = mytuple(["parameters"] + p[1:])

def p_parameter_list(p):
    '''parameter_list   : parameter_decl parameter_decl_rep '''
    p[0] = mytuple(["parameter_list"] + p[1:])

def p_parameter_decl_rep(p):
    '''parameter_decl_rep   : parameter_decl_rep COMMA parameter_decl
                            | epsilon'''
    p[0] = mytuple(["parameter_decl_rep"] + p[1:])

def p_parameter_decl(p):
    '''parameter_decl   : identifier_list_opt ellipsis_opt type '''
    p[0] = mytuple(["parameter_decl"] + p[1:])

def p_identifier_list_opt(p):
    '''identifier_list_opt  : identifier_list
                            | epsilon'''
    p[0] = mytuple(["identifier_list_opt"] + p[1:])

def p_interface_type(p):
    '''interface_type   : INTERFACE LBRACE method_spec_rep RBRACE '''
    p[0] = mytuple(["interface_type"] + p[1:])

def p_method_spec_rep(p):
    '''method_spec_rep  : method_spec_rep method_spec semicolon_opt
                        | epsilon'''
    p[0] = mytuple(["method_spec_rep"] + p[1:])

def p_method_spec(p):
    '''method_spec  : method_name signature
                    | interface_type_name'''
    p[0] = mytuple(["method_spec"] + p[1:])

def p_method_name(p):
    '''method_name  : IDENT'''
    p[0] = mytuple(["method_name"] + p[1:])

def p_interface_type_name(p):
    '''interface_type_name  : type_name'''
    p[0] = mytuple(["interface_type_name"] + p[1:])

def p_map_type(p):
    '''map_type : MAP LBRACK key_type RBRACK element_type'''
    p[0] = mytuple(["map_type"] + p[1:])

def p_key_type(p):
    '''key_type : type'''
    p[0] = mytuple(["key_type"] + p[1:])

def p_declaration(p):
    '''declaration  : const_decl
                    | type_decl
                    | var_decl'''
    p[0] = mytuple(["declaration"] + p[1:])

def p_top_level_decl(p):
    '''top_level_decl   : declaration
                        | function_decl
                        | method_decl'''
    p[0] = mytuple(["top_level_decl"] + p[1:])

def p_const_decl(p):
    '''const_decl   : CONST const_spec
                    | CONST LPAREN const_spec_rep RPAREN'''
    p[0] = mytuple(["const_decl"] + p[1:])

def p_const_spec_rep(p):
    '''const_spec_rep   : const_spec_rep const_spec semicolon_opt
                        | epsilon'''
    p[0] = mytuple(["const_spec_rep"] + p[1:])

def p_const_spec(p):
    '''const_spec   : identifier_list
                    | identifier_list type_opt ASSIGN expression_list'''
    p[0] = mytuple(["const_spec"] + p[1:])

def p_type_opt(p):
    '''type_opt : type
                | epsilon'''
    p[0] = mytuple(["type_opt"] + p[1:])

def p_type_decl(p):
    '''type_decl    : TYPE type_spec
                    | type LPAREN type_spec_rep RPAREN'''
    p[0] = mytuple(["type_decl"] + p[1:])

def p_type_spec_rep(p):
    '''type_spec_rep    : type_spec_rep type_spec semicolon_opt
                        | epsilon'''
    p[0] = mytuple(["type_spec_rep"] + p[1:])

def p_type_spec(p):
    '''type_spec    : alias_decl
                    | type_def'''
    p[0] = mytuple(["type_spec"] + p[1:])

def p_alias_decl(p):
    '''alias_decl   : IDENT ASSIGN type'''
    p[0] = mytuple(["alias_decl"] + p[1:])

def p_type_def(p):
    '''type_def : IDENT type'''
    p[0] = mytuple(["type_def"] + p[1:])

def p_var_decl(p):
    '''var_decl : VAR var_spec
                | VAR LPAREN var_spec_rep RPAREN'''
    p[0] = mytuple(["var_decl"] + p[1:])

def p_var_spec_rep(p):
    '''var_spec_rep : var_spec_rep var_spec semicolon_opt
                    | epsilon'''
    p[0] = mytuple(["var_spec_rep"] + p[1:])

def p_var_spec(p):
    '''var_spec : identifier_list type expr_list_assign_opt
                | identifier_list ASSIGN expression_list'''
    p[0] = mytuple(["var_spec"] + p[1:])

def p_expr_list_assign_opt(p):
    '''expr_list_assign_opt : ASSIGN expression_list
                            | epsilon'''
    p[0] = mytuple(["expr_list_assign_opt"] + p[1:])

def p_short_val_decl(p):
    '''short_val_decl   : IDENT DEFINE expression'''
    # '''short_val_decl   : identifier_list DEFINE expression_list'''
    # Arpit: mutiple identifiers can be defined
    p[0] = mytuple(["short_val_decl"] + p[1:])

def p_function_decl(p):
    '''function_decl    : FUNC function_name add_scope function end_scope
                        | FUNC function_name add_scope signature end_scope semicolon_opt'''
    #TODO: verify whether we need to add scope at the time of signature declaration
    global scopes, current_scope
    if len(p) == 6:
        if in_scope(p[2]):
            raise NameError("Function " + p[2] + " already defined")
        else:
            scopes[current_scope].insert(p[2], "function")
            p[0] = Node()
            p[0].code += p[4].code
    else:
        if in_scope("signature_" + p[2]):
            raise NameError("Signature " + p[2] + " already defined")
        else:
            scopes[current_scope].insert("signature_" + p[2], "signature")
            p[0] = Node()

def p_function_name(p):
    '''function_name    : IDENT'''
    p[0] = p[1]

def p_function(p):
    '''function : signature function_body'''
    p[0] = mytuple(["function"] + p[1:])

def p_function_body(p):
    '''function_body    : block'''
    p[0] = mytuple(["function_body"] + p[1:])

def p_method_decl(p):
    '''method_decl  : FUNC receiver method_name function
                    | FUNC receiver method_name signature'''
    p[0] = mytuple(["method_decl"] + p[1:])

def p_receiver(p):
    '''receiver : parameters'''
    p[0] = mytuple(["receiver"] + p[1:])

def p_operand(p):
    '''operand  : literal
                | operand_name
                | LPAREN expression RPAREN'''
    # check_shivansh
    # method_expr removed from the RHS of production and added to primary_expr directly
    # method and LPAREN expression RPAREN should may be removed
    p[0] = mytuple(["operand"] + p[1:])

def p_literal(p):
    '''literal  : basic_lit
                | composite_lit
                | function_lit'''
    p[0] = mytuple(["literal"] + p[1:])

def p_basic_lit(p):
    '''basic_lit    : int_lit
                    | FLOAT_LIT
                    | STRING_LIT '''
    #Add imaginary and rune lit
    p[0] = mytuple(["basic_lit"] + p[1:])

def p_int_lit(p):
    '''int_lit  : DECIMAL_LIT
                | OCTAL_LIT
                | HEX_LIT'''
    p[0] = mytuple(["int_lit"] + p[1:])


def p_qualified_ident(p):
    '''qualified_ident  : package_name PERIOD IDENT'''
    p[0] = mytuple(["qualified_ident"] + p[1:])

def p_composite_lit(p):
    '''composite_lit    : literal_type literal_value'''
    p[0] = mytuple(["composite_lit"] + p[1:])

def p_literal_type(p):
    '''literal_type : struct_type
                    | array_type
                    | slice_type
                    | map_type
                    | type_name
                    | LBRACK ELLIPSIS RBRACK element_type'''
    p[0] = mytuple(["literal_type"] + p[1:])

def p_literal_value(p):
    '''literal_value    : LBRACE RBRACE
                        | LBRACE element_list comma_opt RBRACE'''

def p_element_list(p):
    '''element_list : keyed_element keyed_element_rep'''
    p[0] = mytuple(["element_list"] + p[1:])

def p_keyed_element_rep(p):
    '''keyed_element_rep    : keyed_element_rep COMMA keyed_element
                            | epsilon'''
    p[0] = mytuple(["keyed_element_rep"] + p[1:])

def p_keyed_element(p):
    '''keyed_element    : key COLON element
                        | element'''
    p[0] = mytuple(["element"] + p[1:])

def p_key(p):
    '''key  : field_name
            | expression
            | literal_value'''
    p[0] = mytuple(["key"] + p[1:])

def p_field_name(p):
    '''field_name : IDENT'''
    p[0] = mytuple(["field_name"] + p[1:])

def p_element(p):
    '''element  : expression
                | literal_value'''
    p[0] = mytuple(["element"] + p[1:])

def p_function_lit(p):
    '''function_lit : FUNC function'''
    p[0] = mytuple(["function_lit"] + p[1:])


# conversion deleted form the RHS of the primary expression
def p_primary_expr(p):
    '''primary_expr : operand
                    | conversion
                    | method_expr arguments
                    | primary_expr selector
                    | primary_expr index
                    | primary_expr slice
                    | primary_expr arguments'''
    # check_shivansh
    # | operand_selector
    # | method_expr LPAREN arguments_for_method_expr RPAREN
    # since we already have method_expr we can remove primary_expr arguments_for_method_expr
    # but make sure of test cases : a.b.c(d,e)      x.a = b     foo(a,b)    etc.
    # operand selector in RHS becomes redundant; never gets used
    # slice may need to be removed from RHS
    # typeassertion removed from RHS of above production
    p[0] = mytuple(["primary_expr"] + p[1:])

def p_selector(p):
    '''selector : PERIOD IDENT'''
    p[0] = mytuple(["selector"] + p[1:])

def p_index(p):
    '''index    : LBRACK expression RBRACK'''
    p[0] = mytuple(["index"] + p[1:])

def p_slice(p):
    '''slice    : LBRACK expression_opt COLON expression_opt RBRACK
                | LBRACK expression_opt COLON expression COLON expression RBRACK'''
    p[0] = mytuple(["slice"] + p[1:])

def p_type_assertion(p):
    '''type_assertion   : PERIOD LPAREN type RPAREN'''
    p[0] = mytuple(["type_assertion"] + p[1:])

def p_arguments(p):
    '''arguments    : LPAREN RPAREN
                    | LPAREN expression_list ellipsis_opt comma_opt RPAREN
                    | LPAREN type expr_list_comma_opt ellipsis_opt comma_opt RPAREN'''
    # check_shivansh
    # lst RHS may have to be removed
    p[0] = mytuple(["arguments"] + p[1:])

def p_expr_list_comma_opt(p):
    '''expr_list_comma_opt  : COMMA expression_list
                            | epsilon'''
    p[0] = mytuple(["expr_list_comma_opt"] + p[1:])

def p_ellipsis_opt(p):
    '''ellipsis_opt : ELLIPSIS
                    | epsilon'''
    p[0] = mytuple(["ellipsis_opt"] + p[1:])

def p_method_expr(p):
    '''method_expr  : receiver_type PERIOD method_name'''
    p[0] = mytuple(["method_expr"] + p[1:])

# ReceiverType  = TypeName | "(" "*" TypeName ")" | "(" ReceiverType ")" .
def p_receiver_type(p):
    '''receiver_type    : type_name'''
    # Removed some RHS from production
    # couldn't find any of its use
    p[0] = mytuple(["receiver_type"] + p[1:])

def p_expression(p):
    '''expression   : unary_expr
                    | expression LOR expression
                    | expression LAND expression
                    | expression EQL expression
                    | expression NEQ expression
                    | expression LSS expression
                    | expression LEQ expression
                    | expression GTR expression
                    | expression GEQ expression
                    | expression ADD expression
                    | expression SUB expression
                    | expression OR expression
                    | expression XOR expression
                    | expression MUL expression
                    | expression QUO expression
                    | expression REM expression
                    | expression SHL expression
                    | expression SHR expression
                    | expression AND expression
                    | expression AND_NOT expression'''
    p[0] = mytuple(["expression"] + p[1:])

def p_unary_expr(p):
    '''unary_expr   : primary_expr
                    | unary_op unary_expr'''
    p[0] = mytuple(["unary_expr"] + p[1:])

def p_unary_op(p):
    '''unary_op : ADD
                | SUB
                | MUL
                | AND
                | NOT'''
    #TODO: can add more here
    p[0] = mytuple(["unary_op"] + p[1:])

def p_expression_opt(p):
    '''expression_opt   : expression
                        | epsilon'''
    p[0] = mytuple(["expression_opt"] + p[1:])

def p_expression_list(p):
    '''expression_list  : expression expression_rep'''
    p[0] = mytuple(["expression_list"] + p[1:])

def p_expression_rep(p):
    '''expression_rep   : COMMA expression expression_rep
                        | epsilon'''
    p[0] = mytuple(["expression_rep"] + p[1:])

def p_identifier_list(p):
    '''identifier_list  : identifier_list COMMA IDENT
                        | IDENT'''
    p[0] = mytuple(["identifier_list"] + p[1:])

def p_statement_list(p):
    '''statement_list   : statement_rep'''
    p[0] = mytuple(["statement_list"] + p[1:])

def p_statement_rep(p):
    '''statement_rep    : statement semicolon_opt statement_rep
                        | epsilon'''
    p[0] = mytuple(["statement_rep"] + p[1:])

def p_block(p):
    '''block    : LBRACE statement_list RBRACE'''
    p[0] = mytuple(["block"] + p[1:])

def p_conversion(p):
    '''conversion   : TYPECAST type_token LPAREN expression RPAREN'''
    # check prakhar TYPECAST is added
    # check prakhar comma is removed
    p[0] = mytuple(["conversion"] + p[1:])

def p_comma_opt(p):
    '''comma_opt    : COMMA
                    | epsilon'''
    p[0] = mytuple(["comma_opt"] + p[1:])

######################################################## SACRED #############################################################################

def p_statement(p):
    '''statement    : declaration
                    | labeled_stmt
                    | simple_stmt
                    | return_stmt
                    | break_stmt
                    | continue_stmt
                    | goto_stmt
                    | fallthrough_stmt
                    | add_scope_with_lbrace statement_list end_scope_with_rbrace
                    | if_stmt
                    | switch_stmt
                    | for_stmt
                    | defer_stmt'''
    p[0] = mytuple(["statement"] + p[1:])

def p_simple_stmt(p):
    '''simple_stmt  : epsilon
                    | expression_stmt
                    | inc_dec_stmt
                    | assignment
                    | short_val_decl'''
    p[0] = mytuple(["simple_stmt"] + p[1:])

def p_labeled_stmt(p):
    '''labeled_stmt : label COLON statement'''
    if in_scope(p[1]):
        raise NameError("Label " + p[1] + " already defined")
    else:
        global scopes
        scopes[current_scope].insert(p[1], "label")

def p_expression_stmt(p):
    '''expression_stmt  : expression'''
    p[0] = mytuple(["expression_stmt"] + p[1:])

def p_inc_dec_stmt(p):
    '''inc_dec_stmt : expression INC
                    | expression DEC'''
    p[0] = mytuple(["inc_dec_stmt"] + p[1:])

def p_assignment(p):
    '''assignment   : expression_list assign_op expression_list'''
    #Hritvik canges expression_list to identifier_list before assign_op
    p[0] = mytuple(["assignment"] + p[1:])

def p_assign_op(p):
    '''assign_op    : ASSIGN
                    | ADD_ASSIGN
                    | SUB_ASSIGN
                    | MUL_ASSIGN
                    | QUO_ASSIGN
                    | REM_ASSIGN
                    | AND_ASSIGN
                    | OR_ASSIGN
                    | XOR_ASSIGN
                    | SHL_ASSIGN
                    | SHR_ASSIGN
                    | AND_NOT_ASSIGN'''
    p[0] = mytuple(["assign_op"] + p[1:])

def p_if_stmt(p):
    '''if_stmt  : IF expression add_scope block end_scope
                | IF expression add_scope block end_scope ELSE add_scope block end_scope
                | IF expression add_scope block end_scope ELSE if_stmt'''
    p[0] = mytuple(["if_stmt"] + p[1:])

def p_switch_stmt(p):
    '''switch_stmt  : expr_switch_stmt'''
    p[0] = mytuple(["switch_stmt"] + p[1:])

def p_expr_switch_stmt(p):
    '''expr_switch_stmt : SWITCH expression_opt add_scope LBRACE expr_case_clause_rep RBRACE end_scope'''
    p[0] = mytuple(["expr_switch_stmt"] + p[1:])

def p_expr_case_clause_rep(p):
    '''expr_case_clause_rep : expr_case_clause_rep expr_case_clause
                            | epsilon'''
    p[0] = mytuple(["expr_case_clause_rep"] + p[1:])

def p_expr_case_clause(p):
    '''expr_case_clause : expr_switch_case COLON statement_list'''
    p[0] = mytuple(["expr_case_clause"] + p[1:])

def p_expr_switch_case(p):
    '''expr_switch_case : CASE expression_list
                        | DEFAULT'''
    p[0] = mytuple(["expr_switch_case"] + p[1:])

def p_for_stmt(p):
    '''for_stmt : FOR add_scope block end_scope
                | FOR add_scope condition block end_scope
                | FOR add_scope for_clause block end_scope
                | FOR add_scope range_clause block end_scope'''
    p[0] = mytuple(["for_stmt"] + p[1:])

def p_for_clause(p):
    '''for_clause   : init_stmt post_init_stmt'''
    p[0] = mytuple(["for_clause"] + p[1:])

def p_post_init_stmt(p):
    '''post_init_stmt    : SEMICOLON condition_opt SEMICOLON post_stmt
                    | epsilon'''
    p[0] = mytuple(["post_init_stmt"] + p[1:])


def p_post_stmt(p):
    '''post_stmt    : simple_stmt
                    | epsilon'''
    p[0] = mytuple(["post_stmt"] + p[1:])

def p_init_stmt(p):
    '''init_stmt    : simple_stmt
                    | epsilon'''
    p[0] = mytuple(["init_stmt"] + p[1:])

def p_condition(p):
    '''condition    : expression'''
    p[0] = mytuple(["condition"] + p[1:])

def p_condition_opt(p):
    '''condition_opt    : condition
                        | epsilon'''
    p[0] = mytuple(["condition_opt"] + p[1:])

def p_range_clause(p):
    '''range_clause : RANGE expression
                    | expression_list ASSIGN RANGE expression
                    | identifier_list DEFINE RANGE expression'''
    p[0] = mytuple(["range_clause"] + p[1:])

def p_return_stmt(p):
    '''return_stmt  : RETURN
                    | RETURN expression_list'''
    p[0] = mytuple(["return_stmt"] + p[1:])

def p_fallthrough_stmt(p):
    '''fallthrough_stmt : FALLTHROUGH'''
    p[0] = Node()
    p[0].code += ["fallthrough"] #TODO: WTF is this

def p_defer_stmt(p):
   '''defer_stmt  : DEFER expression'''
   p[0] = Node()
   p[0].code += ["defer"] + p[2].code #TODO: WTF is this

def p_goto_stmt(p):
    '''goto_stmt  : GOTO label'''
    if !in_scope(p[2]):
        raise NameError("Label " + p[2] + " not defined")
    p[0] = Node()
    p[0].code += ["goto", p[2]] #TODO: change this

def p_continue_stmt(p):
    '''continue_stmt    : CONTINUE label
                        | CONTINUE'''
    p[0] = Node()
    if len(p) == 3:
        if !in_scope(p[2]):
            raise NameError("Label " + p[2] + " not defined")
        p[0].code += ["continue", p[2]] #TODO: change this
    else:
        p[0].code += ["continue"] #TODO: change this to jump to end of the loop

def p_break_stmt(p):
    '''break_stmt   : BREAK label
                    | BREAK'''
    p[0] = Node()
    if len(p) == 3:
        if !in_scope(p[2]):
            raise NameError("Label " + p[2] + " not defined")
        p[0].code += ["break", p[2]] #TODO: change this
    else:
        p[0].code += ["break"] #TODO: change this to jump to end of the loop

def p_label(p):
    '''label : IDENT'''
    p[0] = p[1]

def p_error(p):
    print("------------ Syntax Error ----------")
    print(p)
    print("------------ Syntax Error ----------")

precedence = (
    ("right", "ASSIGN", "NOT"),
    ("left", "LOR"),
    ("left", "LAND"),
    ("nonassoc", "EQL", "NEQ", "LSS", "LEQ", "GTR", "GEQ"),
    ("left", "ADD", "SUB", "OR", "XOR"),
    ("left", "MUL", "QUO", "REM", "SHL", "SHR", "AND", "AND_NOT")
)


#Build the parser
parser = yacc.yacc(start = "source_file", debug = True)

f = open(infile)
data = f.read()
f.close()

output = parser.parse(data)

print(output)

for i, scope in enumerate(scopes):
    print(i, scope.table, scope.global_list, scope.parent)
