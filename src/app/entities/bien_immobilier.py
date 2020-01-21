from db.entity import Entity
from db.relationships.one_to_many import OneToMany
from db.relationships.one_to_one import OneToOne

class BienImmobilier(Entity):
   _table_name = "bien_immobilier"
   fields = {
      "charges": "string",
      "tarif_journalier": "string",
      "description": "string",
      "capacite": "string",
      "taille": "string",
      "proprietaire_id" : "relationship",
      "adresse_id" : "relationship",
      "type_bien_nom": "relationship"
   }
   
   relationships = {
      "proprietaire": OneToOne("bien_immobilier", "personne", "id", "proprietaire_id"),
      "addresse": OneToOne("bien_immobilier", "addresse", "id", "addresse_id"),
      "type_bien": OneToOne("bien_immobilier", "type_bien", "nom", "type_bien_nom"),
   }