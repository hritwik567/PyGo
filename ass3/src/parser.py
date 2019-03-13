#!/usr/bin/env python3
import ply.yacc as yacc
import sys
import argparse
import lexer
import os
import inspect
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
#-------------------TEMPORARY VARIABLE STUFF-----------------------------
temp_ctr = 0
label_ctr = 0
label_dict = dict()
sizeof = dict()
sizeof["uint8"] = 1; sizeof["uint16"] = 2; sizeof["uint32"] = 4; sizeof["uint"] = 4; sizeof["uint64"] = 8;
sizeof["int8"] = 1; sizeof["int16"] = 2; sizeof["int32"] = 4; sizeof["int"] = 4; sizeof["int64"] = 8;
sizeof["float32"] = 4; sizeof["float64"] = 8;
sizeof["byte"] = 1; sizeof["bool"] = 1;


def new_temp():
    global temp_ctr
    print(inspect.stack()[1].function)
    temp_ctr += 1
    return "temp" + str(temp_ctr)

def new_label():
    global label_ctr
    label_ctr += 1
    return "label" + str(label_ctr)

def add_to_import_table(package, ident):
    global import_dict
    if package in import_dict:
        if ident in import_dict[package]:
            raise NameError(ident + " already imported from " + package)
        else:
            import_dict[package] += [ident]
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
    if p[-1] == 'for':
        p[0] = Node()
        for_label = "_for_" + new_label()
        end_for_label = "_end_" + for_label
        scopes[current_scope].insert(for_label, "label")
        scopes[current_scope].update("__BeginFor", for_label, "value")
        scopes[current_scope].update("__MidFor", for_label, "value")
        scopes[current_scope].update("__EndFor", end_for_label, "value")
        p[0].code += ["label, " + for_label]

