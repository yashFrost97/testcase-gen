"""
OBSOLETE UTILITY FUNCTIONS
NOT IN USE.
"""

def dfs(self):
	if not self._edge_copied:
		self._dfs_edges = deepcopy(self._edge_transition)
		self._edge_copied = True
	start_node = list(self._dfs_edges.keys())[0]
	visited = set()

	self.dfs_recursive(start_node, visited, 0)
	return self.path


def dfs_recursive(self, v, visited, count):
	visited.add(v)
	print("Node visited: ", v, " node count: ", count)
	self.path.append(v)
	count+=1

	for label, neighbour in self._dfs_edges[v].items():
		to_visit = neighbour.pop()
		if to_visit not in visited:
			self.dfs_recursive(to_visit, visited, count)

def allPaths(self, source = 6798208728600954568, target = 176509315602857959):
	is_visited = {}
	path = []
	self._dfs_edges = deepcopy(self._edge_transition)
	print("Start!")
	self.allPathsRecur(source, target, is_visited, path)

def allPathsRecur(self, s, d, is_visited, path):
	# marking the node s as visited and appending to path
	is_visited[s] = True
	path.append(s)
	# print("in recur")

	# if current node s is destination d, print all paths and gg
	if s == d:
		print(len(path))
	else:
		for label, i in self._dfs_edges[s].items():
			to_visit = i.pop()
			if to_visit not in is_visited.keys() or not is_visited[to_visit]:
				self.allPathsRecur(to_visit, d, is_visited, path)
