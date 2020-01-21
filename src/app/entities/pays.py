from db.entity import Entity

class Pays(Entity):
   _table_name = "pays"

   fields = {
      "nom": "string"
   }