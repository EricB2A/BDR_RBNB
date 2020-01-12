import sys
import json
import logging
import utils
from pathlib import Path

@utils.singleton
class Config:
   #__metaclass__ = utils.Singleton
   configs = {}
   config_path = None
   
   def __init__(self):
      pass

   def load(self, path):
      
      for f in utils.get_files_in_path(path):
         config_name = Path(f).stem
         logging.debug("Loading {}".format(f))
         with open(f, "r") as fp:
            self.configs[config_name] = json.load(fp)
      
      logging.debug("Loaded config: ", self.configs)

   def _get_path(self):
      return self.config_path

   def save(self):
      pass

   def __getattr__(self,name):
      if name in self.configs:
         return self.configs[name]