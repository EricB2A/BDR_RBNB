from db.entity import Entity

class Commune(Entity):
   _table_name = "commune"
   fields = {
      "nom" : "string",
      "etat" : "string",
      "pays_nom" : "string"
   }