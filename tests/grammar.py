from nltk import parse_cfg, ChartParser
from random import choice

def produce(grammar, symbol, minlen):
	words = []
	if minlen>=1:
		productions = grammar.productions(lhs = symbol)
		print "Productions:",productions
		production = choice(productions)
		#for production in productions:
		for sym in production.rhs():
			#print "Symbol: ",sym
			if symbol in ('N1','N2'):
				minlen=minlen-1
			if isinstance(sym, str):
				words.append(sym)
			else:
				words.extend(produce(grammar, sym, minlen))
	return words




grammar = parse_cfg('''
F -> N1 '(' P ')' | N2 '(' P ',' P ')'
N1 -> 'half'
N2 -> 'sum'
P -> 'a' | 'b' | F
''')

'''
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
V -> 'shot' | 'killed' | 'wounded'
Det -> 'an' | 'my' 
N -> 'elephant' | 'pajamas' | 'cat' | 'dog'
P -> 'in' | 'outside'
'''

parser = ChartParser(grammar)

gr = parser.grammar()
print ' '.join(produce(gr, gr.start(),3))

