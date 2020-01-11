import os

def get_app_path(extra = ''):
   return os.path.join(get_base_path(), "app", extra)

def get_config_path(extra = ''):
   return os.path.join (get_base_path(), "config", extra)

def get_base_path():
   return os.getcwd()