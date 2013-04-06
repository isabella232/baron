#!/usr/bin/python
# -*- coding:Utf-8 -*-

from grammator import parser, Token

def parse(tokens, result):
    assert parser.parse(iter(map(lambda x: Token(*x) if x else x, tokens + [('ENDMARKER', ''), None]))) == result

def test_empty():
    parse([], [])

def test_space():
    parse([('SPACE', '   ')], [{"type": "space", "value": "   "}])

def test_int():
    parse([('INT', '1')], [{"type": "expression", "value": {"type": "int", "section": "number", "value": "1"}}])

def test_endl():
    parse([('ENDL', '\n')], [{"type": "endl", "value": "\n", "before_space": ""}])

def test_space_endl():
    parse([('SPACE', '   '), ('ENDL', '\n')], [{"type": "endl", "value": "\n", "before_space": "   "}])

def test_some_stuff():
    parse([('INT', '3'), ('SPACE', '   '), ('ENDL', '\n'), ('INT', '42')], [{"type": "expression", "value": {"type": "int", "section": "number", "value": "3"}}, {"type": "endl", "value": "\n", "before_space": "   "}, {"type": "expression", "value": {"type": "int", "section": "number", "value": "42"}}])

def test_name():
    parse([('NAME', 'a')], [{"type": "expression", "value": {"type": "name", "value": "a"}}])

def test_string():
    parse([('STRING', '"pouet pouet"')], [{"type": "expression", "value": {"type": "string", "value": '"pouet pouet"'}}])
    parse([('STRING', '"""pouet pouet"""')], [{"type": "expression", "value": {"type": "string", "value": '"""pouet pouet"""'}}])

def test_simple_import():
    parse([('IMPORT', 'import'), ('SPACE', '  '), ('NAME', 'pouet')], [{"type": "import", "space": "  ", "value": {"type": "dotted_name", "value": [{"type": "name", "value": "pouet"}]}}])

def test_import_basic_dot():
    parse([('IMPORT', 'import'), ('SPACE', '  '), ('NAME', 'pouet'), ('DOT', '.'), ('NAME', 'blob')], [{"type": "import", "space": "  ", "value": {"type": "dotted_name", "value": [{"type": "name", "value": "pouet"}, {"type": "dot", "value": "."}, {"type": "name", "value": "blob"}]}}])

def test_import_more_dot():
    parse([('IMPORT', 'import'), ('SPACE', '  '), ('NAME', 'pouet'), ('DOT', '.'), ('NAME', 'blob'), ('SPACE', ' '), ('DOT', '.'), ('NAME', 'plop')], [{"type": "import", "space": "  ", "value": {"type": "dotted_name", "value": [{"type": "name", "value": "pouet"}, {"type": "dot", "value": "."}, {"type": "name", "value": "blob"}, {"type": "space", "value": " "}, {"type": "dot", "value": "."}, {"type": "name", "value": "plop"}]}}])

# dotted_name: NAME
# dotted_name: NAME.NAME
# dotted_name: NAME(.NAME)+

# dotted_as_name: dotted_name
# dotted_as_name: dotted_name SPACE 'as' SPACE NAME

# dotted_as_names: dotted_as_name
# dotted_as_names: dotted_as_name [SPACE] ',' [SPACE] dotted_as_name
# dotted_as_names: dotted_as_name ([SPACE] ',' [SPACE] dotted_as_name)*

# import_as_name: NAME
# import_as_name: NAME SPACE 'as' SPACE NAME

# import_as_names: import_as_name
# import_as_names: import_as_name [SPACE] ',' [SPACE] import_as_name
# import_as_names: import_as_name ([SPACE] ',' [SPACE] import_as_name)*
# import_as_names: import_as_name ([SPACE] ',' [SPACE] import_as_name)* [SPACE] [',']

# import_name: 'import' SPACE dotted_as_names

