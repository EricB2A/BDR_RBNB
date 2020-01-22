use airbnb;

-- Fonction pour inserer une nouvelle location
DROP FUNCTION IF EXISTS insert_location;
DELIMITER //
CREATE FUNCTION insert_location(loc_id int, bien_immo_id int, date_arrivee date, duree int)
RETURNS boolean
DETERMINISTIC
BEGIN
    DECLARE done BOOLEAN;
    IF (SELECT COUNT(id) FROM personne WHERE id = loc_id) = 1
        AND (SELECT COUNT(id) FROM bien_immobilier WHERE id = bien_immo_id) = 1
        AND (date_arrivee < NOW()) 
		THEN
        --    INSERT INTO location (locataire_id, bien_immobilier_id, date_arrivee, duree)
          --  VALUE (loc_id, bien_immo_id, date_arrivee, duree);
            SET done = TRUE;
		ELSE 
            SET done = FALSE;
            
        END IF;
        RETURN done;
END //

-- Vérifie si une location a déjà lieu dans l'intervalle donnée.
DROP FUNCTION IF EXISTS valide_location;
CREATE FUNCTION valide_location(
    loc_id INT,
    starting_date DATE,
    duration INT
)
RETURNS BOOL
READS SQL DATA
BEGIN
    RETURN EXISTS(
        SELECT l.id FROM location as l
        WHERE l.id <> loc_id
        AND (l.date_arrivee BETWEEN starting_date AND DATE_ADD(starting_date, INTERVAL duration DAY))
    );
END //

DELIMITER ;

-- SELECT (insert_location(1, 1, NOW(), 2));