def p_end_scope(p):
    '''end_scope    :'''
    if p[-3] == 'for' or p[-4] == 'for':
        p[0] = Node()
        for_label = find_info("__BeginFor", current_scope)["value"]
        end_for_label = "_end_" + for_label
        p[0].code += ["goto " + for_label]
        p[0].code += ["label, " + end_for_label]
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
                    | UINTPTR
                    | STRING'''
    global sizeof
    p[0] = Node()
    p[0].type_list += [p[1]]
    p[0].extra["size"] = sizeof[p[1]]

def p_type(p):
    '''type : type_token
            | type_lit
            | TYPE IDENT'''
    # check_shivansh
    # Arpit LPAREN type RPAREN removed from RHS
    # we shoudl check wether this type is available
    if len(p) == 3:
        p[0] = Node()
        p[0].type_list += ["type " + p[2]]
        info = find_info("type " + p[2], 0)
        p[0].extra["methods"] = info["methods"]
        p[0].extra["fields"] = info["fields"]
        p[0].extra["fields_type"] = info["fields_type"]
        p[0].extra["fields_size"] = info["fields_size"]
        p[0].extra["size"] = info["size"]
    else:
        p[0] = p[1]

def p_operand_name(p):
    '''operand_name : IDENT'''
    p[0] = Node()
    if p[1] == "true" or p[1] == "false":
        p[0].place_list = [temp_v]
        p[0].code = [[temp_v, "=", p[1]]]
        p[0].type_list = ["bool"]
        p[0].extra["size"] = 1
    else:
        p[0].id_list = [p[1]]
        p[0].type_list = ["identifier"]

def p_type_name(p):
    '''type_name    : TYPE IDENT'''
    # check_shivansh
    #Hritvik remove qualified_ident from type_name
    p[0] = Node()
    p[0].type_list = ["type " + p[1]]

def p_type_lit(p):
    '''type_lit : array_type
                | struct_type
                | pointer_type
                | interface_type
                | slice_type'''
    #Hritvik removed function_type
    p[0] = p[1]

def p_array_type(p):
    '''array_type   : LBRACK array_length RBRACK element_type'''
    global scopes
    if type(p[2].code[-1][-1]) != int:
        raise TypeError("Array length should be integer")
    p[0] = Node()
    temp_v = p[4].extra["size"]
    p[0].type_list = [["array", p[4].type_list[0], temp_v]]
    p[0].extra["size"] = p[2].code[-1][-1]*temp_v
    p[0].code = p[4].code

def p_array_length(p):
    '''array_length : expression'''
    p[0] = p[1]

def p_element_type(p):
    '''element_type : type'''
    p[0] = p[1]

def p_slice_type(p):
    '''slice_type   : LBRACK RBRACK element_type'''
    p[0] = Node()
    temp_v = p[3].extra["size"]
    p[0].type_list = [["slice", p[3].type_list[0], temp_v]]
    p[0].code = p[3].code

def p_struct_type(p):
    '''struct_type  : STRUCT LBRACE field_decl_rep RBRACE'''
    # ADD "fields" and "methods" and "fields_type" and "field_size"
    if len(p[3].id_list) != len(set(p[3].id_list)):
        raise NameError("Multiple fields with same name in struct")
    p[0] = Node()
    p[0].extra["fields"] = p[3].id_list
    p[0].extra["fields_type"] = p[3].type_list
    p[0].extra["fields_size"] = p[3].extra["element_size"]
    p[0].type_list = ["struct"]
    p[0].extra["size"] = sum(p[3].extra["element_size"])
    p[0].code = p[3].code

def p_field_decl_rep(p):
    '''field_decl_rep   : field_decl_rep field_decl semicolon_opt
                        | epsilon'''
    p[0] = p[1]
    if len(p) == 4:
        p[0].id_list += p[2].id_list
        p[0].type_list += p[2].type_list
        p[0].extra["element_size"] += p[2].extra["element_size"]
        p[0].code += p[2].code
    else:
        p[0].extra["element_size"] = []

def p_field_decl(p):
    '''field_decl   : identifier_list type'''
    p[0] = Node()
    p[0].id_list = p[1].id_list
    p[0].type_list = [p[4].type_list[0]]*len(p[0].id_list)
    if "type" in p[4].type_list[0]:
        info = find_info(p[4].type_list[0], 0)
        p[0].extra["element_size"] = [info["size"]]*len(p[0].id_list)
    else:
        p[0].type_list = [p[0].extra["size"]]*len(p[0].id_list)
    p[0].code = p[2].code

def p_pointer_type(p):
    '''pointer_type : MUL base_type'''
    p[0] = Node()
    p[0].type_list = [["pointer", p[2].type_list[0], p[2].extra["size"]]]
    p[0].extra["size"] = 4

def p_base_type(p):
    '''base_type    : type'''
    p[0] = p[1]

# def p_function_type(p):
#     '''function_type    : FUNC signature'''
#     p[0] = Node()
#     p[0].type_list += ["func"] + p[1].type_list #TODO: Need to fix this

def p_signature(p):
    '''signature    : parameters result'''
    p[0] = Node()
    p[0].id_list = p[1].id_list
    p[0].type_list = p[1].type_list
    p[0].extra["paramter_size"] = p[1].extra["size"]
    if len(p[2].type_list) == 0:
        p[0].extra["return_type"] = ["void"]
        p[0].extra["return_id"] = [None]
        p[0].extra["return_size"] = [0]
    else:
        p[0].extra["return_type"] = p[2].type_list
        p[0].extra["return_id"] = p[2].id_list
        p[0].extra["return_size"] = p[2].extra["size"]

def p_result(p):
    '''result   : parameters
                | type_list
                | type
                | epsilon'''
    p[0] = p[1]
    if len(p[0].type_list) != len(p[0].id_list):
        p[0].id_list = [None]*(len(p[0].type_list))

def p_type_list(p):
    '''type_list    : LPAREN type type_rep comma_opt RPAREN'''
    p[0] = p[2]
    p[0].type_list += p[3].type_list
    p[0].extra["size"] = [p[0].extra["size"]] + p[3].extra["size"]
    p[0].id_list = [None]*(len(p[0].type_list))

def p_type_rep(p):
    '''type_rep : type_rep COMMA type
                | epsilon'''
    p[0] = p[1]
    if len(p) == 4:
        p[0].type_list += p[3].type_list
        p[0].extra["size"] += [p[3].extra["size"]]
    else:
        p[0].extra = []

def p_parameters(p):
    '''parameters   : LPAREN RPAREN
                    | LPAREN parameter_list comma_opt RPAREN'''
    if len(p) == 3:
        p[0] = Node()
        p[0].extra["size"] = []
    else:
        p[0] = p[2]

def p_parameter_list(p):
    '''parameter_list   : parameter_decl parameter_decl_rep '''
    p[0] = p[1]
    p[0].id_list += p[2].id_list
    p[0].type_list += p[2].type_list
    p[0].extra["size"] += p[2].extra["size"]

def p_parameter_decl_rep(p):
    '''parameter_decl_rep   : parameter_decl_rep COMMA parameter_decl
                            | epsilon'''
    p[0] = p[1]
    if len(p) == 4:
        p[0].id_list += p[3].id_list
        p[0].type_list += p[3].type_list
        p[0].extra["size"] += p[3].extra["size"]
    else:
        p[0].extra["size"] = []
def p_parameter_decl(p):
    '''parameter_decl   : identifier_list_opt type '''
    p[0] = Node()
    if len(p[1].id_list) == 0:
        p[0].type_list = [p[2].type_list[0]]
        p[0].id_list = [None]
        p[0].extra["size"] = [p[2].extra["size"]]
    else:
        p[0].id_list = p[1].id_list
        p[0].type_list = [p[2].type_list[0]]*(len(p[1].id_list))
        p[0].extra["size"] = [p[2].extra["size"]]*(len(p[1].id_list))

def p_identifier_list_opt(p):
    '''identifier_list_opt  : identifier_list
                            | epsilon'''
    p[0] = p[1]

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
    p[0] = p[1]

def p_interface_type_name(p):
    '''interface_type_name  : type_name'''
    p[0] = p[1]

def p_key_type(p):
    '''key_type : type'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration  : const_decl
                    | type_decl
                    | var_decl'''
    p[0] = p[1]

def p_top_level_decl(p):
    '''top_level_decl   : declaration
                        | function_decl
                        | method_decl'''
    p[0] = p[1]

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
    p[0] = p[1]

def p_type_decl(p):
    '''type_decl    : TYPE type_spec
                    | TYPE LPAREN type_spec_rep RPAREN'''
    p[0] = p[1]

def p_type_spec_rep(p):
    '''type_spec_rep    : type_spec_rep type_spec semicolon_opt
                        | epsilon'''
    p[0] = p[1]

def p_type_spec(p):
    '''type_spec    : type_def'''
    #TODO: Hritvik removed alias type add that it is pretty easy
    p[0] = p[1]

# def p_alias_decl(p):
#     '''alias_decl   : IDENT ASSIGN type'''
#     p[0] = mytuple(["alias_decl"] + p[1:])

def p_type_def(p):
    '''type_def : IDENT struct_type'''
    #TODO: Hritvik changed this to struct type
    p[0] = Node()
    global scopes, current_scope
    scopes[current_scope].insert("type " + p[1], "struct")
    scopes[current_scope].update("type " + p[1], [], "methods")
    scopes[current_scope].update("type " + p[1], p[0].extra["fields"], "fields")
    scopes[current_scope].update("type " + p[1], p[2].extra["fields_type"], "fields_type")
    scopes[current_scope].update("type " + p[1], p[2].extra["fields_size"], "fields_size")
    scopes[current_scope].update("type " + p[1], p[2].extra["size"], "size")

def p_var_decl(p):
    '''var_decl : VAR var_spec
                | VAR LPAREN var_spec_rep RPAREN'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[3]

