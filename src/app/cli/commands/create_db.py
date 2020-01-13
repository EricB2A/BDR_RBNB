from .command import Command
from db.entity_manager import EntityManager
from config import Config
import sys
import logging
class CreateDb(Command):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.entity_manager = EntityManager(Config())
      logging.debug("EM {}".format(self.entity_manager))
   def help(self):
      

      command_executable = "{} {}".format(sys.executable, sys.argv[0])
      usage = "{} create_db".format(command_executable)
      print("""
      Create a new database
      Usage: {}

      Exmaple: {}
      """.format(
         command_executable,
         usage,
         usage
      ))

   def run(self, *args):
      db_name = self.entity_manager.db_name
      if self.entity_manager.is_connected:
         self.entity_manager.create_database()
         print("New database {} created succesfully".format(db_name))

      else:
         print("Couldn't connect to database, are you sure of your credentials?")
      