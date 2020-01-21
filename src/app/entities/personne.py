from db.entity import Entity

class Personne(Entity):
   fields = {
      "id":"primary_key",
      "nom": "string",
      "prenom": "string",
      "email": "string" ,
      "mot_de_passe": "string",
      "adresse_id": "string",
      "genre": "string",
   }