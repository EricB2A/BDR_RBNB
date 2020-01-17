from .relationship import Relationship
from db.entity_manager import EntityManager
import logging
from collections.abc import Iterable

class OneToMany(Relationship):
   """
   Users
      id

   Locations
      user_id

   from a user get multiple locations

   """
   def find(self, entity):
      sql = "SELECT * FROM {} WHERE {} in ({})".format(
         self.foreign_table, 
         self.foreign_key,
         entity.key
      )
      logging.debug("QUERY: %s", sql)
      em = EntityManager()
      db = em.db
      cursor = db.cursor(dictionary=True)
      cursor.execute(sql)
      return [self.foreign_entity.build(**data) for data in cursor.fetchall()]

   def find_all(self): #return every data available in foreign table
      return self.foreign_entity.find()

   def save(self, entity):
      if self._data is None:
         return
         
      if not entity.exists:
         entity._persist() # first save it, we need it's key!
      if self._data is None: #no data to be saved go along about our day
         return True

      assert isinstance(self._data, Iterable) #must be iterable, many remote models to one local entity, not the other way around

      for remote in self._data:
         setattr(remote, self.foreign_key, entity.key) #set the remote attribute to {table_name}_id = this entities key
         remote.save()

   def destroy(self):
      if not self.local_entity.exists:
         self._data = []
         return True

      sql = "DELETE FROM {} WHERE {} in ({})".format(
         self.foreign_table, 
         self.foreign_key,
         self.local_entity.key
      )
      em = EntityManager()
      db = em.db
      cursor = db.cursor()
      res = cursor.execute(sql)
      db.commit()