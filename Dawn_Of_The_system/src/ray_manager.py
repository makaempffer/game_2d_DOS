from ray import * 


class RayManager:
    def __init__(self, game, origin, walls, renderer):
        self.game = game
        self.objects = walls
        self.renderer = renderer
        self.origin = origin
        self.rays = []
        self.set_rays()
    
    def set_rays(self):
        """Create ray array and set angles to ++DELTA_ANGLE"""
        angle = DELTA_ANGLE
        for i in range(NUM_RAYS):
            self.rays.append(Ray(self.game, angle, self.origin, i))
            angle += DELTA_ANGLE

    def update(self):
        self.cast_rays()
    
    def cast_rays(self):
        columns = []
        objects = []
        angles = []
        for ray in self.rays:
            ray.update()
            closest_object = None
            record = 100000
            
            for object in self.objects.object_list:
                point = ray.cast(object)
                
                if point:
                    point_x, point_y = point
                    distance_from_object =  math.sqrt((point_x - ray.pos.x)**2 + (point_y - ray.pos.y)**2)
                   
                    if distance_from_object < record:
                        record = distance_from_object
                        closest_object = point
            #only setting the objects if render distance is met
            if closest_object and record < RENDER_DISTANCE - 1:
                #pg.draw.line(self.game.screen, 'blue', ray.pos, (closest_object))
                objects.append(closest_object)
                columns.append(ray.column)

        self.renderer.objects = objects
        self.renderer.columns = columns