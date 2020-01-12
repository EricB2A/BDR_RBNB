from db.entity import Entity

class Location(Entity):
   def render(self):
      pass
   def render_excerpt(self)
      return "({})Location {}".format(self.key, self.name)