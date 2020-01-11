from db.entity_manager import EntityManager

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
      pass
   def help(self):
      pass
   def run(self):
      print("Hello world!")