use airbnb;

-- Vue pour la lecture des messages
DROP VIEW IF EXISTS personnal_message;
CREATE VIEW personnal_message AS
SELECT personne.id, message.contenu
FROM personne
INNER JOIN message
    ON message.author_id = personne.id;

-- Vue des locations d'un utilisateur
DROP VIEW IF EXISTS location_personne;
CREATE VIEW location_personne AS
SELECT bien_immobilier_id, date_arrivee, duree, estConfirme, personne.id  'personne_id'
FROM personne
INNER JOIN location
    ON location.locataire_id = personne.id
WHERE location.estConfirme <> FALSE;

-- Vue affiche le type de bien d'un bien immobilier, son adresse (au complet) ainsi
-- que le propriétaire.
DROP VIEW IF EXISTS search_biens;
CREATE VIEW `search_biens` AS
SELECT bi.id 'bien_id', taille, capacite, description, p.nom 'pays',tb.nom 'type_bien' ,
        proprio.nom , c.nom 'commune', etat, rue, complement_rue, proprio.id 'proprietaire',
        numero, npa, bi.tarif_journalier, bi.charges
FROM bien_immobilier bi
INNER JOIN adresse a ON bi.adresse_id = a.id
INNER JOIN commune c ON a.commune_nom = c.nom
INNER JOIN pays p ON c.pays_nom = p.nom
INNER JOIN type_bien tb ON bi.type_bien_nom = tb.nom
INNER JOIN personne proprio ON bi.proprietaire_id = proprio.id;

-- Vue des biens en attente d'un propriétaire.
DROP VIEW IF EXISTS location_prioprietaire;
CREATE VIEW location_prioprietaire AS
SELECT p.id as proprietaire_id, search_biens.*
FROM search_biens
INNER JOIN personne p ON proprietaire = p.id;

-- Vue des messages liés à une location.
DROP VIEW IF EXISTS message_recus;
CREATE VIEW message_recus AS
SELECT p.prenom 'autheur', m.contenu as 'message', l.id as 'location'
FROM personne p
INNER JOIN location l ON l.locataire_id = p.id
INNER JOIN message m ON m.location_id = l.id;

-- Vue d'un bien, de ses fournitures et du type.
DROP VIEW IF EXISTS fournitures_bien;
CREATE VIEW fournitures_bien AS
SELECT bi.id, bi.taille, bi.capacite, bi.tarif_journalier, bi.charges, bi.description, bi.type_bien_nom, f.nom_fourniture
FROM bien_immobilier bi
INNER JOIN fourniture f ON f.bien_immobilier_id = bi.id;

-- Vue affichant les fourniture d'un bien, son type ainsi que ses reviews.
DROP VIEW IF EXISTS revues_bien;
CREATE VIEW revues_bien AS
SELECT fournitures_bien.*, r.note, r.commentaire
FROM fournitures_bien
INNER JOIN location l ON fournitures_bien.id = l.bien_immobilier_id
INNER JOIN review r ON r.location_id = l.id;
