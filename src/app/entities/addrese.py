from db.entity import Entity

class Addresse(Entity):
   _table_name = "adresse"
   fields = {
      "rue": "string",
      "complement_rue": "string",
      "numero": "string",
      "npa": "string",
      "ville": "string",
      "commune_nom": "string",
   }