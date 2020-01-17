from .relationship import Relationship
from db.entity_manager import EntityManager
from db.entity import Entity
import logging
from collections.abc import Iterable

class OneToOne(Relationship):
   """
   Users
      id

   Locations
      user_id

   from a user get multiple locations

   """
   def find(self, entity):
      if getattr(entity,self.local_key) is None:
         return None
      sql = "SELECT * FROM {} WHERE {} = {} LIMIT 0,1".format(
         self.foreign_table, 
         self.foreign_key,
         getattr(entity,self.local_key)
      )
      logging.debug("QUERY: %s", sql)
      em = EntityManager()
      db = em.db
      cursor = db.cursor(dictionary=True)
      cursor.execute(sql)
      res = cursor.fetchone()
      if res is None:
         return None
      return self.foreign_entity.build(**res)

   def find_all(self): #return every data available in foreign table
      return self.foreign_entity.find()

   def save(self, entity):
      if self._data is None:
         return
      if not self._data.exists:
         self._data.save()
      assert isinstance(self._data, Entity) #must be iterable, many remote models to one local entity, not the other way around
      setattr(entity, self.local_key, self._data.key) #set the entity attribute to {table_name}_id = this entities key
      if entity.was_recently_created:
         entity._update_db({self.local_key:self._data.key}) #save the entity if created, making an update of it
      else:
         entity.save()

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