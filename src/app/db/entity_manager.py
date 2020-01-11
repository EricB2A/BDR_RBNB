import utils

class EntityManager:
   __metaclass__ = utils.Singleton

   config = None
   entities = {
      
   }
   def __init__(self, config):
      self.config = config

   def boot(self):
      self._connect()
      self._get_entities()
   def _connect(self):
      pass
   def _get_entities(self):
      pass
   @staticmethod
   def get_entity(entity_name):
      """
      Dynamically get a class for an entity
      """
      pass