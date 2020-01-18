from utils import sanitize, compose, iterable
from abc import abstractmethod
from db.entity_manager import EntityManager
import logging
from mysql.connector.conversion import MySQLConverter
from config import Config
from decimal import Decimal
from mysql.connector.custom_types import HexLiteral
from collections.abc import Iterable

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
   _key = None
   was_recently_created = False
   @property
   def id(self):
      return self.key
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
      return self._key

   @property
   def key_name(self):
      return self._key_name if self._key_name is not None else "id"

   @property
   def exists(self):
      return self._key is not None
      

   def __init__(self, *args, **fields):
      super(Entity, self).__init__()
      self._data = {}
      self._dirty = {}
      self._key = None
      self.was_recently_created = False
      self._fill(**fields)

   @classmethod
   def build(cls, **fields):
      new_entity = cls() 
      new_entity._fill(**fields)
      return new_entity

   @classmethod
   def where(cls, criteria):
      new_entity = cls() 
      return new_entity._search_in_db(criteria)

   @classmethod
   def find(cls, id = None):
      instance = cls()
      return instance._find_in_db(id)  

   @classmethod
   def create(cls, **data):
      instance = cls()
      instance._fill(**data)

      instance.save()
      return instance

   def _fill(self, **data):
      if self.key_name in data.keys():
         self._key = data[self.key_name]

      self._dirty = {key:value for (key,value) in data.items() if key in self.fields.keys()}
      self._relationships = {key:value for (key,value) in data.items() if key in self.relationships.keys()}

   def fresh(self):
      if not self.exists:
         return self(**self._dirty)
      else:
         self._find_in_db(self.key)
   
   def update(self, **data):
      self._fill(**data)
      return self.save()

   def delete(self):
      if not self.exists:
         return True

      return self._delete_in_db()

   
   def render(self):
      return self.render_excerpt()
   
   def render_excerpt(self):
      """
      A smaller string than the full entity string. Can be used when seleting stuff
      """
      return "({}) {}".format(self.key, self.name)
   
   def save(self, **data):
      #self._fill(**data)
      self._sanitize_fields() # build up all the fields -> sanitize them and everything
      
      if self._persist(): #persist in db
         self.was_recently_created = True
         self._build_relationships() #build up all relationships
         
         return True

      return False

   def _sanitize_fields(self):
      for k, v in self._dirty.items():
         self._data[k] = sanitize(v)

   def _build_relationships(self):
      for k,r in self.relationships.items(): #tell each relationship that we're now saving the local entity
         #each relationship will now fill the local entity if needed before saving
         r.save(self)

   def _persist(self):
      if self.exists:
         data = { k:v for (k,v) in self._data.items() if k is not self.key_name} # TODO define if app needs to do this
         return self._update_db(data)
      else:
         return self._insert_into_db(self._data)
      return False

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
         fields.insert(0,self.key_name)

      fields = map(quote, fields)

      query = "SELECT {} from {} ".format(", ".join(fields),self.table_name) #TODO don't select *......
      db = self.db
      cursor = db.cursor(dictionary=True)
      
      if iterable(id):
         ids = list(filter(lambda x: bool(x), id))
         logging.debug("SEARCHING for ids: %s", ids)
         query += "WHERE {} in ({})".format(self.key_name, ", ".join(ids))
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
         if cursor.rowcount <= 0:
            return None
         return self.build(**result)

   def _search_in_db(self, criteria):
      def quote(v):
         return "`"+v+"`"

      fields = list(self.fields.keys())

      if self.key_name not in fields:
         fields.insert(0,self.key_name)

      fields = map(quote, fields)

      query = "SELECT {} from {} ".format(", ".join(fields),self.table_name) #TODO don't select *......
      query += "WHERE {}".format(criteria)
      db = self.db
      cursor = db.cursor(dictionary=True)
      logging.debug("SEARCHING for critera: %s", criteria)
      logging.debug("QUERY: %s", query)
      cursor.execute(query)
      result = cursor.fetchall()
      logging.debug("FOUND: %s", result)
      return map(lambda x: self.build(**x), result)
      

   def _update_db(self, data):
      if self.key is None:
         raise Exception("Unable to update entity that doesn't exist")
      db = self.db
      # create placeholders for the data
      columns, values = self._get_sql_data(data)
      
      update_statement = "SET"
      for c,v in zip(columns, values):
         update_statement += " "+ c +" = " + v+ ", "
      
      update_statement = update_statement[:-2] #remove trailing comma

      sql = "UPDATE `{}` {} WHERE {}={};".format(self.table_name, update_statement, self.key_name, self.key)
      logging.debug("Using db: %s", db.database)
      cursor = db.cursor()
      logging.debug("EXECUTING SQL: %s",sql)
      logging.debug("DATA FROM MODEL: %s", data)
      cursor.execute(sql, data)
      db.commit()
      if cursor.rowcount >= 0:
         # set the id, now the class exists!
         return True
      else:
         raise Exception("Unable to update in db")

   def _insert_into_db(self, data):
      em = EntityManager()
      db = em.get_db()
      # create placeholders for the data
      columns, values = self._get_sql_data(data)

      assert len(columns) == len(values)

      column_string = ""
      value_string = ""

      for c, v in zip(columns, values):
         value_string +=  v +  ", "
         column_string += c + ", "

      value_string = value_string[:-2] #remove trailing comma
      column_string = column_string[:-2] #remove trailing comma

      sql = "INSERT INTO `{}`({}) VALUES({});".format(self.table_name, column_string, value_string)
      logging.debug("Using db: %s", db.database)
      cursor = db.cursor()
      logging.debug("EXECUTING SQL: %s",sql)
      logging.debug("DATA FROM MODEL: %s", data)
      cursor.execute(sql, data)
      db.commit()
      if cursor.rowcount > 0:
         # set the id, now the class exists!
         self._key = cursor.lastrowid
         return True
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
            return str(val)
         return "'"+val+"'"

      def quote_col(val):
         return "`"+val+"`"

      _escape_value = compose(none_to_null, quote , converter.escape)
      _escape_column = compose(none_to_null, quote_col, converter.escape) #column quting is different than normal quotes
      
      if self.key_name not in data.keys() and self.key is not None: #add the key to the data
         data[self.key_name] = self.key
      
      columns = list()
      values = list()

      for k,v in data.items():
         values.append(_escape_value(v))
         columns.append(_escape_column(k))

      return (columns, values)

   def __setattr__(self, name, val):
      if name in self.relationships.keys():
         self.relationships[name].build(val)
      elif name in self.fields.keys():
         self._dirty[name] = val
      else:
         super(Entity, self).__setattr__(name, val)

   def __getattr__(self, name):
      if name in self._dirty.keys():
         return self._dirty[name]
      elif name in self._data.keys():
         return self._data[keys]
      elif name in self.relationships.keys():
         self._relationships[name].find(self)
      else:
         return None

   def __str__(self):
      return self.render_excerpt()


class ReadonlyEntity(Entity):
   @classmethod
   def find(cls, id = None):
      instance = cls()
      return instance._find_in_db(id)  

   @classmethod
   def create(cls, **data):
      raise Exception("Cannot create read only entity {}".format(self.name))
      return True

   def update(self, **data):
      self._fill(**data)
      return self.save()

   def delete(self):
      return True
   
   def save(self, **data):
      return True

#Doran told me to do this, frick that dude
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
   