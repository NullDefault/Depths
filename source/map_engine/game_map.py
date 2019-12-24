from source.map_engine.tile import Tile
from source.map_engine.rect import Rect
from random import randint


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def generate_map(self, max_rooms, min_room_size, max_room_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = randint(min_room_size, max_room_size)
            h = randint(min_room_size, max_room_size)

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.generate_room(new_room)

                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        self.create_tunnel_h(prev_x, new_x, prev_y)
                        self.create_tunnel_v(prev_y, new_y, new_x)
                    else:
                        self.create_tunnel_v(prev_y, new_y, prev_x)
                        self.create_tunnel_h(prev_x, new_x, new_y)

                rooms.append(new_room)
                num_rooms += 1


    def generate_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.create_opening(x, y)

    def create_tunnel_h(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.create_opening(x, y)

    def create_tunnel_v(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.create_opening(x, y)

    def create_opening(self, x, y):
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False