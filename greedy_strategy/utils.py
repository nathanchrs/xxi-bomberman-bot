# Check whether a location on the map is equal to any of the characters in chars list.
# If the location is out of range, return False.
def map_equals(map, location, chars):
	equals = False
	x, y = location
	if (x >= 0) and (x < len(map[0])) and (y >= 0) and (y < len(map)):
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

# Debug helper function
def print_map(map):
	for i in range(0, len(map)):
		row = ''
		for j in range(0, len(map[0])):
			row = row + map[i][j]
		print row
