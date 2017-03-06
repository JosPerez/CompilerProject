import sys
sys.path.insert(0,"../..")
import ply.lex as lex
import decimal

tokens = ('VAR','NUMBER','ASSIGN','EQUALS','LESST','LESSET','GREATT','GREATET','IF','ELSE','LOOP','PLUS','MINUS','MULT','DIV','STRING','LPAR','RPAR','WS')

t_EQUALS = r'=='
t_ASSIGN = r'='
t_LESST = r'<'
t_LESSET = r'<='
t_GREATT = r'>'
t_GREATET = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

RESERVED = {
	"if": "IF",
	"else":"ELSE",
	"loop":"LOOP",
}

def t_NUMBER(t):
	r"(\d+(\.\d*)?|\/\d+)([eE][-+]?\d+)"
	t.value = decimal.Decimal(t.value)
	return t
def t_STRING(t):
	r"'([^\\']+|\\'||\\\\)*'"
	t.value = t.value[1:-1].decode("string-escape")
	return t
def t_VAR(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = RESERVED.get(t.value,"NAME")
	return t
def t_LPAR(t):
	r'\('
	t.lexer.paren_count +=1
	return t
def t_RPAR(t):
	r'\)'
	t.lexer.paren_count -=1
	return t
def t_WS(t):
	r'[ ]+'
	if t.lexer.at_line_start and t.lexer.paren_count == 0 :
		return t
def t_error(t):
	raise SyntaxError("Unknown type %r" % (t.value[0],))
	print "Skipping", repr(t.value[0])
	t.lexer.skip(1)	

NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2

def track_tokens(lexer, tokens):
	lexer.at_line_start = at_line_start = True
	indent = NO_INDENT
	for token in tokens:
		token.at_line_start = at_line_start
		if token.type ==  "WS":
			assert token.at_line_start == True
			at_line_start = True
			token.must_indent = False
		else:
			if indent == MUST_INDENT:
				token.must_indent = True
			else:
				token.must_indent = False
			at_line_start = False
			indent = NO_INDENT
		yield token
		lexer.at_line_start = at_line_start

def _new_token(type,lineno):
	tok = lex.LexToken()
	tok.type = type
	tok.value = None
	tok.lineno = lineno
	return tok

def DEDENT(lineno):
	return _new_token("DEDENT",lineno)
def INDENT(lineno):
	return _new_token("INDENT",lineno)


lexer = lex.lex()