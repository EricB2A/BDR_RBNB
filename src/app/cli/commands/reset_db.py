from .command import Command
from .create_db import CreateDb
from .delete_db import DeleteDb
from db.entity_manager import EntityManager
from config import Config
import sys
import logging
import utils.path
class ResetDb(Command):
   schema_file = utils.path.get_config_path("db.sql")

   def help(self):
      

      command_executable = "{} {}".format(sys.executable, sys.argv[0])
      usage = "{} reset_db".format(command_executable)
      print("""
      Reset the database.
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
         cmd = DeleteDb()
         cmd.run(*args)

         cmd = CreateDb()
         cmd.run(*args)

         self.import_schema()
         print("Database {} reseted succesfully".format(db_name))

      else:
         print("Couldn't connect to database, are you sure of your credentials?")
   def import_schema(self):
      em = EntityManager()
      with open(self.schema_file, "r") as f:
         db = em.db
         sql = f.read()
         cursor = db.cursor()
         for result in cursor.execute(sql, multi=True):
            if result.with_rows:
               logging.debug("Rows added by {}".format(result.statement))
               logging.debug(reuslt.fetchall())
            else:
               logging.debug("Rows affected {} by {}".format(result.rowcount,result.statement))
         db.commit()
