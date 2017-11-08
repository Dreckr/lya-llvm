import ply.yacc as yacc
import ply.lex as lex
from .lexer import tokens
from .lexer import lexer


def p_program(p):
    r'''program : program statement
                    | statement'''
    if len(p) == 2:
        p[0] = ('PROGRAM', [p[1]])
    elif len(p) == 3:
        p[1][1].append(p[2])
        p[0] = ('PROGRAM', p[1][1])


def p_statement(p):
    r'''statement : declaration_statement
                    | synonym_statement
                    | newmode_statement
                    | procedure_statement
                    | action_statement'''
    p[0] = ('STATEMENT', [p[1]])


# Declaration
def p_declaration_statement(p):
    r'declaration_statement : DCL declaration_list SEMICOLON'
    p[0] = ('DECLARATION_STATEMENT', [p[2]])


def p_declaration_list(p):
    r'''declaration_list : declaration_list COMMA declaration
                         | declaration'''
    if len(p) == 2:
        p[0] = ('DECLARATION_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('DECLARATION_LIST', p[1][1])


def p_declaration(p):
    r'''declaration : identifier_list mode
                    | identifier_list mode initialization'''
    if len(p) == 3:
        p[0] = ('DECLARATION', [p[1], p[2]])
    elif len(p) == 4:
        p[0] = ('DECLARATION', [p[1], p[2], p[3]])


def p_initialization(p):
    r'initialization : EQUALS expression'
    p[0] = ('INITIALIZATION', [p[2]])


def p_identifier_list(p):
    r'''identifier_list : identifier_list COMMA identifier
                        | identifier'''
    if len(p) == 2:
        p[0] = ('IDENTIFIER_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('IDENTIFIER_LIST', p[1][1])


def p_identifier(p):
    r'identifier : IDENTIFIER'
    p[0] = ('IDENTIFIER', [], p[1])


# Synonym
def p_synonym_statement(p):
    r'synonym_statement : SYN synonym_list SEMICOLON'
    p[0] = ('SYNONYM_STATEMENT', [p[2]])


def p_synonym_list(p):
    r'''synonym_list : synonym_list COMMA synonym_definition
                        | synonym_definition'''
    if len(p) == 2:
        p[0] = ('SYNONYM_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('SYNONYM_LIST', p[1][1])


def p_synonym_definition(p):
    r'''synonym_definition : identifier_list EQUALS constant_expression
                            | identifier_list mode EQUALS constant_expression'''
    if len(p) == 4:
        p[0] = ('SYNONYM_DEFINITION', [p[1], p[3]])
    elif len(p) == 5:
        p[0] = ('SYNONYM_DEFINITION', [p[1], p[2], p[4]])


def p_constant_expression(p):
    r'constant_expression : expression'
    p[0] = p[1]


# New mode
def p_newmode_statement(p):
    r'newmode_statement : TYPE newmode_list SEMICOLON'
    p[0] = ('NEWMODE_STATEMENT', [p[2]])


def p_newmode_list(p):
    r'''newmode_list : newmode_list COMMA mode_definition
                        | mode_definition'''
    if len(p) == 2:
        p[0] = ('NEWMODE_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('NEWMODE_LIST', p[1][1])


def p_mode_definition(p):
    r'mode_definition : identifier_list EQUALS mode'
    p[0] = ('MODE_DEFINITION', [p[1], p[3]])


# Procedure
def p_procedure_statement(p):
    r'procedure_statement : label COLON procedure_definition SEMICOLON'
    p[0] = ('PROCEDURE_STATEMENT', [p[1], p[3]])


def p_procedure_definition(p):
    r'''procedure_definition : PROC LPARENS formal_parameter_list RPARENS SEMICOLON action_statement_list END
                            | PROC LPARENS formal_parameter_list RPARENS result_spec SEMICOLON action_statement_list END'''
    if len(p) == 9:
        p[0] = ('PROCEDURE_DEFINITION', [p[3], p[5], p[7]])
    elif len(p) == 8:
        p[0] = ('PROCEDURE_DEFINITION', [p[3], p[6]])


def p_formal_parameter_list(p):
    r'''formal_parameter_list : formal_parameter_list COMMA formal_parameter
                                | formal_parameter
                                | empty'''
    if len(p) == 2:
        if p[1] is None:
            p[0] = ('FORMAL_PARAMETER_LIST', [])
        else:
            p[0] = ('FORMAL_PARAMETER_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('FORMAL_PARAMETER_LIST', p[1][1])


def p_formal_parameter(p):
    r'formal_parameter : identifier_list parameter_spec'
    p[0] = ('FORMAL_PARAMETER', [p[1], p[2]])


def p_parameter_spec(p):
    r'''parameter_spec : mode LOC
                            | mode'''
    if len(p) == 2:
        p[0] = ('PARAMETER_SPEC', [p[1]])
    elif len(p) == 3:
        p[0] = ('PARAMETER_SPEC_LOC', [p[1]])


def p_result_spec(p):
    r'''result_spec : RETURNS LPARENS mode RPARENS
                        | RETURNS LPARENS mode LOC RPARENS'''
    if len(p) == 5:
        p[0] = ('RESULT_SPEC', [p[3]])
    elif len(p) == 6:
        p[0] = ('RESULT_SPEC_LOC', [p[3]])


# Action
def p_action_statement_list(p):
    r'''action_statement_list : action_statement_list action_statement
                                | action_statement'''
    if len(p) == 2:
        p[0] = ('ACTION_STATEMENT_LIST', [p[1]])
    elif len(p) == 3:
        p[1][1].append(p[2])
        p[0] = ('ACTION_STATEMENT_LIST', p[1][1])


def p_action_statement(p):
    r'''action_statement : label COLON action SEMICOLON
                            | action SEMICOLON'''
    if len(p) == 3:
        p[0] = ('ACTION_STATEMENT', [p[1]])
    elif len(p) == 5:
        p[0] = ('ACTION_STATEMENT', [p[1], p[3]])


def p_label(p):
    r'label : IDENTIFIER'
    p[0] = ('LABEL', [], p[1])


def p_action(p):
    r'''action : bracketed_action
                | assert_action
                | assignment_action
                | call_action
                | exit_action
                | return_action
                | result_action'''
    p[0] = ('ACTION', [p[1]])


def p_bracketed_action(p):
    r'''bracketed_action : if_action
                            | do_action'''
    p[0] = ('BRACKETED_ACTION', [p[1]])


def p_assert_action(p):
    r'assert_action : ASSERT boolean_expression'
    p[0] = ('ASSERT_ACTION', [p[2]])


def p_assignment_action(p):
    r'assignment_action : location assigning_operator expression'
    p[0] = (p[2][0], [p[1], p[3]])


def p_assigning_operator(p):
    r'''assigning_operator : EQUALS
                                | closed_dyadic_operator EQUALS'''
    if len(p) == 2:
        p[0] = ('ASSIGNING_OPERATOR', [])
    elif len(p) == 3:
        p[0] = p[1]


def p_closed_dyadic_operator(p):
    r'''closed_dyadic_operator : arithmetic_additive_operator
                                | arithmetic_multiplicative_operator
                                | string_concatenation_operator'''
    p[0] = ('CLOSED_DYADIC_ASSIGNING_OPERATOR', [p[1]])


def p_if_action(p):
    r'''if_action : IF boolean_expression then_clause FI
                    | IF boolean_expression then_clause else_clause FI'''
    if len(p) == 5:
        p[0] = ('IF_ACTION', [p[2], p[3]])
    elif len(p) == 6:
        p[0] = ('IF_ACTION', [p[2], p[3], p[4]])


def p_then_clause(p):
    r'then_clause : THEN action_statement_list'
    p[0] = ('THEN_CLAUSE', [p[2]])


def p_else_clause(p):
    r'''else_clause : ELSE action_statement_list
                    | ELSEIF boolean_expression then_clause
                    | ELSEIF boolean_expression then_clause else_clause'''
    if len(p) == 3:
        p[0] = ('ELSE_CLAUSE', [p[2]])
    elif len(p) == 4:
        p[0] = ('ELSE_CLAUSE', [p[2], p[3]])
    elif len(p) == 5:
        p[0] = ('ELSE_CLAUSE', [p[2], p[3], p[4]])


def p_do_action(p):
    r'''do_action : DO action_statement_list OD
                    | DO control_part SEMICOLON action_statement_list OD'''
    if len(p) == 4:
        p[0] = ('DO_ACTION', [p[2]])
    elif len(p) == 6:
        p[0] = ('DO_ACTION', [p[2], p[4]])


def p_control_part(p):
    r'''control_part : for_control
                        | while_control'''
    p[0] = ('CONTROL_PART', [p[1]])


def p_for_control(p):
    r'for_control : FOR iteration'
    p[0] = ('FOR_CONTROL', [p[2]])


def p_iteration(p):
    r'''iteration : step_enumeration
                    | range_enumeration'''
    p[0] = ('ITERATION', [p[1]])


def p_step_enumeration(p):
    r'''step_enumeration : loop_counter EQUALS start_value end_value
                            | loop_counter EQUALS start_value step_value end_value
                            | loop_counter EQUALS start_value DOWN end_value
                            | loop_counter EQUALS start_value step_value DOWN end_value'''
    if len(p) == 5:
        p[0] = ('STEP_ENUMERATION', [p[1], p[3], p[4]])
    elif len(p) == 6 and p[3].type == 'step_value':
        p[0] = ('STEP_ENUMERATION', [p[1], p[3], p[4]])
    elif len(p) == 6 and p[3].type == 'DOWN':
        p[0] = ('STEP_ENUMERATION_DOWN', [p[1], p[4]])
    elif len(p) == 7:
        p[0] = ('STEP_ENUMERATION_DOWN', [p[1], p[3], p[4], p[6]])


def p_loop_counter(p):
    r'loop_counter : IDENTIFIER'
    p[0] = ('LOOP_COUNTER', [], p[1])


# integer expression ?
def p_start_value(p):
    r'start_value : expression'
    p[0] = ('START_VALUE', [p[1]])


# integer expression ?
def p_step_value(p):
    r'step_value : BY expression'
    p[0] = ('STEP_VALUE', [p[2]])


# integer expression ?
def p_end_value(p):
    r'end_value : TO expression'
    p[0] = ('END_VALUE', [p[2]])


# discrete_mode_name -> mode
def p_range_enumeration(p):
    r'''range_enumeration : loop_counter IN range_definition
                            | loop_counter DOWN IN range_definition'''
    if len(p) == 4:
        p[0] = ('RANGE_ENUMERATION', [p[1], p[3]])
    elif len(p) == 5:
        p[0] = ('RANGE_ENUMERATION', [p[1], p[4]])


# range_definition: mode | composite_object (location or expression)
def p_range_definition(p):
    r'''range_definition : expression'''
    p[0] = ('RANGE_DEFINITION', [p[1]])


def p_while_control(p):
    r'while_control : WHILE boolean_expression'
    p[0] = ('WHILE_CONTROL', [p[2]])


def p_call_action(p):
    r'''call_action : procedure_call
                        | builtin_call'''
    p[0] = ('CALL_ACTION', [p[1]])


def p_exit_action(p):
    r'exit_action : EXIT label'
    p[0] = ('EXIT_ACTION', [p[2]])


def p_return_action(p):
    r'''return_action : RETURN
                    | RETURN result'''
    if len(p) == 2:
        p[0] = ('RETURN_ACTION', [])
    elif len(p) == 3:
        p[0] = ('RETURN_ACTION', [p[2]])


def p_result_action(p):
    r'result_action : RESULT result'
    p[0] = ('RESULT_ACTION', [p[2]])


def p_result(p):
    r'result : expression'
    p[0] = ('RESULT', [p[1]])


def p_builtin_call(p):
    r'''builtin_call : builtin_name LPARENS RPARENS
                        | builtin_name LPARENS parameter_list RPARENS '''
    if len(p) == 4:
        p[0] = ('BUILTIN_CALL', [p[1]])
    elif len(p) == 5:
        p[0] = ('BUILTIN_CALL', [p[1], p[3]])


def p_builtin_name(p):
    r'''builtin_name : NUM
                        | PRED
                        | SUCC
                        | UPPER
                        | LOWER
                        | LENGTH
                        | READ
                        | PRINT
                        | NEW
                        | FREE'''
    p[0] = ('BUILTIN_NAME', [], p[1])


# Mode
def p_mode(p):
    r'''mode : mode_name
                | discrete_mode
                | reference_mode
                | composite_mode'''
    p[0] = p[1]


def p_mode_name(p):
    r'mode_name : IDENTIFIER'
    p[0] = ('MODE_NAME', [], p[1])


def p_discrete_mode(p):
    r'''discrete_mode : INT
                        | BOOL
                        | CHAR'''
    p[0] = ('DISCRETE_MODE', [], p[1])


def p_reference_mode(p):
    r'reference_mode : REF mode'
    p[0] = ('REFERENCE_MODE', [p[2]])


def p_composite_mode(p):
    r'''composite_mode : string_mode
                        | array_mode
                        | struct_mode'''
    p[0] = p[1]


def p_string_mode(p):
    r'string_mode : CHARS LBRACKET integer_literal RBRACKET'
    p[0] = ('STRING_MODE', [p[3]])


def p_array_mode(p):
    r'array_mode : ARRAY LBRACKET index_mode_list RBRACKET element_mode'
    p[0] = ('ARRAY_MODE', [p[3]])


def p_element_mode(p):
    r'element_mode : mode'
    p[0] = ('ELEMENT_MODE', [p[1]])


def p_index_mode_list(p):
    r'''index_mode_list : index_mode_list COMMA index_mode
                            | index_mode'''
    if len(p) == 2:
        p[0] = ('INDEX_MODE_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('INDEX_MODE_LIST', p[1][1])


def p_index_mode(p):
    r'index_mode : literal_range'
    p[0] = ('INDEX_MODE', [p[1]])


def p_struct_mode(p):
    r'struct_mode : STRUCT LPARENS field_list RPARENS'
    p[0] = ('STRUCT_MODE', [p[3]])


def p_field_list(p):
    r'''field_list : field_list COMMA fields_declaration
                   | fields_declaration'''
    if len(p) == 2:
        p[0] = ('FIELD_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('FIELD_LIST', p[1][1])


def p_fields_declaration(p):
    r'fields_declaration : identifier_list mode'
    p[0] = ('FIELDS_DECLARATION', [p[1], p[2]])


def p_literal_range(p):
    r'literal_range : integer_literal COLON integer_literal'
    p[0] = ('LITERAL_RANGE', [p[1], p[3]])


# Expression
def p_expression_list(p):
    r'''expression_list : expression_list COMMA expression
                        | expression'''
    if len(p) == 2:
        p[0] = ('EXPRESSION_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('EXPRESSION_LIST', p[1][1])


def p_expression(p):
    r'''expression : operand0
                        | conditional_expression'''
    p[0] = ('EXPRESSION', [p[1]])


def p_conditional_expression(p):
    r'''conditional_expression : IF boolean_expression then_expression else_expression FI
                                | IF boolean_expression then_expression elseif_expression else_expression FI'''
    if len(p) == 5:
        p[0] = ('CONDITIONAL_EXPRESSION', [p[2], p[3], p[4]])
    elif len(p) == 6:
        p[0] = ('CONDITIONAL_EXPRESSION', [p[2], p[3], p[4], p[5]])


def p_boolean_expression(p):
    r'boolean_expression : expression'
    p[0] = ('BOOLEAN_EXPRESSION', [p[1]])


def p_then_expression(p):
    r'then_expression : THEN expression'
    p[0] = ('THEN_EXPRESSION', [p[2]])


def p_elseif_expression(p):
    r'''elseif_expression : elseif_expression ELSEIF boolean_expression then_expression
                            | ELSEIF boolean_expression then_expression'''
    if len(p) == 3:
        p[0] = ('ELSEIF_EXPRESSION', [p[2], p[3]])
    elif len(p) == 6:
        p[0] = ('ELSEIF_EXPRESSION', [p[1], p[3], p[4]])


def p_else_expression(p):
    r'''else_expression : ELSE expression'''
    p[0] = ('ELSE_EXPRESSION', [p[2]])


def p_operand0(p):
    r'''operand0 : operand0 operator1 operand1
                    | operand1'''
    if len(p) == 4:
        p[0] = (p[2][0], [p[1], p[3]])
    elif len(p) == 2:
        p[0] = p[1]


def p_operator1(p):
    r'''operator1 : relational_operator
                    | membership_operator'''
    p[0] = p[1]


# some of these apply to booleans, others to integers... maybe we should pull them apart
def p_relational_operator(p):
    r'''relational_operator : AND
                                | OR
                                | NOT
                                | EQ
                                | NEQ
                                | GT
                                | GE
                                | LT
                                | LE'''
    p[0] = ('{}_OPERATOR'.format(p.slice[1].type), [])


def p_membership_operator(p):
    r'membership_operator : IN'
    p[0] = ('MEMBERSHIP_OPERATOR', [], p[1])


def p_operand1(p):
    r'''operand1 : operand1 operator2 operand2
                    | operand2'''
    if len(p) == 4:
        p[0] = (p[2][0], [p[1], p[3]])
    elif len(p) == 2:
        p[0] = p[1]


def p_operator2(p):
    r'''operator2 : arithmetic_additive_operator
                    | string_concatenation_operator'''
    p[0] = p[1]


def p_arithmetic_additive_operator(p):
    r'''arithmetic_additive_operator : PLUS
                                        | MINUS'''
    p[0] = ('{}_OPERATOR'.format(p.slice[1].type), [])


def p_string_concatenation_operator(p):
    r'string_concatenation_operator : STRINGCONCAT'
    p[0] = ('STRING_CONCATENATION_OPERATOR', [])


def p_operand2(p):
    r'''operand2 : operand2 arithmetic_multiplicative_operator operand3
                    | operand3'''
    if len(p) == 4:
        p[0] = (p[2][0], [p[1], p[3]])
    elif len(p) == 2:
        p[0] = p[1]


def p_arithmetic_multiplicative_operator(p):
    r'''arithmetic_multiplicative_operator : TIMES
                                            | DIVIDE
                                            | MODULO'''
    p[0] = ('{}_OPERATOR'.format(p.slice[1].type), [])


def p_operand3(p):
    r'''operand3 : operand4
                   | monadic_operator operand4'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1][0], [p[2]])


def p_monadic_operator(p):
    r'''monadic_operator : MINUS
                            | NOT'''
    p[0] = ('{}_OPERATOR'.format(p.slice[1].type), [])


def p_operand4(p):
    r'''operand4 : location
                    | referenced_location
                    | primitive_value'''
    p[0] = p[1]


# Location
def p_location(p):
    r'''location : location_name
                    | dereferenced_reference
                    | composite_element
                    | composite_slice
                    | procedure_call'''
    p[0] = p[1]


def p_location_name(p):
    r'location_name : IDENTIFIER'
    p[0] = ('LOCATION_NAME', [], p[1])


def p_dereferenced_reference(p):
    r'dereferenced_reference : primitive_value ARROW'
    p[0] = ('DEREFERENCED_REFERENCE', [p[1]])


# maybe use integer_expression instead of expression?
def p_composite_element(p):
    r'composite_element : location LBRACKET expression RBRACKET'
    p[0] = ('COMPOSITE_ELEMENT', [p[1], p[3]])


# maybe use integer_expression instead of expression?
def p_composite_slice(p):
    r'composite_slice : location LBRACKET expression COLON expression RBRACKET'
    p[0] = ('COMPOSITE_SLICE', [p[1], p[3], p[5]])


def p_referenced_location(p):
    r'referenced_location : ARROW location'
    p[0] = ('REFERENCED_LOCATION', [p[1]])


# Value
def p_primitive_value(p):
    r'''primitive_value : literal
                        | value_array_element
                        | value_array_slice
                        | parenthesized_expression'''
    p[0] = p[1]


# Literal
def p_literal(p):
    r'''literal : integer_literal
                    | boolean_literal
                    | character_literal
                    | empty_literal
                    | character_string_literal'''
    p[0] = p[1]


def p_integer_literal(p):
    r'integer_literal : NUMBERCONST'
    p[0] = ('INTEGER_LITERAL', [], int(p[1]))


def p_boolean_literal(p):
    r'''boolean_literal : FALSE
                            | TRUE'''
    p[0] = ('BOOLEAN_LITERAL', [], True if p[1] == 'true' else False)


def p_character_literal(p):
    r'character_literal : CHARCONST'
    p[0] = ('CHARACTER_LITERAL', [], p[1][0])


def p_empty_literal(p):
    r'empty_literal : NULL'
    p[0] = ('empty_literal', [], p[1])


def p_character_string_literal(p):
    r'character_string_literal : STRINGCONST'
    p[0] = ('CHARACTER_STRING_LITERAL', [], p[1])


# integer_expression_list?
def p_value_array_element(p):
    r'value_array_element : array_primitive_value LBRACKET expression_list RBRACKET'
    p[0] = ('VALUE_ARRAY_ELEMENT', [p[1], p[3]])


def p_value_array_slice(p):
    r'value_array_slice : array_primitive_value LBRACKET expression COLON expression RBRACKET'
    p[0] = ('VALUE_ARRAY_SLICE', [p[1], p[3], p[5]])


def p_array_primitive_value(p):
    r'array_primitive_value : primitive_value'
    p[0] = ('ARRAY_PRIMITIVE_VALUE', [p[1]])


def p_parenthesized_expression(p):
    r'parenthesized_expression : LPARENS expression RPARENS'
    p[0] = p[2]


# Procedure call
def p_procedure_call(p):
    r'''procedure_call : procedure_name LPARENS RPARENS
                            | procedure_name LPARENS parameter_list RPARENS'''
    if len(p) == 4:
        p[0] = ('PROCEDURE_CALL', [p[1]])
    elif len(p) == 5:
        p[0] = ('PROCEDURE_CALL', [p[1], p[3]])


def p_procedure_name(p):
    r'procedure_name : IDENTIFIER'
    p[0] = ('PROCEDURE_NAME', [], p[1])


def p_parameter_list(p):
    r'''parameter_list : parameter_list COMMA parameter
                        | parameter'''
    if len(p) == 2:
        p[0] = ('PARAMETER_LIST', [p[1]])
    elif len(p) == 4:
        p[1][1].append(p[3])
        p[0] = ('PARAMETER_LIST', p[1][1])


def p_parameter(p):
    r'parameter : expression'
    p[0] = ('PARAMETER', [p[1]])

def p_empty(p):
    r'empty :'
    pass


parser = yacc.yacc()