def p_var_spec_rep(p):
    '''var_spec_rep : var_spec_rep var_spec semicolon_opt
                    | epsilon'''
    p[0] = p[1]
    if len(p) != 2:
        p[0].id_list += p[2].id_list
        p[0].type_list += p[2].type_list
        p[0].code += p[2].code

def p_var_spec(p):
    '''var_spec : identifier_list type expr_list_assign_opt
                | identifier_list ASSIGN expression_list'''
    global scopes, current_scope
    p[0] = p[1]
    p[0].code += p[3].code
    if p[2] == "=":
        if len(p[1].id_list) != len(p[3].place_list):
            raise ArithmeticError("Different Number of identifiers and Expression")
        p[0].place_list = p[3].place_list
        id_list = p[1].id_list
        expr_type_list = p[3].type_list
        for i in range(len(p[1].id_list)):
            if scopes[current_scope].look_up(id_list[i]):
                raise NameError("Variable " + id_list[i] + "already declared\n")
            scopes[current_scope].insert(id_list[i], expr_type_list[i])
            scopes[current_scope].update(id_list[i], p[3].extra["size"][i], "size")
            scopes[current_scope].update(id_list[i], p[3].place_list[i], "temp")
            scopes[current_scope].update(id_list[i], True, "is_var")
    else:
        if len(p[3].place_list) == 0:
            # not initialised with expressions
            id_list = p[1].id_list
            for i in range(len(id_list)):
                if scopes[current_scope].look_up(id_list[i]):
                    raise NameError("Variable " + id_list[i] + "already declared\n")
                temp_v = new_temp()
                scopes[current_scope].insert(id_list[i], p[2].type_list[0])
                scopes[current_scope].update(id_list[i], p[2].extra["size"], "size")
                scopes[current_scope].update(id_list[i], temp_v, "temp")
                scopes[current_scope].update(id_list[i], True, "is_var")
                p[0].code += p[2].code
        else:
            if len(p[1].id_list) != len(p[3].place_list):
                raise ArithmeticError("Different Number of identifiers and Expressions\n")
            p[0].place_list = p[3].place_list
            id_list = p[1].id_list
            expr_type_list = p[3].type_list
            for i in range(len(id_list)):
                if scopes[current_scope].look_up(id_list[i]):
                    raise NameError("Variable " + id_list[i] + "already declared\n")
                typecast = ("float" in p[2].type_list[0] and "int" in expr_type_list[i])
                typecast = typecast or (p[2].type_list[0].startswith("int") and "int" in expr_type_list[i])
                typecast = typecast or (p[2].type_list[0].startswith("uint") and "uint" in expr_type_list[i])
                if p[2].type_list[0] == expr_type_list[i] or typecast:
                    scopes[current_scope].insert(p[1].id_list[i], p[2].type_list[0])
                    scopes[current_scope].update(id_list[i], p[2].extra["size"], "size")
                    scopes[current_scope].update(id_list[i], p[3].place_list[i], "temp")
                    scopes[current_scope].update(id_list[i], True, "is_var")
                    p[0].code += p[2].code
                else:
                    raise TypeError("Type mismatch for identifier:" + id_list[i])

