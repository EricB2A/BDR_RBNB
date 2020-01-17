
from cli.cli_manager import Cli
from config import Config
from db import EntityManager
from utils.path import get_config_path
import logging
from entities import entity_registrar
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)

booted = False

def boot():
   global booted
   logging.debug("Starting app")
   logging.debug("Parsing config")
   
   config = Config()
   entity_manager = EntityManager()
   if not booted:
      config.load(get_config_path())

      
      entity_manager.set_entities(entity_registrar)
      entity_manager.boot()
      entity_manager.boot_relationships()
      booted = True
   return (config, entity_manager)

def run():
   manager = Manager()
   manager.parse_arguments()
   return manager.run()
   
def render(config, db):
   cli = Cli(config, db)
   cli.run()

def run():
   return render(*boot())