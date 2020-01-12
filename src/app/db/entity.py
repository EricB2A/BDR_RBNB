class Entity:
   """
   Meta class for all entities
   """
   _dirty = {}
   _data = {}

   table_name = ""
   fields = {}

   relationships = {
      "user": OneToOne("users", "id", "user_id"),
      
   }

   def __init__(self, **fields):
      # set table name based on class
      self.table_name = self.table_name if len(self.table_name) > 0 else self.__name__.lower()
      # build relationship mapping
      # fill the entity with all the fields
      self._fill(fields)
      pass
   @classmethod
   def build(cls, **fields):
      new_entity = cls() 
      new_entity._fill(fields)
      return new_entity

   def _fill(self, **fields):
      self._dirty = filter(lambda f : f in self.fields.keys(), fields)
      self._relationships = filter(lambda f : f in self.relationships.keys(), fields)

   def findOne(self, criteria):
      pass
   def find(self, criteria):
      pass
   def create(self):
      pass
   def update(self):
      pass
   def delete(self):
      pass

   @abstractmethod
   def render(self):
      pass

   def _save(self, fields, action):
      pass
   def _clean(self, statement):
      pass
   def __setattr__(self, name, val):
      if name in self.fields.keys():
         self._dirty[name] = val
      elif name in self.relationships.keys():
         self._relationships[name] = self.relationships[name].build(val)
   