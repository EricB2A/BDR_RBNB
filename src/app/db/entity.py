from utils import sanitize, compose
from abc import abstractmethod
from db.entity_manager import EntityManager
import logging
from mysql.connector.conversion import MySQLConverter
from config import Config
from decimal import Decimal
from mysql.connector.custom_types import HexLiteral

NUMERIC_TYPES = (int, float, Decimal, HexLiteral)

class Entity(object):
   """
   Meta class for all entities
   """
   _dirty = {} #data before being processed
   _data = {} #data that is retrieved from db and secure hehe

   _table_name = None
   _key_name = None
   fields = {}
   relationships = {}
   manager = None

   @property
   def db(self):
      """
      Turns out singletons can't get accessed on init of a class
      So simple hack, creating a property that accesses the singleton
      and getting the wanted property
      """
      em = EntityManager()
      db = em.get_db()
      return db

   @property
   def class_name(self):
      return self.__class__.__name__.lower()

   @property
   def table_name(self):
      return self._table_name if self._table_name is not None else self.class_name

   @property
   def key(self):
      return self._data[self.key_name] if self.key_name in self._data else None

   @property
   def key_name(self):
      return self._key_name if self._key_name is not None else "id"

   @property
   def exists(self):
      return hasattr(self._data,self.key_name)

   def __init__(self, **fields):
      self._fill(**fields)
      
   @classmethod
   def build(cls, **fields):
      new_entity = cls() 
      new_entity._fill(**fields)
      return new_entity

   def _fill(self, **fields):
      self._dirty = {key:value for (key,value) in fields.items() if key in self.fields.keys()}
      self._relationships = {key:value for (key,value) in fields.items() if key in self.relationships.keys()}

   def fresh(self):
      if not self.exists:
         return self(**self._dirty)
      else:
         self._find_in_db(self.key)

   @classmethod
   def find(cls, id = None):
      instance = cls()
      return instance._find_in_db(id)  

   def create(self, **data):
      return self.save(data)

   def update(self, **data):
      return self.save(data)

   def delete(self):
      if not self.exists:
         return False

      return self._delete_from_db()

   
   def render(self):
      return self.render_excerpt()
   
   def render_excerpt(self):
      """
      A smaller string than the full entity string. Can be used when seleting stuff
      """
      return "({}) {}".format(self.key, self.name)
   
   def save(self, **data):
      self._fill(**data)
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
      if self.exists:
         self._update_db(self._data)
      else:
         self._insert_into_db(self._data)

   def _delete_in_db(self):
      sql = "DELETE from {} WHERE `{}` = {}".format(self.table_name, self.key_name, self.key)
      db = self.db
      cursor = db.cursor()
      logging.debug("QUERY: %s", sql)
      cursor.execute(sql)
      db.commit()
      if cursor.rowcount > 0:
         return True

      return False

   def _find_in_db(self, id = None):
      def quote(v):
         return "`"+v+"`"

      fields = list(self.fields.keys())

      if self.key_name not in fields:
         fields.append(self.key_name)

      fields = map(quote, fields)

      query = "SELECT {} from {} ".format(", ".join(fields),self.table_name) #TODO don't select *......
      db = self.db
      cursor = db.cursor(dictionary=True)

      if isinstance(id, list):
         query += "WHERE {} in ({})".format(self.key, ", ".join(id))
         logging.debug("QUERY: %s", query)
         cursor.execute(query)
         result = cursor.fetchall()
         logging.debug("FOUND: %s", result)
         return map(lambda x: self.build(**x), result)
      elif id is None: # no id no problem
         cursor.execute(query)
         result = cursor.fetchall()
         logging.debug("FOUND: %s", result)
         return list(map(lambda x: self.build(**x), result))
      else: # find single instance with the specified id
         query += "WHERE {} = {}".format(self.key_name, id)
         logging.debug("QUERY: %s", query)
         cursor.execute(query)
         result = cursor.fetchone()
         logging.debug("FOUND: %s", result)
         return self.build(**result)

   def _update_db(self, data):
      if self.key is None:
         raise Exception("Unable to update entity that doesn't exist")
      db = self.db
      # create placeholders for the data
      columns, values = self._get_sql_data(data)

      update_statement = ""
      for i in columns:
         update_statement += "SET "+columns[i]+" = " +values[i]

      sql = "UPDATE `{}` {} WHERE {}={};".format(self.table_name, update_statement, self.key_name, self.key)
      logging.debug("Using db: %s", db.database)
      cursor = db.cursor()
      logging.debug("EXECUTING SQL: %s",sql)
      cursor.execute(sql, data)
      db.commit()
      if cursor.rowcount > 0:
         # set the id, now the class exists!
         # setattr(self, self.key_name, cursor.lastrowid)
         return self
      else:
         raise Exception("Unable to update in db")

   def _insert_into_db(self, data):
      em = EntityManager()
      db = em.get_db()
      # create placeholders for the data
      columns, values = self._get_sql_data(data)

      sql = "INSERT INTO `{}`({}) VALUES({});".format(self.table_name, columns, values)
      logging.debug("Using db: %s", db.database)
      cursor = db.cursor()
      logging.debug("EXECUTING SQL: %s",sql)
      cursor.execute(sql, data)
      db.commit()
      if cursor.rowcount > 0:
         # set the id, now the class exists!
         setattr(self, self.key_name, cursor.lastrowid)
         return self
      else:
         raise Exception("Unable to insert in db")

   def _get_sql_data(self, data):
      """
      returns tuple with (columns, values)
      """
      em = EntityManager()
      db = em.get_db()
      config = Config()
      charset = config.db.charset if "charset" in config.db.keys() else "utf8"
      converter = MySQLConverter(charset)
      def none_to_null(val):
         if val is None:
            return "NULL"
         return val
      def quote(val):
         if isinstance(val, NUMERIC_TYPES):
            return val
         return "'"+val+"'"
      _escape_value = compose(none_to_null, quote , converter.escape)
      _escape_column = compose(none_to_null,lambda x: "`"+x+"`", converter.escape)
      # create placeholders for the data
      column_string = ""
      value_string = ""

      for k,v in data.items():
         value_string +=  _escape_value(v) +  ", "
         column_string += _escape_column(k) + ", "

      value_string = value_string[:-2] #remove trailing comma
      column_string = column_string[:-2] #remove trailing comma

      return (column_string, value_string)

   def __setattr__(self, name, val):
      if name in self.relationships.keys():
         self.relationships[name].build(val)
      elif name in self.fields.keys():
         self._dirty[name] = val
      else:
         super(Entity, self).__setattr__(name, val)

   def __getattr__(self, name):
      if len(self.fields.keys()) > 0 and name in self.fields.keys():
         if name in self._dirty.keys():
            return self._dirty[name]
         elif name in self._data.keys():
            return self._data[keys]
         else:
            return None
      elif len(self.relationships.keys()) > 0 and name in self.relationships.keys():
         self._relationships[name]
   
   def __str__(self):
      return self.render_excerpt()

class HeritableEntity(Entity):
   parent_entity = ""
   @property
   def parent_id_name(self):
      return self.parent_entity + "_id"
   @property
   def parent_id(self):
      return getattr(self, self.parent_id_name)
      
   @property
   def parent_entity(self):
      em = EntityManager()
      parent = em.get_entity(self.parent_entity)
      return parent

   @property
   def parent(self):
      p = self.parent_entity()
      return p._find(self.parent_id)

   def find(self, id = None):
      #get all local entities by id
      entities = super()._find(id)
      #then get all their parents
      return map(lambda x: x.parent(), entities) # TODO should work

   def update(self, data):
      pass #TODO same as find

   def save(self, **data):
      parent = self.parent()
      parent.save(**data)
      setattr(self, self.parent_id, parent.key)
      data_to_save = {
         self.parent_id: self.personne_id
      }
      if self.exists:
         self._update_db(data_to_save)
      else:
         self._insert_to_db(data_to_save)
   