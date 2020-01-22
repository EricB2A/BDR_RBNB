from db.entity import Entity

class Commune(Entity):
   _table_name = "commune"
   _key_name = "nom"
   fields = {
      "nom" : "string",
      "etat" : "string",
      "pays_nom" : "string"
   }