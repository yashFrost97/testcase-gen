""""
Parser for the dot file dumped by TLA+ toolbox.
Usage: python dotparser.py [absolute file path]
a -> b[label="", foo=", bar=""] - This is an edge from a to b, [] contains attributes of the edge
a[] - This denotes a node and its attributes.
"""
import collections
import re
from collections import deque
import tlaparser
from copy import deepcopy
import argparse
import sys


# -8631748407493987020 [label="/\\ decision = <<FALSE, FALSE, FALSE>>\n/\\ k = <<1, 1, 1>>\n/\\ p1v = <<1, 0, 0>>\n/\\ pc = <<\"START\", \"START\", \"START\">>\n/\\ p2v = <<-1, -1, -1>>\n/\\ p2Msg = {}\n/\\ decided = <<-1, -1, -1>>\n/\\ p1Msg = {}",style = filled]
node_pattern = re.compile(r'(?P<id>-?\d+)\s+\[label="(?P<tla_stuff>.+)".*];?')

# 6798208728600954568 -> 8768434477171639267 [label="",color="2",fontcolor="2"];
edge_pattern = re.compile(
    r'(?P<from_node>-?\d+)\s+->\s+(?P<to_node>-?\d+)\s+'
    r'\[label="(?P<label>.+?)"(,|).*];?')


class DotGraph:

	def __init__(self):
		self._edge_transition = {}
		self._state_to_id = {}
		self._id_to_state = {}
		self.init_state = None

	def set_init_state(self, state):
		if not self.init_state is None:
			self.init_state = state

	def add_state(self, state, state_id):
		self._state_to_id[state] = state_id
		self._id_to_state[state_id] = state

	def add_edge(self, label, from_node_id, to_node_id):
		action_to_id = self._edge_transition.setdefault(from_node_id, {})
		action_to_id.setdefault(label, set()).add(to_node_id)


	def __str__(self) -> str:
		s = '\n'.join(["{}:{}".format(key, val) for key, val in self._edge_transition.items()])
		s += "\n State to ID: \n"
		s += '\n'.join(["{}:{}".format(key,val) for key,val in self._state_to_id.items()])
		s += "\n ID to State: \n"
		s += '\n'.join(["{}:{}".format(key,val) for key,val in self._id_to_state.items()])
		return s

	def print_edges(self):
		for k,v in self._edge_transition.items():
			print(k, v, "\n")
		print(len(self._edge_transition))
		# print(self._edge_transition[list(self._edge_transition.keys())[0]])
		# print("Len of edges: ", len(self._edge_transition))
		# print("Len of state to id: ",len(self._state_to_id))
		# print("Len of id to state: ",len(self._id_to_state))



	def all_traces(self, source = 6798208728600954568, target = 176509315602857959):
		results = []
		graph = self.flatten()
		
		def backtrack(current, path):
			# print(current)
			if current == target:
				results.append(list(path))
				return
			for next in graph[current]:
				path.append(next)
				backtrack(next, path)
				path.pop()

		path = deque([source])
		backtrack(source, path)

		return results


	def flatten(self):
		graph_copy = deepcopy(self._edge_transition)
		graph = collections.defaultdict(list)
		for key, val_dict in graph_copy.items():
			for label, vals in val_dict.items():
				for node in vals:
					graph[key].append(node)

		return graph


def dotparser(lines):
	new_graph = DotGraph()
	node_count = 0
	edge_count = 0
	print("Parsing Lines")
	for line in lines:
		# regex match for nodes
		node_match = node_pattern.match(line)
		if node_match:
			node_count += 1
			tla_stuff = node_match.group("tla_stuff")
			id = node_match.group("id")
			# parse the tla stuff to a state
			# if first state set it as the starting state -> init state
			# for the rest: add the state to the graph
			tla = tla_stuff.encode().decode("unicode_escape")
			state = tlaparser.parse_tla(tla)
			if new_graph.init_state is None:
				new_graph.init_state = state
			else:
				new_graph.add_state(state, id)
			continue
		# regex match for edges
		edge_match = edge_pattern.match(line)
		if edge_match:
			edge_count += 1
			from_id = edge_match.group("from_node")
			to_id = edge_match.group("to_node")
			tla_label = edge_match.group("label")

			new_graph.add_edge(tla_label, int(from_id), int(to_id))

	print("Parsing Done")
	print("Node count: ", node_count, " Edge count: ", edge_count)
	print("Returning the graph")
	return new_graph


def main():
	my_args = argparse.ArgumentParser(description="Input the absolute .dot file path")
	my_args.add_argument('Path', metavar="path", type=str, help="Absolute .dot File Path")
	arg = my_args.parse_args()
	input = arg.Path

	try:
		file = open(input, "r")
		lines = file.readlines()
		file.close()

		print("File found!")
		print("Beginning to parse the DOT File")
		graph = dotparser(lines)

		print("Generating all possible trace behaviours!")
		traces = graph.all_traces() # contains all paths
		print(f"Number of trace behaviours are: {len(traces)}")

	except:
		print(f'File: {input} does not exist!')

if __name__ == "__main__":
	main()