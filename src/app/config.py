import sys
import json


import utils
from pathlib import Path


class Config:
   __metaclass__ = utils.Singleton
   configs = {}
   config_path = None
   
   def __init__(self, config_path = None):
      self.config_path = config_path

   def load(self, path = None):
      if path is None and self.config_path is None:
         raise Exception("No path provided for config")

      for f in utils.get_files_in_path(self._get_path()):
         config_name = Path(f).stem
         with open(f, "r") as fp:
            self.configs[config_name] = json.load(fp)
      
   def _get_path(self):
      return self.config_path

   def save(self):
      pass

   def __getattr__(self,name):
      if name in self.configs:
         return self.configs[name]