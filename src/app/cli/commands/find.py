from .command import Command
from db.entity_manager import EntityManager
from db.entity import Entity
from db.relationships.many_to_many import ManyToMany
from db.relationships.one_to_many import OneToMany
from db.relationships.one_to_one import OneToOne
import sys
import logging
import inquirer
import termtables as tt


class Find(Command):
   headers = list()

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
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
      em = EntityManager()

      if len(args) < 1:
         return self.help()
      entity_name = args[0]
      entity = em.get_entity(entity_name)
      if not entity:
         print("Couldn't find the class you are looking for")
         return self.help()
      
      ids = args[1:]
      res = None
      if len(ids) > 0:
         res = entity.find(ids)
      else:
         res = entity.find()

      data = []
      self.headers = list(entity.fields.keys())
      self.headers.insert(0, "id")
      logging.debug("GOT MODELS: %s",res)
      if isinstance(res, Entity):
         data = [e.key] + [ self._get_data_from_entity(res) ]
      else:
         for e in res:
            data.append([e.key] + self._get_data_from_entity(e))
         
      
      if len(data) <= 0:
         data = [ [ "" for i in range(len(self.headers)) ]] 

      logging.debug(data)
      logging.debug(self.headers)
      string = tt.to_string(
         data,
         header=self.headers,
         style=tt.styles.ascii_thin_double,
      )
      print(string)
      
   def _get_data_from_entity(self, entity):
      relations = list()
      for n,relation in entity.relationships.items():

         if isinstance(relation, OneToMany):
            relations.append(list(map(lambda e_: e_.render_excerpt(), relation.find(entity))))
         elif isinstance(relation, OneToOne):
            r = relation.find(entity)
            relations.append(r.render_excerpt() if r is not None else None)

         if n not in self.headers:
            self.headers.append(n)
      def map_relations(rel):
         if isinstance(rel, list):
            return ", ".join(rel)
         return rel
      
      return [ getattr(entity,k) for k in entity.fields.keys() ] + list(map(map_relations, relations))
      
      