# import_from: 'from' SPACE dotted_name SPACE 'import' SPACE import_as_names
# import_from: 'from' SPACE dotted_name SPACE 'import' [SPACE] '(' [SPACE] import_as_names [SPACE] ')'
# import_from: 'from' SPACE dotted_name SPACE 'import' [SPACE] '*'

# import_from: 'from' [SPACE] '.'* [SPACE] dotted_name SPACE 'import' ...........
# import_from: 'from' [SPACE] '.'+ [SPACE] 'import' ...........

# ----------

# stmt: simple_stmt
# stmt: compound_stmt

# simple_stmt: small_stmt [SPACE] NEWLINE
# simple_stmt: small_stmt [SPACE] ';' [SPACE] NEWLINE
# simple_stmt: small_stmt [SPACE] ';' small_stmt [SPACE] ';' [SPACE] NEWLINE
# simple_stmt: small_stmt ([SPACE] ';' small_stmt [SPACE] ';') [SPACE] NEWLINE

# small_stmt: expr_stmt
# small_stmt: print_stmt
# small_stmt: del_stmt
# small_stmt: pass_stmt
# small_stmt: flow_stmt
# small_stmt: import_stmt
# small_stmt: global_stmt
# small_stmt: exec_stmt
# small_stmt: assert_stmt

# expr_stmt: testlist
# expr_stmt: testlist ([SPACE] '=' [SPACE] testlist)*
# expr_stmt: testlist ([SPACE] '=' [SPACE] yield_expr)*
# expr_stmt: testlist augassign yield_expr
# expr_stmt: testlist augassign testlist

# testlist: test
# testlist: test [SPACE] [',']
# testlist: test ([SPACE] ',' [SPACE] test)*
# testlist: test ([SPACE] ',' [SPACE] test)* [SPACE] [',']

# test: lambdef
# test: or_test
# test: or_test [SPACE 'if' SPACE or_test SPACE 'else' SPACE test]

# or_test: and_test
# or_test: and_test (SPACE 'or' SPACE and_test)*

# and_test: not_test
# and_test: not_test (SPACE 'and' SPACE not_test)*

# not_test: 'not' SPACE not_test
# not_test: comparison

# comparison: expr
# comparison: expr (comp_op expr)*

# comp_op: '<'
# comp_op: '>'
# comp_op: '=='
# comp_op: '>='
# comp_op: '<='
# comp_op: '<>'
# comp_op: '!='
# comp_op: 'in'
# comp_op: 'not' SPACE 'in'
# comp_op: 'is'
# comp_op: 'is' SPACE 'not'

# expr: xor_expr
# expr: xor_expr ([SPACE] '|' [SPACE] xor_expr)*

# xor_expr: and_expr
# xor_expr: and_expr ([SPACE] '^' [SPACE] and_expr)*

# and_expr: shift_expr
# and_expr: shift_expr ([SPACE] '&' [SPACE] shift_expr)*

# shift_expr: arith_expr
# shift_expr: arith_expr ([SPACE] ('<<'|'>>') [SPACE] arith_expr)*

# arith_expr: term
# arith_expr: term ([SPACE] ('+'|'-') [SPACE] term)*

# term: factor
# term: factor ([SPACE] ('*'|'/'|'%'|'//') [SPACE] factor)*

# factor: ('+'|'-'|'~') [SPACE] factor
# factor: power

# power: atom [SPACE] trailer* [[SPACE] '**' [SPACE] factor]

# trailer: '.' [SPACE] NAME
# trailer: '[' [SPACE] subscriptlist [SPACE] ']'
# trailer: '(' [SPACE] [arglist] [SPACE] ')'

# atom: '(' [SPACE] [testlist_comp] [SPACE] ')'
# atom: '(' [SPACE] [yield_expr] [SPACE] ')'
# atom: '[' [SPACE] [listmaker] [SPACE] ']'
# atom: '{' [SPACE] [dictorsetmaker] [SPACE] '}'
# atom: '`' [SPACE] testlist1 [SPACE] '`'
### atom: NAME
### atom: NUMBER
### atom: STRING+
