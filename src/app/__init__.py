
from app.cli.cli_manager import Cli
from config import Config
from db import EntityManager
from utils.path import get_config_path, get_log_path
import logging
from entities import entity_registrar
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG, filename=get_log_path("app.log"))

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

