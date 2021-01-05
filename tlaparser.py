from lark import Lark, tree
from typing import Tuple, List

class SystemState:
	""" Class for system variables, as seen in TLA+.
	 """
	p1val: List[int]
	p2val: List[int]
	round: List[int]
	decided: List[int]
	decision: List[bool]

	def __init__(self, round, p1val, p2val, decided, decision):
		self.round = round
		self.p1val = p1val
		self.p2val = p2val
		self.decided = decided
		self.decision = decision

	def __repr__(self):
		s = f'round:{self.round}, p1val:{self.p1val}, p2val:{self.p2val}, decided:{self.decided}, decision:{self.decision}'
		return s


	def __str__(self):
		s = f'round:{self.round}, p1val:{self.p1val}, p2val:{self.p2val}, decided:{self.decided}, decision:{self.decision}'
		return s

""""
	Use paxos_grammars.lark for parsing paxos tla dot dump.
	grammars.lark was for benor. 
"""
with open("grammars.lark", "r") as grammar_file:
	lark_parser = Lark(grammar_file, start="state",propagate_positions=True)

def parse_tla(sample):
	parse_tree = lark_parser.parse(sample)
	state_dict = {}
	for child in parse_tree.children:
		state_dict[child.children[0]] = child.children[1]

	# parse_round(state_dict["k"])
	# parse_p1(state_dict["p1v"])
	# parse_p2(state_dict["p2v"])
	# parse_decided(state_dict["decided"])
	# parse_decision(state_dict["decision"])
	return SystemState(round = parse_round(state_dict['k']), p1val = parse_p1(state_dict["p1v"]), p2val = parse_p2(state_dict["p2v"]), decided = parse_decided(state_dict["decided"]), decision = parse_decision(state_dict["decision"]))


def parse_round(stuff):
	# need to find a better method to do this
	rnd = []
	rnd.append(int(stuff.children[0].children[1].children[0].children[0]))
	rnd.append(int(stuff.children[0].children[2].children[0].children[0]))
	rnd.append(int(stuff.children[0].children[3].children[0].children[0]))
	return list(rnd)


def parse_p1(stuff):
	# help
	p1v = []
	p1v.append(int(stuff.children[0].children[1].children[0].children[0]))
	p1v.append(int(stuff.children[0].children[2].children[0].children[0]))
	p1v.append(int(stuff.children[0].children[3].children[0].children[0]))
	return list(p1v)


def parse_p2(stuff):
	p2v = []
	p2v.append(int(stuff.children[0].children[1].children[0].children[0]))
	p2v.append(int(stuff.children[0].children[2].children[0].children[0]))
	p2v.append(int(stuff.children[0].children[3].children[0].children[0]))
	return list(p2v)


def parse_decided(stuff):
	decided = []
	decided.append(int(stuff.children[0].children[1].children[0].children[0]))
	decided.append(int(stuff.children[0].children[2].children[0].children[0]))
	decided.append(int(stuff.children[0].children[3].children[0].children[0]))
	return list(decided)


def parse_decision(stuff):
	# print(stuff.children[0].children[1].children[0].children[0].value)
	deci = []
	deci.append(additional_processing(stuff.children[0].children[1].children[0].children[0].value))
	deci.append(additional_processing(stuff.children[0].children[2].children[0].children[0].value))
	deci.append(additional_processing(stuff.children[0].children[3].children[0].children[0].value))
	return list(deci)


def additional_processing(temp):
	if temp == "FALSE":
		return False
	else:
		return True
