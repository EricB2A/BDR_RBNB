use airbnb;

-- Vue pour la lecture des messages
-- Faut-il rajouter les messages dont on est le destinataire ?
DROP VIEW IF EXISTS personnal_message;
CREATE VIEW personnal_message AS
SELECT personne.id, message.contenu
FROM personne
INNER JOIN message 
    ON message.author_id = personne.id
;


-- Vue des locations d'un utilisateur
DROP VIEW IF EXISTS location_personne;
CREATE VIEW location_personne AS
SELECT bien_immobilier_id, date_arrivee, duree, estConfirme, personne.id
FROM personne
INNER JOIN location
    ON location.locataire_id = personne.id
WHERE location.estConfirme <> FALSE
;

DROP VIEW IF EXISTS search_biens;
CREATE VIEW `search_biens` AS 
SELECT bi.id 'bien_id', taille, capacite, description, p.nom 'pays',tb.nom 'type_bien' ,
        proprio.nom , c.nom 'commune', etat, rue, complement_rue,
        numero, npa, bi.tarif_journalier, bi.charges
FROM bien_immobilier bi
    -- relatif à postion/adresse complète de l'appartement
    INNER JOIN adresse a ON bi.adresse_id = a.id
    INNER JOIN commune c ON a.commune_nom = c.nom
    INNER JOIN pays p ON c.pays_nom = p.nom 
    -- relatif au type de bien
    INNER JOIN type_bien tb ON bi.type_bien_nom = tb.nom
    -- relatif au proprio
    INNER JOIN personne proprio ON bi.proprietaire_id = proprio.id;
select * from search_biens;
        
-- Vue des biens en attente d'un propriétaire
/*
DROP VIEW IF EXISTS location_prioprietaire;
CREATE VIEW location_prioprietaire AS
SELECT 
FROM search_biens 
;
*/