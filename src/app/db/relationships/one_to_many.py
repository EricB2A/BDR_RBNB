from .relationship import Relationship
from db.entity_manager import EntityManager
import logging
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
         self.foreign_key if self.foreign_key else self.foreign_entity.table_name + "_id",
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
      if not entity.exists:
         entity.save() # first save it, we need it's key

      for remote in self._data:
         setattr(remote, self.local_entity.table_name + "_id", entity.key) #set the remote attribute to {table_name}_id = this entities key
         remote.save()

   def destroy(self):
      sql = "DELETE FROM {} WHERE {} in ({})".format(
         self.foreign_entity.table_name, 
         self.local_entity.table_name + "_id",
         self.local_entity.key
      )
      em = EntityManager()
      db = em.db
      cursor = db.cursor()
      res = cursor.execute(sql)
      db.commit()