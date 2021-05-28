#
from __future__ import annotations
import node as N
import connection as C
import matrix
from copy import deepcopy

class Polygon:
	def __init__(self, nodes : list[N.Node]):
		self.nodes = nodes

	def __str__(self):
		return '\n* '.join(map(str, self.nodes))

	def __len__(self):
		return len(self.nodes)

	def __getitem__(self, index : int):
		return self.nodes[index]

	def __iter__(self):
		return iter(self._hash_iter_triplets())

	def _iter_triplets(self):
		triplet_list = []
		for node in self.nodes:
			for triplet in node.get_triplets():
				# check unique-ness
				if Polygon._triplet_in_list(triplet_list, triplet):
					continue
				# it is unique, so we can add it to the list
				triplet_list.append(triplet)
		print('num triplets', len(triplet_list))
		return triplet_list

	def _hash_iter_triplets(self):
		triplet_list = []
		triplet_hash_set = set()
		triplet_hash_func = lambda triplet: sum([sum([int(triplet[i][j] * 10e3) ** (j + 3) for j in range(3)]) for i in range(3)]) # pay atention to when a triplet is unique !
		for node in self.nodes:
			for triplet in node.get_triplets():
				# check unique-ness
				triplet_hash = triplet_hash_func(triplet)
				if triplet_hash in triplet_hash_set:
					continue
				triplet_hash_set.add(triplet_hash)
				# it is unique, so we can add it to the list
				triplet_list.append(triplet)
		print('num hash triplets', len(triplet_hash_set))
		return triplet_list

	@staticmethod
	def _triplet_in_list(triplet_list, triplet) -> bool:
		if triplet in triplet_list: return True
		for other_triplet in triplet_list:
			if triplet[0] in other_triplet and triplet[1] in other_triplet and triplet[2] in other_triplet:
				return True
		return False

	@staticmethod
	def unique_triplets(triplets):
		index = 0
		length = len(triplets)
		while index < length:
			triplet = triplets.pop(index) # pop it from the list
			if Polygon._triplet_in_list(triplets, triplet):
				length -= 1
			else:
				# add it back and go one forward
				triplets.insert(index, triplet)
				index += 1
		return triplets

	@staticmethod
	def from_raw_points(points : list[tuple[float]], index_list : list[int], inverse_index_list : bool = False, connect_endpoints : bool = True) -> Polygon:
		'''
		'''
		nodes : list[N.Node] = []
		num_points = len(points)
		processed_points = []
		index = num_nodes = 0
		if inverse_index_list:
			index_set = set(range(len(points))) # all indexes
			index_set -= set(index_list) # remove those from the initially given index_list
			index_list = list(index_set) # reassign index_list
		# process all points at least once
		while index < num_points:
			if index in index_list:
				connection_type = 'main'
			else:
				connection_type = 'graphical'
			current = points[index]
			print('doing', current, 'conn type:', connection_type)
			node = N.Node(current[0], current[1], current[2])
			# check for reconnection
			if current in processed_points:
				point_index = processed_points.index(current)
				connect_node = nodes[point_index]
				connect_node.connect(nodes[-1], connection_type)
				index += 1
				print('already processed point:', connect_node, '&', nodes[-1])
				continue
			# connect
			if num_nodes > 0:
				node.connect(nodes[-1], connection_type)
				print('-1 connected', node, 'with', nodes[-1])

			# append
			nodes.append(node)
			processed_points.append(current)
			num_nodes += 1
			# incr index
			index += 1
		# process edge-points (non yet-connected)
		if connect_endpoints:
			print('connecting endpoints')
			last_node = nodes[-1]
			for node in filter(lambda n: n.num_connections < 3, nodes[:-1]):
				node.connect(last_node, 'main')
				print('connected last with', node)

		return Polygon(nodes)

	@staticmethod
	def from_triangular_points(points : list[tuple[float]], index_list : list[int], inverse_index_list : bool = False, connect_endpoints : bool = True) -> Polygon:
		'''Create a polygon object from an ordered list of (x,y,z) points/coordinates
		The index_list indicates all the "real" points of the polygon. All points that are not in this index_list will be understood
		as 'graphical connection points'. You an also choose to give the index_list of the graphical connection points only. You then
		have to specify the 'inverse_index_list' as being 'True'. This will inverse the list. If 'connect_endpoints' is
		set to true, the last point and the first point will be connected as a 'main' connection (non graphical)
		'''
		nodes : list[N.Node] = []
		num_points = len(points)
		processed_points = []
		index = num_nodes = 0
		if inverse_index_list:
			index_set = set(range(len(points))) # all indexes
			index_set -= set(index_list) # remove those from the initially given index_list
			index_list = list(index_set) # reassign index_list
		# process all points at least once
		while index < num_points:
			if index in index_list:
				connection_type = 'main'
			else:
				connection_type = 'graphical'
			current = points[index]
			#print('doing', current, 'conn type:', connection_type)
			node = N.Node(current[0], current[1], current[2])
			# check for reconnection
			if current in processed_points:
				point_index = processed_points.index(current)
				connect_node = nodes[point_index]
				connect_node.connect(nodes[-1], connection_type)
				index += 1
				#print('not a main connection:', connect_node, '&', nodes[-1])
				continue
			# connect
			if num_nodes > 0:
				node.connect(nodes[-1], connection_type)
				#print('-1 connected', node, 'with', nodes[-1])
				if num_nodes > 1:
					node.connect(nodes[-2], connection_type)
					#print('-2 connected', node, 'with', nodes[-2])
			# append
			nodes.append(node)
			processed_points.append(current)
			num_nodes += 1
			# incr index
			index += 1
		# process edge-points (non yet-connected)
		if connect_endpoints:
			#print('connecting endpoints')
			last_node = nodes[-1]
			for node in filter(lambda n: n.num_connections < 3, nodes[:-1]):
				node.connect(last_node, 'main')
				#print('connected last with', node)

		return Polygon(nodes)

	@staticmethod
	def Chaikin3D(polygon : Polygon, n : int = 4) -> Polygon:
		'''ratio could also be float ?
		'''
		# init
		base_ratio = (n - 1) / n
		special_ratio = (n - 2) / (n - 1) # when the vector has already been trunced once
		node_dict : dict[N.Node, list[N.Node]] = dict()
		new_connections : list[C.Connection] = []

		old_nodes = deepcopy(polygon.nodes)

		sub_node_count = 0

		#
		for node_index,current_node in enumerate(polygon.nodes):
			print('\ncurrent node:', current_node)
			# create sub-nodes
			num_new_connections = num_graphical_nodes = 0
			sub_node_list : list[N.Node] = []
			graphical_connections : list[C.Connection] = []
			for conn in current_node.connection_list:
				if conn.type_ == 'main':
					#
					partner_node = conn.get_partner_node(current_node)
					print('\n - partner', partner_node)

					# calculate new pos (calculations done from num_connections to current node)
					u = matrix.vector.vector(partner_node.coords, current_node.coords)
					# get the right coefficient
					if partner_node not in polygon.nodes: # partner is one of the new nodes (already has been truncated once)
						print(' - special ratio')
						ratio = special_ratio
					else:
						ratio = base_ratio
					# new vector
					v : list[float] = matrix.vector.multiplication_k(u, ratio)
					w = matrix.vector.add(partner_node.coords, v)

					# create new N.Node & new Connection
					sub_node = N.Node.from_point(w)
					sub_conn = C.Connection(sub_node, partner_node, 'main')

					# re-connect connection to new node & vice-versa
					print(' * test\n  ->', '\n  -> '.join(map(str, partner_node.connection_list)))
					conn.update_node(current_node, sub_node)
					sub_node.connection_list = [conn]
					sub_node.num_connections = 1
					print(' * test\n  ->', '\n  -> '.join(map(str, partner_node.connection_list)))
					print(' - sub_node:', sub_node)
					print(' - sub_node connection:', ' ; '.join(map(str, sub_node.connection_list)))

					# add to list & increment num_new_connections
					print(' - adding', sub_node)
					sub_node_list.append(sub_node)
					num_new_connections += 1
				elif conn.type_ == 'graphical':
					graphical_connections.append(conn)
					print(' - added graphical connection:', conn)
				else:
					raise Exception('Unknown connection type:', conn.type_)
			# connect all the sub-nodes together (might find something to avoid connection-crossing -> len(sub_node_list) > 3)
			print(' - num sub-nodes', num_new_connections)
			for i in range(num_new_connections - 1):
				for j in range(i + 1, num_new_connections):
					sub_node_list[i].connect(sub_node_list[j], 'main')

			# add those sub-nodes to the new nodes list
			node_dict[old_nodes[node_index]] = sub_node_list
			print('sub-nodes:', len(sub_node_list))
			sub_node_count += len(sub_node_list)

		print('sub_node_count', sub_node_count)

		print('\nreconnection')
		# connect all the sub_nodes together
		processed_triplets : list[list[tuple[float]]] = []
		for old_node in old_nodes:
			print('old_node', old_node)
			chaikin_nodes_1 = node_dict[old_node]
			for old_conn in old_node.connection_list:
				old_conn_node = old_conn.get_partner_node(old_node)
				for old_sub_conn in filter(lambda old_sub_conn: not old_sub_conn.contains_node(old_node), old_conn_node.connection_list):
					old_sub_conn_node = old_sub_conn.get_partner_node(old_conn_node)
					if C.Connection.are_connected(old_sub_conn_node, old_node):
						triplet = [
							old_node.coords,
							old_conn_node.coords,
							old_sub_conn_node.coords
						]
						# have we already processed this triplet ?
						if Polygon._triplet_in_list(processed_triplets, triplet):
							continue
						processed_triplets.append(triplet)
						'''
						# centroid of triplet
						centroid_node = N.Node.from_point(matrix.centroid_of_triangle(old_node.coords, old_conn_node.coords, old_sub_conn_node.coords))
						'''
						# select the right sub-nodes to connect
						chaikin_nodes_2 = node_dict[old_conn_node]
						chaikin_nodes_3 = node_dict[old_sub_conn_node]
						selected_chaikin_nodes : set[N.Node] = set() # there should be exactly 6 nodes in it
						# search in chaikin-nodes 1
						for c_node_1 in chaikin_nodes_1:
							for c_node_2 in chaikin_nodes_2:
								if not C.Connection.are_connected(c_node_1, c_node_2): continue
								selected_chaikin_nodes.add(c_node_1)
								selected_chaikin_nodes.add(c_node_2)
							for c_node_3 in chaikin_nodes_3:
								if not C.Connection.are_connected(c_node_1, c_node_3): continue
								selected_chaikin_nodes.add(c_node_1)
								selected_chaikin_nodes.add(c_node_3)
						for c_node_2 in chaikin_nodes_2:
							for c_node_3 in chaikin_nodes_3:
								if not C.Connection.are_connected(c_node_2, c_node_3): continue
								selected_chaikin_nodes.add(c_node_2)
								selected_chaikin_nodes.add(c_node_3)
						print(selected_chaikin_nodes)
						assert len(selected_chaikin_nodes) == 6
						# select an 'intern' triangle from these nodes
						r'''
						The 'intern' triangle ABC for the chaikin groups 1, 2 & 3
						-------A-------------------------
						 \ 1  /                   \  2 /
						  \  /                     \  /
						   \/                       \/
						    \                       B
						     \                     /
						      \                   /
						       \                 /
						        \               /
						         \             /
						          \           /
						           \         /
						            \       /
						             C-----/
						              \ 3 /
						               \ /
						                v

						(note: there are two intern triangles for each set of 3 chaikin groups)
						'''
						for A_node in chaikin_nodes_1:
							# get the chaikin node from group 1 that is connected to the group 2
							if A_node in selected_chaikin_nodes and any([C.Connection.are_connected(A_node, c_n_2) for c_n_2 in chaikin_nodes_2]):
								# get the other chaikin node from group 2 (not connected to group 1, but group 3)
								B_node_possibilities = list(filter(lambda c_n_2: c_n_2 in selected_chaikin_nodes and not C.Connection.are_connected(A_node, c_n_2), chaikin_nodes_2))
								assert len(B_node_possibilities) == 1
								B_node = B_node_possibilities[0]
								# get the node from group 3
								C_node_possibilities = list(filter(lambda c_n_3: c_n_3 in selected_chaikin_nodes and not C.Connection.are_connected(B_node, c_n_3), chaikin_nodes_3))
								assert len(C_node_possibilities) == 1
								C_node = C_node_possibilities[0]
								break
						else:
							raise Exception('No intern triangle found for {} & {} & {}'.format(chaikin_nodes_1, chaikin_nodes_2, chaikin_nodes_3))

						# connect the nodes
						A_node.connect(B_node, 'graphical')
						A_node.connect(C_node, 'graphical')
						B_node.connect(C_node, 'graphical')

		# construct new node list
		new_node_list : list[N.Node] = []
		for _,sub_nodes in node_dict.items():
			new_node_list.extend(sub_nodes)

		print('num nodes:', len(new_node_list))

		# return the final polygon
		return Polygon(new_node_list)

	@staticmethod
	def _find_chaikin_groups(chaikin_node : N.Node) -> list[set[N.Node]]:
		# trivial chaikin groups
		pass

	@staticmethod
	def _connect_chaikin_group(group_set : set[N.Node]) -> None:
		ordered_group : list[N.Node] = Polygon._order_chaikin_group(group_set)
		length = len(group_set)
		num_iter = int(matrix.np.log2(length)) - 1
		print('number of iterations: {} for {} nodes'.format(num_iter, length))
		for x in range(num_iter):
			step = 2 ** (x + 1)
			print('step:', step)
			prev_node = ordered_group[0]
			for i in range(step, length, step):
				current_node = ordered_group[i]
				prev_node.connect(current_node)
				prev_node = current_node

	@staticmethod
	def _order_chaikin_group(group_set : set[N.Node]) -> list[N.Node]:
		# initialize variables
		group_list : list[N.Node] = list(group_set)
		current_node = group_list.pop(0)
		ordered_group = [current_node]
		# connect the next ones (don't care if we go 'left' or 'right')
		while group_list:
			for remaining_node in group_list:
				if C.Connection.are_connected(current_node, remaining_node):
					ordered_group.append(remaining_node)
					group_list.remove(remaining_node)
					current_node = remaining_node
					break

		return ordered_group
