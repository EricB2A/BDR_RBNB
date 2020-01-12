class Relationship:
   from_table = ""
   local_key = ""
   foreign_key = ""
   foreign_table = ""
   _foreign_data = None
   _local_data = None
   _foreign_entity = None
   _local_entity = None
   def __init__(self, foreign_entity, local_entity):
      self.from_table = local_entity.table_name
      self.local_key = local_entity.key
      self.foreign_table = foreign_entity.table_name
      self.foreign_key = foreign_entity.key

      self.manager = EntityManager()
      self.db = self.manager.db

   def get_all_foreign_entities(self):
      self.db.query()

   def build(self, **data):
      
      if self.local_entity.name in data:
         self._local_data = data[self.local_entity.name]
      if self._foreign_entity.name in data:
         self._foreign_data = data[self._foreign_entity.name]
   def find(self):
      pass

   def save(self, entity):
      #one to many required local field to be sometable_id = id
      #many to many requires pivot table and multiple entities be modified and found before hand
      if self._local_data is not None:
         setattr(entity, self.local_key, self._local_data)
      if self._foreign_data is not None:
         setattr(entity, self.foreign_key, self._foreign_data)