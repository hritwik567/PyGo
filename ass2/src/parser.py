import ply.yacc as yacc
import sys
import lexer
tokens = lexer.tokens

if len(sys.argv)!=2:
    print("usage: provide 1 input file")

infile = sys.argv[1]
def mytuple(arr):
    print(arr)
    return tuple(arr)

def p_empty(p):
    '''epsilon : '''
    p[0] = "epsilon"

def p_package_name(p):
    '''package_name : IDENT'''
    p[0] = mytuple(["package_name"] + p[1:])

def p_package_clause(p):
    '''package_clause : PACKAGE package_name'''
    p[0] = mytuple(["package_clause"] + p[1:])


def p_import_path(p):
    '''import_path : STRING_LIT'''
    p[0] = mytuple(["import_path"] + p[1:])

def p_import_spec(p):
    '''import_spec  : import_path
                    | package_name import_path
                    | PERIOD import_path'''
    p[0] = mytuple(["import_spec"] + p[1:])

def p_import_spec_rep(p):
    '''import_spec_rep  : import_spec_rep import_spec semicolon_opt
                        | epsilon'''
    p[0] = mytuple(["import_spec_rep"] + p[1:])

def p_import_decl(p):
    '''import_decl  : IMPORT import_spec
                    | IMPORT LPAREN import_spec_rep RPAREN'''
    p[0] = mytuple(["import_decl"] + p[1:])

def p_import_decl_rep(p):
    '''import_decl_rep  : import_decl_rep import_decl semicolon_opt
                        | epsilon'''
    p[0] = mytuple(["import_decl_rep"] + p[1:])

def p_top_level_decl_rep(p):
    '''top_level_decl_rep   : top_level_decl_rep top_level_decl semicolon_opt
                            | epsilon'''
    p[0] = mytuple(["top_level_decl_rep"] + p[1:])


def p_source_file(p):
    '''source_file  : package_clause semicolon_opt import_decl_rep top_level_decl_rep'''
    p[0] = mytuple(["source_file"] + p[1:])

######################################################## SACRED #############################################################################

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
    '''type : type_name
            | type_lit
            | LPAREN type RPAREN'''
    p[0] = mytuple(["type"] + p[1:])

def p_type_name(p):
    '''type_name    : qualified_ident
                    | type_token'''
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
    print("function_type")
    p[0] = mytuple(["function_type"] + p[1:])

def p_signature(p):
    '''signature    : parameters parameters_rep result'''
    p[0] = mytuple(["signature"] + p[1:])

def p_parameters_rep(p):
    '''parameters_rep   : parameters_rep parameters
                        | epsilon'''
    p[0] = mytuple(["parameters_rep"] + p[1:])

