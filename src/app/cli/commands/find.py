from .command import Command
from db.entity_manager import EntityManager
from db.relationships.many_to_many import ManyToMany
from db.relationships.one_to_many import OneToMany
import sys
import logging
import inquirer
import termtables as tt

class Find(Command):
   

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.entity_manager = EntityManager()
      
   def help(self):
      
      entities_available = ""
      em = EntityManager()
      for name in em.get_all_entities():
         entities_available += "\t - " + name + "\n"

      command_executable = "{} {}".format(sys.executable, sys.argv[0])
      usage = "{} find [entity name]".format(command_executable)
      print("""
find a new entity (location, user, etc...)
You will be prompted to complete the necessary fields, once you selected an entity
Usage: {}
Available entities: 
{}

Exmaple usage: 
      """.format(
         usage,
         entities_available
      ))

   def run(self, *args):
      if len(args) < 1:
         return self.help()
      entity_name = args[0]
      entity = self.entity_manager.get_entity(entity_name)
      if not entity:
         print("Couldn't find the class you are looking for")
         return self.help()
      
      ids = args[1:]
      res = None
      if len(ids) > 0:
         res = entity.find(ids)
      else:
         res = entity.find()
      #data = list(map(lambda e: list(map(lambda n: getattr(e,n),e.fields.keys())), res))
      data = []
      logging.debug("GOT MODELS: %s",list(res))
      for e in res:
         data.append(
            [ getattr(e,k) for k in e.fields.keys() ]
         )
      logging.debug(data)
      logging.debug(list(entity.fields.keys()))
      string = tt.to_string(
         data,
         header=list(entity.fields.keys()),
         style=tt.styles.ascii_thin_double,
      )
      print(string)
      

      