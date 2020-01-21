-- Vue pour la lecture des messages
-- Faut-il rajouter les messages dont on est le destinataire ?
CREATE VIEW personnal_message AS
SELECT personne.id, message.contenu
FROM personne
INNER JOIN message 
    ON message.author_id = personne.id
;


-- Vue des locations d'un utilisateur
CREATE VIEW location_personne AS
SELECT bien_immobilier_id, date_arrivee, duree, estConfirmee, personne.id
FROM personne
INNER JOIN location
    ON location.locataire_id = personne.id
WHERE location.estConfirmee <> FALSE
;

