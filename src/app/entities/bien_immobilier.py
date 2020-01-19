from ..db.entity import Entity

class BienImmobilier(Entity):
   fields = {
      "charge": "string",
      "tarif_journalier": "string",
      "description": "string",
      "capacite": "string",
      "taille": "string",
      "proprietaire_id" : "relationship",
      "addresse_id" : "relationship",
      "type_bien_nom": "relationship"
   }
   
   relationships = {
      "proprietaire": OneToOne("bien_immobilier", "personne", "id", "proprietaire_id"),
      "addresse": OneToOne("bien_immobilier", "addresse", "id", "addresse_id"),
   }