from .command import Command
from db.entity_manager import EntityManager
from db.relationships.many_to_many import ManyToMany
from db.relationships.one_to_many import OneToMany
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
      usage = "{} update [entity name] [id][".format(command_executable)
      print("""
Update an existing entity (location, user, etc...)
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
      if len(args) != 2:
         print("You must only provide a single id to update")

      entity = entity.find(args[1])
      if entity is None:
         print("Couldn't find {} {}".format(args[0],args[2]))
      
      print("Updating {}:\n\n".format(entity_name))

      self.ask_for_fields(entity)

      for name, relationship in entity.relationships.items():
         if isinstance(relationship, ManyToMany):
            pass
            # Do something for many to many
         elif isinstance(relationship,  OneToMany):
            #get all remote entities
            questions = [inquirer.Checkbox(name,
                  message="Which {}?".format(name),
                  choices=relationship.find_all(),
            )]
            res = inquirer.prompt(questions)
            setattr(entity, relationship.name, res)

      #TODO add resume plus confirm
      entity.save()
      print("{} updated succesfully".format(entity_name))

   def ask_for_fields(self, entity):
      questions = map(lambda f: inquirer.Text(f, message="{}".format(f)), entity.fields)
      answers = inquirer.prompt(questions)
      logging.debug("Creating entity (%s) with values %s", entity, answers)
      for field, value in answers.items():
         setattr(entity, field, value)
      