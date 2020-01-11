class Entity:
   """
   Meta class for all entities
   """
   _dirty = {}
   table_name = ""
   def __init__(self):
      # set table name based on class
      pass
   
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
   def _save(self, fields, action):
      pass
   def _clean(self, statement):
      pass
   def __setattr__(self, name, val):
      if name in self.fields:
         self._dirty[name] = val
      
   