def p_expr_list_assign_opt(p):
    '''expr_list_assign_opt : ASSIGN expression_list
                            | epsilon'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_short_val_decl(p):
    '''short_val_decl   : IDENT DEFINE expression'''
    # '''short_val_decl   : identifier_list DEFINE expression_list'''
    # Arpit: mutiple identifiers can be defined
    global scopes, current_scope
    p[0] = p[3]
    p[0].id_list += [p[1]]
    if scopes[current_scope].look_up(p[1]):
        raise NameError("Variable " + p[1] + "already declared\n")
    scopes[current_scope].insert(p[1], p[3].type_list[0])
    scopes[current_scope].update(p[1], p[3].extra["size"], "size")
    scopes[current_scope].update(p[1], p[3].place_list[0], "temp")
    scopes[current_scope].update(p[1], True, "is_var")

def p_function_decl(p):
    '''function_decl    : FUNC function_name add_scope function end_scope
                        | FUNC function_name add_scope signature end_scope semicolon_opt'''
    #TODO: verify whether we need to add scope at the time of signature declaration
    #In this function current scope is actually global
    global scopes, current_scope
    if len(p) == 6:
        p[0] = p[4]
    else:
        if in_scope("signature_" + p[2]):
            raise NameError("Signature " + p[2] + " already defined")
        else:
            scopes[0].insert("signature_" + p[2], "signature")
            p[0] = p[4]
            scopes[0].update("signature_" + p[2], p[0].type_list , "parameter_type")
            scopes[0].update("signature_" + p[2], p[0].id_list , "parameter_id")
            scopes[0].update("signature_" + p[2], p[0].extra["paramter_size"] , "parameter_size")
            scopes[0].update("signature_" + p[2], p[0].extra["return_type"] , "return_type")
            scopes[0].update("signature_" + p[2], p[0].extra["return_id"] , "return_id")
            scopes[0].update("signature_" + p[2], p[0].extra["return_size"] , "return_size")

def p_function_name(p):
    '''function_name    : IDENT'''
    p[0] = p[1]

def p_function(p):
    '''function : signature function_body'''
    if in_scope(p[-2]):
        raise NameError("Function " + p[-2] + " already defined")
    if in_scope("signature_" + p[-2]):
        info = scopes[0].find_info("signature_" + p[2])
        if info["parameter_type"] != p[1].type_list:
            raise TypeError("Prototype and Function paramter type don't match ", info["parameter_type"], p[1].type_list)
        elif info["return_type"] != p[1].extra["return_type"]:
            raise TypeError("Prototype and Function return type don't match ", info["parameter_type"], p[1].extra["return_type"])

    temp_l = new_label()
    scopes[0].insert(p[-2], "function")
    scopes[0].update(p[-2], p[1].type_list , "parameter_type")
    scopes[0].update(p[-2], p[1].id_list , "parameter_id")
    scopes[0].update(p[-2], p[1].extra["paramter_size"] , "parameter_size")
    scopes[0].update(p[-2], p[1].extra["return_type"] , "return_type")
    scopes[0].update(p[-2], p[1].extra["return_id"] , "return_id")
    scopes[0].update(p[-2], p[1].extra["return_size"] , "return_size")
    scopes[0].update(p[-2], temp_l , "label")

    id_list = p[1].id_list
    if len(id_list) != len(set(id_list)):
        raise NameError("Variable already declared\n")
    for i in range(len(id_list)):
        temp_v = new_temp()
        scopes[current_scope].insert(id_list[i], p[1].type_list[i])
        scopes[current_scope].update(id_list[i], p[1].extra["paramter_size"][i], "size")
        scopes[current_scope].update(id_list[i], temp_v, "temp")
        scopes[current_scope].update(id_list[i], True, "is_var")

    p[0] = Node()
    p[0].code = [["label", temp_l], ["func", p[-2]]]
    p[0].code += p[1].code + p[2].code + [["end", p[-2]]]

    print("-----------code-----------")
    for i in p[0].code:
        print(i)
    print("-----------code-----------")

def p_function_body(p):
    '''function_body    : block'''
    p[0] = p[1]

def p_method_decl(p):
    '''method_decl  : FUNC receiver method_name add_scope function end_scope
                    | FUNC receiver method_name add_scope signature end_scope'''
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
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_literal(p):
    '''literal  : basic_lit'''
    #TODO: Removed composite_lit for now
    #TODO: Hritvik removed function_lit dekh lo agar ho sakta hai toh
    p[0] = p[1]

def p_basic_lit(p):
    '''basic_lit    : int_lit
                    | FLOAT_LIT
                    | STRING_LIT '''
    #Add imaginary and rune lit
    if type(p[1]) == Node:
        p[0] = p[1]
    elif type(p[1]) == float:
        temp_v = new_temp()
        p[0] = Node()
        p[0].place_list = [temp_v]
        p[0].code = [[temp_v, "=", p[1]]]
        p[0].type_list = ["float32"]
        p[0].extra["size"] = 4
    else:
        temp_v = new_temp()
        p[0] = Node()
        p[0].place_list = [temp_v]
        p[0].code = [[temp_v, "=", p[1]]]
        p[0].type_list = ["string"]

def p_int_lit(p):
    '''int_lit  : DECIMAL_LIT
                | OCTAL_LIT
                | HEX_LIT'''
    temp_v = new_temp()
    p[0] = Node()
    p[0].place_list = [temp_v]
    p[0].code = [[temp_v, "=", p[1]]]
    p[0].type_list = ["int"]
    p[0].extra["size"] = 4


def p_qualified_ident(p):
    '''qualified_ident  : package_name PERIOD IDENT'''
    p[0] = mytuple(["qualified_ident"] + p[1:])

def p_composite_lit(p):
    '''composite_lit    : literal_type literal_value'''
    p[0] = Node()
    #if "type" in p[1].type_list[0]:
        #TODO: check the type of all the elements of the struct
    #elif "slice" in p[1].type_list[0]:
        #TODO: check the type of all the elements they should be equal to p[1].extra["element_type"]
        #and set the length and capacity to number of elements
    #else:
        #TODO: check the type of all the elements they should be equal to p[1].extra["element_type"]
        #and the length should be less than  p[1].extra["element_length"]
        #and set the length to the number of elements and capacity to p[1].extra["element_length"]

def p_literal_type(p):
    '''literal_type : array_type
                    | slice_type
                    | type_name'''
    p[0] = p[1]

def p_literal_value(p):
    '''literal_value    : LBRACE RBRACE
                        | LBRACE element_list comma_opt RBRACE'''
    if len(p) == 3:
        p[0] = Node()
    else:
        p[0] = p[2]

def p_element_list(p):
    '''element_list : element_list COMMA element
                    | element'''
    p[0] = p[1]
    if len(p) == 4:
        p[0].id_list += [","] + p[3].id_list
        p[0].type_list += [","] + p[3].type_list
def p_element(p):
    '''element  : expression
                | literal_value'''
    p[0] = p[1]

# def p_function_lit(p):
#     '''function_lit : FUNC function'''
#     p[0] = mytuple(["function_lit"] + p[1:])


# conversion deleted form the RHS of the primary expression
def p_primary_expr(p):
    '''primary_expr : operand
                    | conversion
                    | primary_expr PERIOD IDENT
                    | primary_expr LBRACK expression RBRACK
                    | primary_expr slice
                    | primary_expr LPAREN arguments RPAREN'''
    # check_shivansh
    # | operand_selector
    # but make sure of test cases : a.b.c(d,e)      x.a = b     foo(a,b)    etc.
    # operand selector in RHS becomes redundant; never gets used
    # slice may need to be removed from RHS
    # typeassertion removed from RHS of above production
    if "conversion" in p[1].extra:
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = p[1]
    elif p[2] == ".":
        #TODO: WE ARE NOT IMPLEMENTING IMPORTS HENCE ASSUMING PRIMARY EXPRESSION IN THIS CASE TO BE A VARIBLE
        p[0] = p[1]
        if "identifier" == p[0].type_list[0]:
            info = find_info(p[0].id_list[0])
            if info["is_var"]:
                temp_v = new_temp()
                p[0].code += [[temp_v, "=", "(addr)", info["temp"]]]
                info1 = find_info(info["type"], 0)
            else:
                raise NameError("Variable " + p[0].id_list[0] + " not defined")
        else:
            info1 = find_info(p[0].type_list[0][1], 0)
            temp_v = p[0].place_list[0]

        if p[3] in info1["fields"]:
            p[0].type_list[0] = ["pointer", info1["fields_type"][info1["fields"].index(p[3])], info1["fields_size"][info1["fields"].index(p[3])]]
            temp_v1 = new_temp()
            p[0].code += [[temp_v1, "=", temp_v, "int_+", sum(info1["fields_size"][:info1["fields"].index(p[3])])]]
            p[0].place_list[0] = temp_v1
            p[0].extra["size"] = 4
        # elif p[3] in info1["methods"]:
        else:
            raise NameError("No field or method " + p[3] + " defined in " + info1["type"])

    elif p[2] == "[":
        p[0] = p[1]
        p[0].code += p[3].code
        if "identifier" == p[0].type_list[0]:
            info = find_info(p[0].id_list[0])
            if info["is_var"]:
                temp_v = new_temp()
                p[0].code += [[temp_v, "=", "(addr)", info["temp"]]]
                info1 = find_info(info["type"], 0)
            else:
                raise NameError("Variable " + p[0].id_list[0] + " not defined")
        elif "array" not in p[0].type_list[0]:
            raise TypeError("Type " + p[0].type_list[0] + " not indexable")
        else:
            temp_v = p[0].place_list[0]
        p[0].type_list[0] = ["pointer", p[0].type_list[0][1], p[0].type_list[0][2]]
        temp_v1 = new_temp()
        temp_v2 = new_temp()
        p[0].code += [[temp_v1, p[0].type_list[0][2], "int_*", p[3].place_list[0]], [temp_v2, "=", temp_v, "int_+", temp_v1]]
        p[0].place_list[0] = temp_v1
        p[0].extra["size"] = 4
    #TODO: Hritvik not implementing slice for now
    # elif len(p) == 3:
    #     if p[1].id_list[0] == "identifier":
    elif p[2] == "(":
        if p[1].id_list[0] == "identifier":
            info = find_info(p[0].id_list[0], 0)

def p_slice(p):
    '''slice    : LBRACK expression_opt COLON expression_opt RBRACK
                | LBRACK expression_opt COLON expression COLON expression RBRACK'''
    p[0] = mytuple(["slice"] + p[1:])

def p_arguments(p):
    '''arguments    : epsilon
                    | expression_list comma_opt'''
    # check_shivansh
    # lst RHS may have to be removed
    p[0] = p[1]

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
    if len(p) == 2:
        p[0] = p[1]
    else:
        temp_v = new_temp()
        p[0] = Node()
        p[0].extra["size"] = max(p[1].extra["size"], p[3].extra["size"])
        print("expression", p[1].code)
        print("expression", p[3].code)
        if len(p[1].code) > 0 and len(p[3].code) > 0:
            if type(p[1].code[-1][-1]) == int and type(p[3].code[-1][-1]) == int:
                p[0].code = p[1].code[:-1]
                p[0].code += p[3].code[:-1]
                p[0].code += [[temp_v, "=", eval(str(p[1].code[-1][-1]) + p[2] + str(p[3].code[-1][-1]))]]
                p[0].place_list = [temp_v]
                if p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==":
                    p[0].type_list = ["bool"]
                else:
                    p[0].type_list = ["int"]
            elif type(p[1].code[-1][-1]) == float or type(p[3].code[-1][-1]) == float:
                p[0].code = p[1].code[:-1]
                p[0].code += p[3].code[:-1]
                p[0].place_list = [temp_v]
                if p[2] == "+" or p[2] == "-" or p[2] == "/" or p[2] == "*":
                    p[0].code += [[temp_v, "=", eval(str(p[1].code[-1][-1]) + p[2] + str(p[3].code[-1][-1]))]]
                    p[0].type_list = ["float32"]
                elif p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==":
                    p[0].place_list = [temp_v]
                    p[0].code += [[temp_v, "=", eval(str(p[1].code[-1][-1]) + p[2] + str(p[3].code[-1][-1]))]]
                    p[0].type_list = ["bool"]
                else:
                    raise TypeError("Cannot do operation " + p[2] + " on float literals")
        else:
            p[0].code = p[1].code
            p[0].code += p[3].code
            if p[1].type_list[0] == p[3].type_list[0]:
                if p[1].type_list[0] == "string":
                    if p[2] == "+":
                        p[0].place_list = [temp_v]
                        p[0].code += [[temp_v, "=", "concat", p[1].place_list[0], p[3].place_list[0]]]
                        p[0].type_list = ["string"]
                    else:
                        raise TypeError("Cannot do operation " + p[2] + " on string literal")
                elif "int" in p[1].type_list[0]:
                    if p[2] == "<<" or p[2] == ">>":
                        if "u" not in p[3].type_list[0]:
                            _temp_v = new_temp()
                            p[0].code += [[_temp_v, "=", "(uint)", p[3].place_list[0]]]
                    p[0].place_list = [temp_v]
                    p[0].code += [[temp_v, "=", p[1].place_list[0], "int_" + p[2], p[3].place_list[0]]]
                    if p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==":
                        p[0].type_list = ["bool"]
                    else:
                        p[0].type_list = [p[1].type_list[0]]
                elif "float" in p[1].type_list[0]:
                    if p[2] == "+" or p[2] == "-" or p[2] == "/" or p[2] == "*":
                        p[0].place_list = [temp_v]
                        p[0].code += [[temp_v, "=", p[1].place_list[0], "float_" + p[2], p[3].place_list[0]]]
                        p[0].type_list = [p[1].type_list[0]]
                    elif p[2] == "<" or p[2] == ">" or p[2] == "<=" or p[2] == ">=" or p[2] == "==":
                        p[0].place_list = [temp_v]
                        p[0].code += [[temp_v, "=", p[1].place_list[0], "float_" + p[2], p[3].place_list[0]]]
                        p[0].type_list = ["bool"]
                    else:
                        raise TypeError("Cannot do operation " + p[2] + " on float literals")
            else:
                raise TypeError("Cannot do operation " + p[2] + " on " + p[1].type_list[0] + " and " + p[3].type_list[0])

def p_unary_expr(p):
    '''unary_expr   : primary_expr
                    | unary_op unary_expr'''
    if len(p) == 2:
        p[0] = p[1]
        if "identifier" == p[0].type_list[0]:
            info = find_info(p[0].id_list[0])
            if info["is_var"]:
                p[0].type_list = [info["type"]]
                p[0].place_list = [info["temp"]]
                p[0].extra["size"] = info["size"]
            else:
                raise NameError("Variable " + p[0].id_list[0] + " not defined")
        elif "pointer" in p[0].type_list[0]:
            temp_v = new_temp()
            p[0].code += [[temp_v, "=", "(load)", p[0].place_list[0]]]
            p[0].type_list = p[0].type_list[0][1]
            p[0].size = p[0].type_list[0][2]
            p[0].place_list = [temp_v]
    else:
        if p[1] == "!":
            if "int" in p[2].type_list[0] or p[2].type_list[0] == "bool" or p[2].type_list[0] == "byte" :
                p[0] = p[2]
                temp_v = new_temp()
                p[0].code += [[temp_v, "=", "!", p[2].place_list[0]]]
                p[0].place_list = [temp_v]
            else:
                raise TypeError("Type Mismatch with unary operator" + p[1])

        if p[1] == "+":
            if "int" in p[2].type_list[0] or "float" in p[2].type_list[0] :
                p[0] = p[2]
            else:
                raise TypeError("Type Mismatch with unary operator" + p[1])

        if p[1] == "-":
            if "int" in p[2].type_list[0] or "float" in p[2].type_list[0] :
                p[0] = p[2]
                if "int" in p[2].type_list[0]:
                    type_v = "int"
                else:
                    type_v = "float"
                temp_v1 = new_temp()
                temp_v2 = new_temp()
                p[0].code += [[temp_v1, "=", "0"]]
                p[0].code += [[temp_v2, "=", temp_v1, type_v + "_" + p[1], p[2].place_list[0]]]
                p[0].place_list = [temp_v2]
            else:
                raise TypeError("Type Mismatch with unary operator" + p[1])

        if p[1] == "*":
            if p[2].type_list[0][0] == "pointer":
                p[0] = p[2]
                temp_v = new_temp()
                p[0].code += [[temp_v, "=", "(load)", p[2].place_list[0]]]
                p[0].type_list = p[2].type_list[0][1]
                p[0].size = p[2].type_list[0][2]
                p[0].place_list = [temp_v]
            else:
                raise TypeError("Type Mismatch with unary operator" + p[1])

        if p[1] == "&":
            p[0] = p[2]
            temp_v = new_temp()
            p[0].code += [[temp_v, "=", "(addr)", p[2].place_list[0]]]
            p[0].type_list = [["pointer", p[2].type_list[0], p[2].extra["size"]]]
            p[0].place_list = [temp_v]

def p_unary_op(p):
    '''unary_op : ADD
                | SUB
                | MUL
                | AND
                | NOT'''
    #TODO: can add more here
    p[0] = p[1]

def p_expression_opt(p):
    '''expression_opt   : expression
                        | epsilon'''
    p[0] = p[1]

def p_expression_list(p):
    '''expression_list  : expression expression_rep'''
    p[0] = p[2]
    p[0].place_list += p[1].place_list
    p[0].type_list += p[1].type_list
    p[0].code += p[1].code
    p[0].extra["size"] += [p[1].extra["size"]]

def p_expression_rep(p):
    '''expression_rep   : COMMA expression expression_rep
                        | epsilon'''
    if len(p) == 2:
        p[0] = p[1]
        p[0].extra["size"] = []
    else:
        p[0] = p[3]
        p[0].place_list += p[2].place_list
        p[0].type_list += p[2].type_list
        p[0].code += p[2].code
        p[0].extra["size"] += [p[2].extra["size"]]

def p_identifier_list(p):
    '''identifier_list  : identifier_list COMMA IDENT
                        | IDENT'''
    if len(p) == 2:
        p[0] = Node()
        p[0].id_list = [p[1]]
    else:
        p[0] = p[1]
        p[0].id_list += [p[3]]

def p_statement_list(p):
    '''statement_list   : statement_rep'''
    p[0] = p[1]

def p_statement_rep(p):
    '''statement_rep    : statement semicolon_opt statement_rep
                        | epsilon'''
    if len(p) == 4:
        p[0] = Node()
        p[0].code = p[1].code + p[3].code
    else:
        p[0] = p[1]
def p_block(p):
    '''block    : LBRACE statement_list RBRACE'''
    # p[0] = mytuple(["block"] + p[1:])
    # TODO: Add block code and pass on above with id, type and temp_var list
    # Note that new label must be made by the production calling the block
    # If the block wants to use the label of the current scope then it should be able to fetch it from symbol table (extra dict())
    p[0] = p[2]

def p_conversion(p):
    '''conversion   : TYPECAST type_token LPAREN expression RPAREN'''
    # check prakhar TYPECAST is added
    # check prakhar comma is removed
    p[0] = p[4]
    p[0].extra["conversion"] = p[2].type_list[0]

    if "int" in p[2].type_list[0] and "int" in p[4].type_list[0]:
        temp_v = new_temp()
        type = "(" + p[4].type_list[0] + ")"
        p[0].code += [[temp_v, "=", type, p[4].place_list[0]]]
        p[0].place_list = [temp_v]
        p[0].type_list = [p[4].type_list[0]]

    if ("int" in p[2].type_list[0] or "float" in p[2].type_list[0]) and "float" in p[4].type_list[0]:
        temp_v = new_temp()
        type = "(" + p[4].type_list[0] + ")"
        p[0].code += [[temp_v, "=", type, p[4].place_list[0]]]
        p[0].place_list = [temp_v]
        p[0].type_list = [p[4].type_list[0]]

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
    p[0] = p[1]

def p_simple_stmt(p):
    '''simple_stmt  : epsilon
                    | expression_stmt
                    | inc_dec_stmt
                    | assignment
                    | short_val_decl'''
    p[0] = p[1]

def p_labeled_stmt(p):
    '''labeled_stmt : label COLON statement'''
    if in_scope(p[1]):
        raise NameError("Label " + p[1] + " already defined")
    else:
        global scopes, current_scope
        scopes[current_scope].insert(p[1], "label")
        scopes[current_scope].update(p[1], new_label(), "value")

def p_expression_stmt(p):
    '''expression_stmt  : expression'''
    p[0] = p[1]

def p_inc_dec_stmt(p):
    '''inc_dec_stmt : expression INC
                    | expression DEC'''
    p[0] = p[1]
    temp_v = new_temp()

    if "int" in p[0].type_list[0]:
        type_v = "int"
    elif "float" in p[0].type_list[0]:
        type_v = "float"
    else:
        type_v = ""

    if type_v != "":
        p[0].code += [[temp_v, "=", p[0].place_list[0], type_v + "_" + p[2][1], "1"]]
        p[0].place_list[0] = temp_v
    else:
        raise TypeError("Can't do " + p[2] + " operation on type " + p[0].type_list[0])

def p_assignment(p):
    '''assignment   : expression_list ASSIGN expression_list'''
    #Hritvik canges assign_op to ASSIGN
    global scopes, current_scope
    p[0] = p[1]
    p[0].code += p[3].code
    if len(p[1].place_list) != len(p[3].place_list):
        raise ArithmeticError("Different Number of expressions and and their values\n")
    # p[0].place_list = p[3].place_list
    expr_type_list_key = p[1].type_list
    expr_type_list_val = p[3].type_list
    expr_place_list_key = p[1].place_list
    expr_place_list_val = p[3].place_list
    for i in range(len(expr_type_list_key)):
        typecast = ("float" in expr_type_list_key[i] and "int" in expr_type_list_val[i])
        typecast = typecast or (expr_type_list_key[i].startswith("int") and "int" in expr_type_list_val[i])
        typecast = typecast or (expr_type_list_key[i].startswith("uint") and "uint" in expr_type_list_val[i])
        if expr_type_list_key[i] == expr_type_list_val[i] or typecast:
            p[0].code += [[expr_place_list_key[i], "=", expr_place_list_val[i]]]
        else:
            raise TypeError("Type mismatch for identifier:" + id_list[i])

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
                | FOR add_scope for_clause block end_scope'''
                #| FOR add_scope range_clause block end_scope'''
    # Leaving out range clause for now
    #p[0] = mytuple(["for_stmt"] + p[1:])
    p[0] = Node()
    if len(p) == 5:
        p[0].code += p[2].code
        p[0].code += p[3].code
        p[0].code += p[4].code
    else:
        p[0].code += p[3].code
        p[0].code += p[4].code
        p[0].code += p[5].code
    
