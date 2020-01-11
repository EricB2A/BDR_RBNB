import utils
import mysql.connector
from mysql.connector import errorcode

class EntityManager:
   __metaclass__ = utils.Singleton

   config = None
   entities = {}
   conn = None

   def __init__(self, config):
      self.config = config

   def boot(self):
      self._connect()
      self._build_entity_list()

   def create_database(self):
      DB_NAME = self.config.db.database
      
      cursor = self.conn.cursor()
      try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        cursor.execute("USE {}".format(DB_NAME))
        self.conn.database = DB_NAME
      except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        raise Exception("Failed creating database: {}".format(err))

   def destroy_db(self):
      DB_NAME = self.config.db.database
      
      cursor = self.conn.cursor()
      try:
        cursor.execute("DROP DATABASE {} ".format(DB_NAME))
      except mysql.connector.Error as err:
        print("Failed destroying database: {}".format(err))
        raise Exception("Failed destroying database: {}".format(err))
   
   def reset_db(self):
      try:
         self.destroy_db() #if we can't destroy db that means it doesn't exist
      except mysql.connector.Error as err:
         pass
      self.create_database()

   def _connect(self):
      conn = None
      try:
         conn = mysql.connector.connect(**self.config.db)
         self.conn = conn
      except mysql.connector.Error as err:
         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
         elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
         else:
            print(err)
      
   
   def _build_entity_list(self):
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
      self.db.close()