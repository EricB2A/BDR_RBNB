DROP SCHEMA IF EXISTS airbnb;
CREATE SCHEMA airbnb;
USE airbnb;

CREATE TABLE pays (
   nom VARCHAR(50),
   PRIMARY KEY (nom)
);

CREATE TABLE commune (
   nom VARCHAR(50) PRIMARY KEY,
   etat VARCHAR(50),
   pays_nom VARCHAR(50) NOT NULL,
   FOREIGN KEY (pays_nom) REFERENCES pays(nom)
);

CREATE TABLE adresse (
   id INT AUTO_INCREMENT,
   commune_nom VARCHAR(50),
   rue VARCHAR(50) NOT NULL,
   complement_rue VARCHAR(50),
   numero VARCHAR(10),
   npa VARCHAR(10) NOT NULL, -- uUuU mais si on est pas en Suisse on fait comment ?
   ville VARCHAR(50) NOT NULL,
   PRIMARY KEY (id) ,
   FOREIGN KEY (commune_nom) REFERENCES commune(nom)
);

CREATE TABLE personne (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(80) NOT NULL, -- => should be 254 => rfc5321 BUT UNIQUE MAX 80~
    mot_de_passe VARCHAR(64) NOT NULL,
    adresse_id INT,
    genre ENUM('Homme', 'Femme', 'Agender', 'Pangender', 'Androgyne', 'Genre fluide' ),
    UNIQUE (email), 
    FOREIGN KEY (adresse_id) REFERENCES adresse(id)
);

CREATE TABLE type_bien (
   nom VARCHAR(50) PRIMARY KEY
);

CREATE TABLE  bien_immobilier (
   id INT AUTO_INCREMENT PRIMARY KEY,
   adresse_id INT NOT NULL,
   type_bien_nom VARCHAR(50) NOT NULL,
   proprietaire_id INT NOT NULL,
   taille SMALLINT, -- en m^2
   capacite SMALLINT, -- n° de places
   description VARCHAR(10000),
   tarif_journalier DECIMAL(6,2) NOT NULL,
   charges DECIMAL(6,2) NOT NULL,
   FOREIGN KEY (adresse_id) REFERENCES adresse(id),
   FOREIGN KEY (type_bien_nom) REFERENCES type_bien(nom),
   FOREIGN KEY (proprietaire_id) REFERENCES personne(id)
);

CREATE TABLE location (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date_arrivee DATE NOT NULL, -- changé de date
    duree INT NOT NULL,
    estConfirme BOOLEAN NOT NULL DEFAULT 0,
    locataire_id INT NOT NULL,
    bien_immobilier_id INT NOT NULL,
    FOREIGN KEY (locataire_id) REFERENCES personne(id),
    FOREIGN KEY (bien_immobilier_id) REFERENCES bien_immobilier(id)
);
CREATE TABLE type_fourniture(
    nom VARCHAR(50) PRIMARY KEY
);

CREATE TABLE fourniture (
   id INT AUTO_INCREMENT PRIMARY KEY,
   description VARCHAR(10000),
   bien_immobilier_id INT NOT NULL,
   nom_fourniture VARCHAR(50) NOT NULL,
   FOREIGN KEY (nom_fourniture) REFERENCES type_fourniture(nom),
   FOREIGN KEY (bien_immobilier_id) REFERENCES bien_immobilier(id)
);

CREATE TABLE message (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contenu VARCHAR(500),
    location_id INT NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location(id),
    FOREIGN KEY (author_id) REFERENCES personne(id)
    
);
CREATE TABLE review (
    id INT PRIMARY KEY AUTO_INCREMENT,
    note SMALLINT NOT NULL, -- CI: à limité à 5 ou 10 à voir
    commentaire VARCHAR(500),
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location(id)
);