def p_for_clause(p):
    '''for_clause   : init_stmt SEMICOLON condition_opt SEMICOLON post_stmt'''
    # Ayush changed this because earlier case allowed a wrond for format to be correctly parsed
    # Suppose init_stmt -> simple_stmt and post_init_stmt -> epsilon (wrong)
    p[0] = mytuple(["for_clause"] + p[1:])

# def p_post_init_stmt(p):
#     '''post_init_stmt    : SEMICOLON condition_opt SEMICOLON post_stmt
#                     | epsilon'''
#     p[0] = mytuple(["post_init_stmt"] + p[1:])


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
    #p[0] = mytuple(["condition"] + p[1:])
    # TODO: Add condition statement for if
    # Test "for" one
    if p[1].type_list[0] != "bool":
        raise TypeError("The condition " + p[1] + " is not a boolean value")
    p[0] = Node()
    if p[-2] == 'for':
        p[0].code += p[-1].code
        p[0].code += p[1].code
        end_for_label = find_info("__EndFor")["value"]
        p[0].code += ["if not " + p[0].place_list[0] + "then goto " + end_for_label]

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
    if not in_scope(p[2]):
        raise NameError("Label " + p[2] + " not defined")
    p[0] = Node()
    p[0].code += ["goto", p[2]] #TODO: change this

def p_continue_stmt(p):
    '''continue_stmt    : CONTINUE label
                        | CONTINUE'''
    p[0] = Node()
    # TODO: Add continue for switch and select if implementing
    # Test this
    if len(p) == 3:
        if not in_scope(p[2]):
            raise NameError("Label " + p[2] + " not defined")
        mid_for_label = "_mid_" + p[2]
        p[0].code += ["goto " + mid_for_label]
    else:
        if not in_scope("__BeginFor"):
            raise SyntaxError("Continue statement must be inside for loop")
        mid_for_label = find_info("__MidFor")["value"]
        p[0].code += ["goto " + mid_for_label]

def p_break_stmt(p):
    '''break_stmt   : BREAK label
                    | BREAK'''
    p[0] = Node()
    # TODO: Add break for switch and select if implementing
    # Test this
    if len(p) == 3:
        if not in_scope(p[2]):
            raise NameError("Label " + p[2] + " not defined")
        end_for_label = "_end_" + p[2]
        p[0].code += ["goto " + end_for_label]
    else:
        if not in_scope("__BeginFor"):
            raise SyntaxError("Break statement must be inside for loop")
        end_for_label = find_info("__EndFor")["value"]
        p[0].code += ["goto " + end_for_label]

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
