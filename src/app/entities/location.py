from db.entity import Entity
from db.relationships.one_to_one import OneToOne

class Location(Entity):
   _table_name = "locations"
   fields = {
      "name" : "string",
      "user_id" : "relationship"
   }
   relationships = {
      "user" : OneToOne("location", "user", "id", "user_id")
   }
   def render(self):
      pass
   def render_excerpt(self):
      return "({})Location {}".format(self.key, self.name)