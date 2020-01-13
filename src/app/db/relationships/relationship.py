class Relationship:
   from_table = ""
   local_key = ""
   foreign_key = ""
   foreign_table = ""
   _foreign_data = None
   _local_data = None
   _foreign_entity = None
   _local_entity = None
   foreign_entity_name = ""
   local_entity_name = ""

   """
   All entity names must be declared in ```/app/entities/__init__.py```
   """
   def __init__(self, local_entity_name, foreign_entity_name):
      self.local_entity_name = local_entity_name
      self.foreign_entity_name = foreign_entity_name

      self.manager = EntityManager()
      self.db = self.manager.db

   def get_all_foreign_entities(self):
      self.db.query()

   def boot(self, local_entity, remote_entity):
      self.local_entity = local_entity()
      self.foreign_entity = remote_entity()

      self.from_table = self.local_entity.table_name
      self.local_key = self.local_entity.key

      self.foreign_table = self.foreign_entity.table_name
      self.foreign_key = self.foreign_entity.key

   def build(self, **data): 
      if self.local_entity.class_name in data:
         self._local_data = data[self.local_entity.class_name]
      if self._foreign_entity.class_name in data:
         self._foreign_data = data[self._foreign_entity.class_name]

   def find(self):
      pass

   def save(self, entity):
      """
      entity: Local entity that is going to be saved
      """
      #one to many required local field to be sometable_id = id
      #many to many requires pivot table and multiple entities be modified and found before hand
      if self._local_data is not None:
         setattr(entity, self.local_key, self._local_data)
      if self._foreign_data is not None:
         setattr(entity, self.foreign_key, self._foreign_data)