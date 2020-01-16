from .relationship import Relationship

class OneToOne(Relationship):
   """
   Users
      id
      
   Locations
      user_id

   from a location get the user

   """
   def find(self):
      sql = "SELECT * FROM {} WHERE {} = {}".format(
         self._foreign_entity.table_name, 
         self.local_entity.table_name + "_id",
         self.local_entity.key
      )
      em = EntityManager()
      db = em.db
      cursor = db.cursor()
      res = cursor.execute(sql)
      return self.foreign_entity.build(res)


