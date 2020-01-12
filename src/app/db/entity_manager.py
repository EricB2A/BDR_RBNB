import utils
import mysql.connector
from mysql.connector import errorcode
from config import Config
import logging
@utils.singleton
class EntityManager:
   #__metaclass__ = utils.Singleton

   config = None
   entities = []
   conn = None
   db = None

   @property
   def db_name(self):
      return self.config["database"] if self.config is not None else None

   @property
   def is_connected(self):
      if self.conn is None:
         return False
      return self.conn.is_connected()

   def __init__(self):
      c = Config()
      self.config = c.db

   def boot(self):
      self._connect()
      self._build_entity_list()

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

   def reset_db(self):
      try:
         self.destroy_db() #if we can't destroy db that means it doesn't exist
      except mysql.connector.Error as err:
         pass
      self.create_database()

   def _connect(self):
      conn = None
      # create and open port to mysql server
      try:
         config = {k:v for k,v in self.config.items() if k != "database"}
         logging.debug("Using config for db connexion:  {}".format(config))
         self.conn = mysql.connector.connect(**config)

      except mysql.connector.Error as err:
         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
         
      # try to use the database now and notify user if something went wrong
      try:
         db_name = self.db_name
         self.conn.database = db_name
      except mysql.connector.Error as err:
         if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")

   def _build_entity_list(self):
      pass

   def get_all_entities(self):
      pass

   def get_db():
      return this.conn

   @staticmethod
   def get_entity(entity_name):
      """
      Dynamically get a class for an entity
      """
      pass

   def __del__(self):
      if self.conn is not None and self.conn.is_connected():
         self.conn.close()