from .command import Command
from db.entity_manager import EntityManager
from db.relationships.many_to_many import ManyToMany
from db.relationships.one_to_many import OneToMany
from db.relationships.one_to_one import OneToOne

import sys
import logging
import inquirer

class Create(Command):
   

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.entity_manager = EntityManager()
      
   def help(self):
      
      entities_available = ""
      em = EntityManager()
      for name in em.get_all_entities():
         entities_available += "\t - " + name + "\n"

      command_executable = "{} {}".format(sys.executable, sys.argv[0])
      usage = "{} create [entity name]".format(command_executable)
      print("""
Create a new entity (location, user, etc...)
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
      logging.debug("EM: %s", self.entity_manager)
      logging.debug("Available entities: %s", self.entity_manager.get_all_entities())
      if not entity:
         print("Couldn't find the class you are looking for")
         return self.help()
      entity = entity()
      
      print("New {}:\n\n".format(entity_name))

      self.ask_for_fields(entity)

      for name, relationship in entity.relationships.items():
         if isinstance(relationship, ManyToMany):
            pass
            # Do something for many to many
         elif isinstance(relationship,  OneToMany):
            #get all remote entities
            available_data = list(relationship.find_all())
            available_data = list(map(lambda x: (x.render_excerpt(), x),available_data))
            logging.debug(available_data)
            questions = [inquirer.Checkbox("relation",
                  message="Which {}?".format(name),
                  choices=available_data,
            )]
            res = inquirer.prompt(questions)
            logging.debug(res)
            setattr(entity, name, res["relation"])
         elif isinstance(relationship, OneToOne):
            #get all remote entities
            available_data = list(relationship.find_all())
            available_data = list(map(lambda x: (x.render_excerpt(), x),available_data))
            logging.debug(available_data)
            questions = [inquirer.List("relation",
                  message="Which {}?".format(name),
                  choices=available_data,
            )]
            res = inquirer.prompt(questions)
            logging.debug(res)
            setattr(entity, name, res["relation"])

      #TODO add resume plus confirm
      entity.save()
      print("New {} {} created succesfully".format(entity_name, entity.id))

   def ask_for_fields(self, entity):
      fields = entity.fields
      fields = { k:v for (k,v) in fields.items() if v is not "relationship" }
      questions = map(lambda f: inquirer.Text(f, message="{}".format(f)), fields)
      answers = inquirer.prompt(questions)
      logging.debug("Creating entity (%s) with values %s", entity, answers)
      for field, value in answers.items():
         setattr(entity, field, value)
      