def p_result(p):
    '''result   : type
                | epsilon'''
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
    '''identifier_list_opt  : identifier_list_opt
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
    '''short_val_decl   : identifier_list DEFINE expression_list'''
    # '''short_val_decl   : identifier_list DEFINE expression_list'''
    # Arpit: mutiple identifiers can be defined
    p[0] = mytuple(["short_val_decl"] + p[1:])

def p_function_decl(p):
    '''function_decl    : FUNC function_name function
                        | FUNC function_name signature semicolon_opt'''
    print("function_decl")
    p[0] = mytuple(["function_decl"] + p[1:])

def p_function_name(p):
    '''function_name    : IDENT'''
    p[0] = mytuple(["function_name"] + p[1:])

def p_function(p):
    '''function : signature function_body'''
    p[0] = mytuple(["function"] + p[1:])

def p_function_body(p):
    '''function_body    : block'''
    p[0] = mytuple(["function_body"] + p[1:])

def p_method_decl(p):
    '''method_decl  : FUNC receiver method_name function
                    | FUNC receiver method_name signature'''
    print("method_decl")
    p[0] = mytuple(["method_decl"] + p[1:])

def p_receiver(p):
    '''receiver : parameters'''
    p[0] = mytuple(["receiver"] + p[1:])

def p_operand(p):
    '''operand  : literal
                | operand_name
                | method_expr
                | LPAREN expression RPAREN'''
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

def p_operand_name(p):
    '''operand_name : qualified_ident
                    | IDENT'''
    p[0] = mytuple(["operand_name"] + p[1:])
    print("--------------- operand name------------------")

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
    print("function_lit")
    p[0] = mytuple(["function_lit"] + p[1:])

def p_primary_expr(p):
    '''primary_expr : operand
                    | conversion
                    | primary_expr selector
                    | primary_expr index
                    | primary_expr slice
                    | primary_expr type_assertion
                    | primary_expr arguments'''
    p[0] = mytuple(["primary_expr"] + p[1:])

def p_selector(p):
    '''selector : IDENT'''
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

def p_receiver_type(p):
    '''receiver_type    : type_name
                        | LPAREN MUL type_name RPAREN
                        | LPAREN receiver_type RPAREN'''
    p[0] = mytuple(["receiver_type"] + p[1:])

def p_expression(p):
    '''expression   : unary_expr
                    | expression binary_op expression'''
    p[0] = mytuple(["expression"] + p[1:])
    print("--------------- expression ------------------")

def p_unary_expr(p):
    '''unary_expr   : primary_expr
                    | unary_op unary_expr'''
    p[0] = mytuple(["unary_expr"] + p[1:])
    print("--------------- unary expression------------------")

def p_binary_op(p):
    '''binary_op    : LAND
                    | LOR
                    | rel_op
                    | add_op
                    | mul_op'''
    p[0] = mytuple(["binary_op"] + p[1:])

def p_rel_op(p):
    '''rel_op   : EQL
                | NEQ
                | LSS
                | LEQ
                | GTR
                | GEQ'''
    p[0] = mytuple(["rel_op"] + p[1:])

def p_mul_op(p):
    '''mul_op   : MUL
                | QUO
                | REM
                | SHL
                | SHR
                | AND
                | AND_NOT'''
    p[0] = mytuple(["mul_op"] + p[1:])

def p_add_op(p):
    '''add_op   : ADD
                | SUB
                | OR
                | XOR'''
    p[0] = mytuple(["add_op"] + p[1:])

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
    print("--------------- expression list ------------------")

def p_expression_rep(p):
    '''expression_rep   : COMMA expression expression_rep
                        | epsilon'''
    p[0] = mytuple(["expression_rep"] + p[1:])
    print("--------------- expression rep ------------------")

def p_identifier_list(p):
    '''identifier_list  : identifier_list COMMA IDENT
                        | IDENT'''
    p[0] = mytuple(["identifier_list"] + p[1:])

def p_statement_list(p):
    '''statement_list   : statement_rep'''
    print("--------------------------------p_statement_list-----------------------------------")
    p[0] = mytuple(["statement_list"] + p[1:])

def p_statement_rep(p):
    '''statement_rep    : statement semicolon_opt statement_rep
                        | epsilon'''
    p[0] = mytuple(["statement_rep"] + p[1:])

def p_block(p):
    '''block    : LBRACE statement_list RBRACE'''
    print("--------------------------------p_block-----------------------------------")
    p[0] = mytuple(["block"] + p[1:])

def p_conversion(p):
    '''conversion   : type_token LPAREN expression comma_opt RPAREN'''
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
                    | block
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
    p[0] = mytuple(["labeled_stmt"] + p[1:])

def p_expression_stmt(p):
    '''expression_stmt  : expression'''
    p[0] = mytuple(["expression_stmt"] + p[1:])

def p_inc_dec_stmt(p):
    '''inc_dec_stmt : expression INC
                    | expression DEC'''
    p[0] = mytuple(["inc_dec_stmt"] + p[1:])

def p_assignment(p):
    '''assignment   : expression_list assign_op expression_list'''
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
    '''if_stmt  : IF simple_stmt_opt expression block
                | IF simple_stmt_opt expression block ELSE block
                | IF simple_stmt_opt expression block ELSE if_stmt'''
    p[0] = mytuple(["if_stmt"] + p[1:])

def p_switch_stmt(p):
    '''switch_stmt  : expr_switch_stmt'''
    p[0] = mytuple(["switch_stmt"] + p[1:])

def p_expr_switch_stmt(p):
    '''expr_switch_stmt : SWITCH simple_stmt_opt expression_opt LBRACE expr_case_clause_rep RBRACE'''
    p[0] = mytuple(["expr_switch_stmt"] + p[1:])

def p_simple_stmt_opt(p):
    '''simple_stmt_opt  : simple_stmt SEMICOLON
                        | epsilon'''
    # Hritvikt can semicolon be optional
    p[0] = mytuple(["simple_stmt_opt"] + p[1:])

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
    '''for_stmt : FOR block
                | FOR condition block
                | FOR for_clause block
                | FOR range_clause block'''
    p[0] = mytuple(["for_stmt"] + p[1:])

def p_for_clause(p):
    '''for_clause   : init_stmt semicolon_opt condition_opt semicolon_opt post_stmt'''
    p[0] = mytuple(["for_clause"] + p[1:])

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
    p[0] = mytuple(["fallthrough_stmt"] + p[1:])

def p_defer_stmt(p):
   '''defer_stmt  : DEFER expression'''
   p[0] = mytuple(["defer_stmt"] + p[1:])

def p_goto_stmt(p):
    '''goto_stmt  : GOTO label'''
    p[0] = mytuple(["goto_stmt"] + p[1:])

def p_continue_stmt(p):
    '''continue_stmt    : CONTINUE label
                        | CONTINUE'''
    p[0] = mytuple(["continue_stmt"] + p[1:])

def p_break_stmt(p):
    '''break_stmt   : BREAK label
                    | BREAK'''
    p[0] = mytuple(["break_stmt"] + p[1:])

def p_label(p):
    '''label : IDENT'''
    p[0] = mytuple(["label"] + p[1:])

def p_error(p):
    print("------------ Syntax Error ----------")
    print(p)
    print("------------ Syntax Error ----------")

precedence = (
    ('right', 'ASSIGN', 'NOT'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('nonassoc', 'EQL', 'NEQ', 'LSS', 'LEQ', 'GTR', 'GEQ'),
    ('left', 'ADD', 'SUB', 'OR', 'XOR'),
    ('left', 'MUL', 'QUO', 'REM', 'SHL', 'SHR', 'AND', 'AND_NOT')
)

#Build the parser
parser = yacc.yacc(start='source_file', debug=True)

f = open(infile)
data = f.read()
f.close()

print(parser.parse(data))
