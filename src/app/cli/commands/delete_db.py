from .command import Command
from db.entity_manager import EntityManager
from config import Config
import sys
import logging
class DeleteDb(Command):

   def help(self):

      command_executable = "{} {}".format(sys.executable, sys.argv[0])
      usage = "{} delete_db".format(command_executable)
      print("""
      Delete the current database
      Usage: {}

      Exmaple: {}
      """.format(
         command_executable,
         usage,
         usage
      ))

   def run(self, *args):
      em = EntityManager()
      db_name = em.db_name
      if em.is_connected:
         try:
            em.destroy_db() #might fail because db doesn't exist
         except Exception:
            pass
         print("Database {} dropped succesfully".format(db_name))

      else:
         print("Couldn't connect to database, are you sure of your credentials?")
      