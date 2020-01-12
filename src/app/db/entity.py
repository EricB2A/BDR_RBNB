from utils import sanitize
from abc import abstractmethod

class Entity:
   """
   Meta class for all entities
   """
   _dirty = {}
   _data = {}

   _table_name = None
   _key_name = None
   fields = {}
   
   @property
   def name(self):
      return self.__name__.lower()

   @property
   def table_name(self):
      return self._table_name if self._table_name is not None else self.name

   @property
   def key(self):
      return self._data[self.key_name]

   @property
   def key_name(self):
      return self._key_name if self._key_name is not None else "id"

   @property
   def exists(self):
      return hasattr(self._data,self.key_name)

   

   def __init__(self, **fields):
      # set table name based on class
      self.table_name = self.table_name if len(self.table_name) > 0 else self.name
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
   
   def render_excerpt(self):
      """
      A smaller string than the full entity string. Can be used when seleting stuff
      """
      return "({}) {}".format(self.key, self.name)
   
   def save(self):
      self._save_fields() # build up all the fields -> sanitize them and everything
      self._save_relationships() #build up all relationships
      return self._persist() #persist in db

   def _save_fields(self):
      for k, v in self._dirty:
         self._data[k] = sanitize(v)
   def _save_relationships(self):
      for r in self.relationships: #tell each relationship that we're now saving the local entity
         #each relationship will now fill the local entity if needed before saving
         r.save(self)

   def _persist(self):
      if self.exists:
         pass # TODO
      else:
         self._insert_into_db(self._data)

   def _insert_into_db(self, data):
      data_keys = data.keys()
      n_values = len(data_keys) * ("%s")
      values = data.values()
      value_string = ", ".join(n_values)
      sql = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, value_string, value_string)
      res = self.db.cursor.execute(sql, values)
      return res
   def _clean(self, statement):
      pass

   def __setattr__(self, name, val):
      if name in self.fields.keys():
         self._dirty[name] = val
      elif name in self.relationships.keys():
         self._relationships[name] = self.relationships[name].build(val)
      else:
         setattr(self, name, val)

   def __getattribute__(self, name):
      if name in self.fields.keys():
         return self._dirty[name]
      elif name in self.relationships.keys():
         self._relationships[name]
      else:
         return getattr(self, name)