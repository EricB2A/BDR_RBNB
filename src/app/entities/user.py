from db.entity import Entity
from .location import Location
from db.relationships.one_to_many import OneToMany

class User(Entity):
   _table_name = "users"
   
   fields = {
      "name": "string",
      "password": "string"
   }
   relationships = {
      "locations" : OneToMany("user", "location", "user_id")
   }