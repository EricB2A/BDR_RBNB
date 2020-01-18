import utils
import mysql.connector
from mysql.connector import errorcode
from config import Config
import logging


@utils.singleton
class EntityManager:
   #__metaclass__ = utils.Singleton

   config = None
   entities = {}
   conn = None

   @property
   def db(self):
      return self.conn

   @property
   def db_name(self):
      c = Config()
      return c.db["database"] if c is not None else None

   @property
   def is_connected(self):
      if self.conn is None:
         return False
      return self.conn.is_connected()

   def __init__(self, *args, **kwargs):
      super().__init__(*args,**kwargs)
      c = Config()

      self.config = c.db

   def boot(self):
      self._connect()

   def boot_relationships(self):
      if not self.entities:
         raise Exception("No entities registered in entity manager")

      for name, entity in self.entities.items():
         for rname, relationship in entity.relationships.items():
            local_entity = entity
            remote_entity = self.entities[relationship.foreign_entity_name]
            relationship.boot(local_entity, remote_entity)

   def create_database(self):
      DB_NAME = self.db_name
      
      cursor = self.conn.cursor()
      try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        cursor.execute("USE {}".format(DB_NAME))
        self.conn.database = DB_NAME
      except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        raise Exception("Failed creating database: {}".format(err))

   def destroy_db(self):
      DB_NAME = self.db_name
      
      cursor = self.conn.cursor()
      try:
        cursor.execute("DROP DATABASE {} ".format(DB_NAME))
      except mysql.connector.Error as err:
        print("Failed destroying database: {}".format(err))
        raise Exception("Failed destroying database: {}".format(err))
      finally:
         cursor.close()

   def _connect(self):
      config = Config()
      self.config = config
      if not config.db:
         raise Exception("No database configuration")
      conn = None
      # create and open port to mysql server
      try:
         config = {k:v for k,v in config.db.items() if k != "database"}
         logging.debug("Using config for db connexion:  {}".format(config))
         self.conn = mysql.connector.connect(**config)

      except mysql.connector.Error as err:
         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
         
      # try to use the database now and notify user if something went wrong
      try:
         db_name = self.config.db["database"]
         self.conn.database = db_name
      except mysql.connector.Error as err:
         if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")

   def set_entities(self, entity_registrar):
      self.entities = entity_registrar
   
   def get_all_entities(self):
      return self.entities

   def get_db(self):
      return self.conn

   def get_entity(self, entity_name):
      """
      Dynamically get a class for an entity
      """
      if entity_name in self.entities.keys():
         return self.entities[entity_name]
      else:
         return False

   def __del__(self):
      if self.conn is not None and self.conn.is_connected():
         self.conn.close()