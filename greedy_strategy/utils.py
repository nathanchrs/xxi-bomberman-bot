import Queue
from entities.moves import Moves

def map_in_range(map, location):
	x, y = location
	return (x >= 0) and (x < len(map[0])) and (y >= 0) and (y < len(map))

# Check whether a location on the map is equal to any of the characters in chars list.
# If the location is out of range, return False.
def map_equals(map, location, chars):
	equals = False
	x, y = location
	if map_in_range(map, location):
		for char in chars:
			if map[y][x] == char:
				equals = True
				break
	return equals

# Returns a (x, y) location tuple, shifted by offset in the specified direction from the original location.
# Valid directions are 'up', 'left', 'right', and 'down'.
def shift(location, direction, offset=1):
	x, y = location
	if direction == 'up':
		return (x, y-offset)
	elif direction == 'left':
		return (x-offset, y)
	elif direction == 'right':
		return (x+offset, y)
	elif direction == 'down':
		return (x, y+offset)
	else:
		raise Exception('Invalid direction')

# Returns the opposite of the direction given
def opposite(direction):
	if direction == 'up':
		return 'down'
	elif direction == 'left':
		return 'right'
	elif direction == 'right':
		return 'left'
	elif direction == 'down':
		return 'up'
	else:
		raise Exception('Invalid direction')

# Debug helper function
def print_map(map):
	for i in range(0, len(map)):
		row = ''
		for j in range(0, len(map[0])):
			row = row + map[i][j]
		print row

# Backtrack helper function for shortest_path; returns sequence of moves from path start to path end.
def shortest_path_backtrack(map, distances, end_location, costs):
	bt_location = end_location
	bt_x, bt_y = bt_location
	bt_length = distances[bt_y][bt_x]
	bt_path = []
	while bt_length > 0:
		for direction in ['up', 'left', 'right', 'down']:
			bt_next_location = shift(bt_location, direction)
			bt_next_x, bt_next_y = bt_next_location
			if map_in_range(distances, bt_next_location) \
			and costs[map[bt_y][bt_x]] > 0 \
			and (distances[bt_next_y][bt_next_x] + costs[map[bt_y][bt_x]] == distances[bt_y][bt_x]):
				bt_location = bt_next_location
				bt_x, bt_y = bt_location
				bt_length = distances[bt_next_y][bt_next_x]
				if direction == 'up':
					bt_path.append(Moves.MOVE_DOWN)
				elif direction == 'left':
					bt_path.append(Moves.MOVE_RIGHT)
				elif direction == 'right':
					bt_path.append(Moves.MOVE_LEFT)
				elif direction == 'down':
					bt_path.append(Moves.MOVE_UP)
				else:
					raise Exception('Invalid direction')
				break
	bt_path.reverse()
	print "Shortest path move sequence:", bt_path # DEBUG
	return bt_path

# Dijkstra's shortest path algorithm; returns sequence of moves from start location to nearest end character.
def shortest_path(map, start, end_chars, costs):
	POS_INF = 99999999
	distances = [[POS_INF for j in range(0, len(map[0]))] for i in range(0, len(map))]
	start_x, start_y = start
	distances[start_y][start_x] = 0
	pq = Queue.PriorityQueue()
	pq.put((0, start))
	print "Finding shortest path from:", start # DEBUG

	while not pq.empty():
		path_length, current_location = pq.get()

		if map_equals(map, current_location, end_chars):
			print "Found shortest path to", current_location, ", path length", path_length # DEBUG
			return shortest_path_backtrack(map, distances, current_location, costs)			

		for direction in ['up', 'left', 'right', 'down']:
			next_location = shift(current_location, direction)
			next_x, next_y = next_location
			if map_in_range(map, next_location) and (costs[map[next_y][next_x]] >= 0):
				print "Finding shortest path: now at", current_location, ", going", direction, "to", next_location # DEBUG
				if (path_length + costs[map[next_y][next_x]]) < distances[next_y][next_x]:
					distances[next_y][next_x] = path_length + costs[map[next_y][next_x]]
					pq.put((distances[next_y][next_x], next_location))

	return None