from .command import Command
from db.entity_manager import EntityManager
from db.relationships.many_to_many import ManyToMany
from db.relationships.one_to_many import OneToMany
import sys

class Create(Command):
   def __init__(self, *args, **kwargs):
      super(*args, **kwargs)
      self.entity_manager = EntityManager()
      
   def help(self):
      
      entities_available = ""
      for e in EntityManager.get_all_entities():
         entities_available += ("\t - {}". e.__name__) + "\n"

      command_executable = "{} {} create".format(sys.executable, sys.argv[0])
      usage = "{} [entity name]".format(command_executable)
      print("""
      Create a new entity (location, user, etc...)
      You will be prompted to complete the necessary fields, once you selected an entity
      Usage: {}
      Available entities: 
      {}

      Exmaple usage: {} {}
      """.format(
         command_executable,
         usage,
         entities_available
      ))

   def run(self, *args):
      entity_name = kwargs[0]
      entity = self.entity_manager.get_entity(entity_name)
      for field in entity.fields:
         setattr(entity, field, ask())
      for relationship in entity.relationships:
         if isinstance(relationship, ManyToMany):
            pass
            # Do something for many to many
         elif isinstance(relationship,  OneToMany):
            setattr(entity, relationship.name, ask(relationship.get_all_foreign_entities()))

      entity.save()
      print("New {} created succesfully".format(entity_name))
      