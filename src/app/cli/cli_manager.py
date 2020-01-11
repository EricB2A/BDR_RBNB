from db.entity_manager import EntityManager
import sys
class Cli:
   actions = {
      # 'delete': lambda entity, id: EntityManager.get_entity(entity).findOne(id).delete()
      # 'create': lambda entity, fields: EntityManager.get_entity(entity).create(Cli.ask(EntityManager.get_entity(entity).fields))
      # 'update': lambda entity, id, fields: EntityManager.get_entity(entity).findOne(id).update(Cli.ask(EntityManager.get_entity(entity).fields))
      # 'find': lambda entity, query: EntityManager.get_entity(entity).find(query)
   }

   def __init__(self, config, entities):
      self.config = config
      self.entities = entities

   def _parse_args(self):
      return sys.argv[1:]

   def help(self, path = []):
      if len(path) <= 0:
         print("Some help with the general application")
      elif len(path) == 1:
         print("Help with actions, list all actions for example")
      elif len(path) == 2:
         print("Print help on action + entity, which means interogating entity manager to see what we can do")
      else:
         print("all hell broke loose hallelujah")

   def get_action(self, *args):
      return {
         name: args[0],
         arguments: args[1:] if len(args) > 1 else []
      }

   def run(self):
      #arguments have the following format
      # (action) (entity) (any other needed arguments)
      # action represents anything the cli can do
      # entity provides where to execute the action, if needed
      # the rest of the arguments are supplied to the callee function
      action = self.get_action(self._parse_args())
      if action.name not in actions:
         print("Action not found")
         self.help()
      if len(action.arguments) <= 2:
         self.help(action.arguments)
      return self.actions[action.name](action.arguments)
      print("Hello world!")