
from cli.cli_manager import Cli
from config import Config
from db import EntityManager
from utils.path import get_config_path

def boot():
   pass

def run():
   manager = Manager()
   manager.parse_arguments()
   return manager.run()
   
def render(config, db):
   cli = Cli(config, db)
   cli.run()

def run():
   config = Config(get_config_path())
   config.load()

   entity_manager = EntityManager(config.db)
   entity_manager.boot()
   return render(config, entity_manager)