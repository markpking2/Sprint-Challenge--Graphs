from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph():
    def __init__(self, player):
        self.player = player

    def dft(self):
        reverse_dirs = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
        exits = self.player.current_room.get_exits()
        traveled = Stack()
        rooms = {}
        rooms[self.player.current_room.id] = {}
        path = []
        for dir in exits:
            rooms[self.player.current_room.id][dir] = '?'

        while True:    
            not_visited = [d for d in rooms[self.player.current_room.id] if rooms[self.player.current_room.id][d] == '?']
            if len(not_visited):
                next_dir = not_visited.pop()
                traveled.push(reverse_dirs[next_dir])
                rooms[self.player.current_room.id][next_dir] = True
                self.player.travel(next_dir)
                path.append(next_dir)
                if self.player.current_room.id not in rooms:
                    rooms[self.player.current_room.id] = {}
                    exits = self.player.current_room.get_exits()
                    for dir in exits:
                        rooms[self.player.current_room.id][dir] = '?'
                    rooms[self.player.current_room.id][reverse_dirs[next_dir]] = True
            else:
                if traveled.size():
                    dir = traveled.pop()
                    self.player.travel(dir)
                    path.append(dir)
                else:
                    return path
                
player = Player(world.starting_room)
graph = Graph(player)
traversal_path = graph.dft()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
