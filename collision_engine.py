from properties import Properties

class CollisionEngine:

    def __init__(self, game_objects):
        self.game_objects = game_objects
        self.grid = {}

    def update(self):
        self.grid = {}
        for obj in self.game_objects:
            coordinates = int(obj.x / Properties.OBJECT_SIZE), int(obj.y / Properties.OBJECT_SIZE)

            if coordinates not in self.grid:
                self.grid[coordinates] = [obj]
            else:
                self.grid[coordinates].append(obj)

    def get_near_objects(self, obj, radius=1):
        objects = []
        gridx, gridy = int(obj.x / Properties.OBJECT_SIZE), int(obj.y / Properties.OBJECT_SIZE)
        for vx in range(-radius, radius + 1):
            for vy in range(-radius, radius + 1):
                coordinates = gridx + vx, gridy + vy
                if coordinates in self.grid:
                    for near_obj in self.grid[coordinates]:
                        if near_obj is not obj:
                            objects.append(near_obj)
        #print(len(objects))
        return objects

    def get_colliding_objects(self, obj, radius=1):
        colliding_objects = []
        for o in self.get_near_objects(obj):
            if obj.collided_with(o):
                colliding_objects.append(o)
        return colliding_objects

    def get_objects_near_point(self, point, radius=1):
        objects = []
        gridx, gridy = int(point[0] / Properties.OBJECT_SIZE), int(point[1] / Properties.OBJECT_SIZE)
        for vx in range(-radius, radius + 1):
            for vy in range(-radius, radius + 1):
                coordinates = gridx + vx, gridy + vy
                if coordinates in self.grid:
                    for near_obj in self.grid[coordinates]:
                        objects.append(near_obj)
        #print(len(objects))
        return objects

    def get_objects_colliding_with_point(self, point):
        result = []
        for obj in self.get_objects_near_point(point, radius=1):
            if obj.point_collided(obj, point):
                result.append(obj)
        return result