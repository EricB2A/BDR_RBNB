from .command import Command
from db.entity_manager import EntityManager
from config import Config
import sys
import logging
class CreateDb(Command):

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
      em = EntityManager()
      db_name = em.db_name
      if em.is_connected:
         em.create_database()
         print("New database {} created succesfully".format(db_name))

      else:
         print("Couldn't connect to database, are you sure of your credentials?")
      