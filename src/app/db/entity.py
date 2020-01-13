from utils import sanitize
from abc import abstractmethod
from db.entity_manager import EntityManager
import logging

class Entity:
   """
   Meta class for all entities
   """
   _dirty = {}
   _data = {}

   _table_name = None
   _key_name = None
   fields = {}
   relationships = {}
   manager = None
   db = None
   @property
   def class_name(self):
      return self.__class__.__name__.lower()

   @property
   def table_name(self):
      return self._table_name if self._table_name is not None else self.class_name

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

      # build relationship mapping
      # fill the entity with all the fields
      self._fill(**fields)
      em = EntityManager()
      self.manager = em
      logging.debug("Instantiating new %s, EM: %s", self.__class__, em)

      self.db = em.conn
      
   @classmethod
   def build(cls, **fields):
      new_entity = cls() 
      new_entity._fill(**fields)
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
      self._sanitize_fields() # build up all the fields -> sanitize them and everything
      self._build_relationships() #build up all relationships
      return self._persist() #persist in db

   def _sanitize_fields(self):
      for k, v in self._dirty.items():
         self._data[k] = sanitize(v)
   def _build_relationships(self):
      for r in self.relationships: #tell each relationship that we're now saving the local entity
         #each relationship will now fill the local entity if needed before saving
         r.save(self)

   def _persist(self):
      #if not self.db:
      #   raise Exception("Not connected to database") #TODO there seems to be a bug where the db field isn't populated at all when creating an entity

      if self.exists:
         pass # TODO
      else:
         self._insert_into_db(self._data)

   def _insert_into_db(self, data):
      em = EntityManager()
      db = em.get_db()

      data_keys = data.keys()
      n_values = len(data_keys) * "%s, "
      values = data.values()
      value_string = n_values[:-2]
      sql = "INSERT INTO `{}`({}) VALUES({})".format(self.table_name, ", ".join(map(lambda s: "`"+s+"`", data_keys)), value_string)
      cursor = db.cursor()
      logging.debug("EXECUTING SQL: %s with values : %s",sql, values)
      cursor.execute(sql, data)
      db.commit()
      if cursor.rowcount > 0:
         # set the id, now the class exists!
         setattr(self, self.key_name, cursor.lastrowid)
         return self
      else:
         raise Exception("Unable to insert in db")

   def _clean(self, statement):
      pass

   def __setattr__(self, name, val):
      if name in self.fields.keys():
         self._dirty[name] = val
      elif name in self.relationships.keys():
         self._relationships[name] = self.relationships[name].build(val)

   def __getattr__(self, name):
      if len(self.fields.keys()) > 0 and name in self.fields.keys():
         return self._dirty[name]
      elif len(self.relationships.keys()) > 0 and name in self.relationships.keys():
         self._relationships[name]
      