DROP SCHEMA IF EXISTS airbnb;
CREATE SCHEMA airbnb;
USE airbnb;




CREATE TABLE messages(
    id PRIMARY KEY AUTO_INCREMENT,
    contenu VARCHAR(500),
    location_id INT,
    author_id INT
    FOREIGN KEY (location_id) REFERENCES locations(id)
    FOREIGN KEY (author_id) REFERENCES personnes(id)
    
);
CREATE TABLE review(
    id INT PRIMARY KEY AUTO_INCREMENT,
    note SMALLINT, -- CI: à limité à 5 ou 10 à voir
    commentaire VARCHAR(500)
    location_id INT,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);


--

CREATE TABLE pays (
   nom VARCHAR(50),
   PRIMARY KEY (nom)
);

CREATE TABLE commune (
   nom VARCHAR(50),
   etat VARCHAR(50),
   pays_id VARCHAR(50) NOT NULL,
   PRIMARY KEY (nom),
   FOREIGN KEY (pays_id) REFERENCES pays(pays_id)
);

CREATE TABLE adresse (
   id INT AUTO_INCREMENT,
   commune_nom VARCHAR(50),
   rue VARCHAR(50),
   complement_rue VARCHAR(50),
   numero VARCHAR(10),
   npa VARCHAR(10), -- uUuU mais si on est pas en Suisse on fait comment ?
   PRIMARY KEY (id) ,
   FOREIGN KEY (commune_nom) REFERENCES commune(nom)
);
CREATE TABLE personne (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(30),
    prenom VARCHAR(30),
    email VARCHAR(254), -- => rfc5321
    mot_de_Passe VARCHAR(32),
    adresse_id INT,
    genre ENUM('Homme', 'Femme', 'Agender', 'Pangender', 'Androgyne', 'Genre fluide' )
    FOREIGN KEY (adresse_id) REFERENCES adresse(id)
);

CREATE TABLE type_bien (
   nom VARCHAR(50),
   PRIMARY KEY nom
);

CREATE TABLE  bien_immobilier (
   id INT AUTO_INCREMENT,
   adresse_id INT,
   type_bien_nom VARCHAR(50),
   proprietaire_id INT,
   taille SMALLINT, -- en m^2
   capacite SMALLINT, -- n° de places
   description TEXT,
   tarif_journalier DECIMAL(6,2) NOT NULL,
   charges DECIMAL(6,2) NOT NULL,
   PRIMARY KEY (id),
   FOREIGN KEY (adresse_id) REFERENCES adresse(id)
   FOREIGN KEY (type_bien_nom) REFERENCES type_bien(nom)
   FOREIGN KEY (proprietaire_id) REFERENCES personne(id)
);

CREATE TABLE locations(
    id PRIMARY KEY AUTO_INCREMENT,
    date_arrivee DATE, -- changé de date
    duree INT,
    estConfirme BOOLEAN,
    locataire_id,
    bien_immo_id
    FOREIGN KEY (locataire_id) REFERENCES personnes(id)
    FOREIGN KEY (bien_immo_id) REFERENCES bien_immobilier(id)
    
);
