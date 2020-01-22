-- Procedure d'annulation des réservations passées
DROP PROCEDURE IF EXISTS annule_ancienne_locations;
DELIMITER //
CREATE PROCEDURE annule_ancienne_locations()
BEGIN
    UPDATE location
    SET estConfirmee = false
    WHERE location.date_debut < NOW()
    AND location.estConfirmee IS NULL;
END //

-- Procedure pour valider une location et invalider les locations chevauchantes
DROP PROCEDURE IF EXISTS valide_location;
DELIMITER //
CREATE PROCEDURE valide_location(
    IN loc_id int(11)
)
BEGIN
	DECLARE bien_immo int(11);
    DECLARE date_arr DATE;
    DECLARE date_dep DATE;
    IF ((SELECT COUNT(id) FROM location WHERE id = loc_id) = 1) THEN 
		SET bien_immo = (SELECT bien_immobilier_id FROM location WHERE id = loc_id);
		SET date_arr = (SELECT date_arrivee FROM location WHERE id = loc_id);
	    SET date_dep = (SELECT ADDDATE(date_arrivee, duree) FROM location WHERE id = loc_id);
UPDATE location 
SET 
    estConfirme = TRUE
WHERE
    id = loc_id;
UPDATE location 
SET 
    estConfirme = FALSE
WHERE
    estConfirme IS NULL
        AND location.bien_immobilier_id = bien_immo
        AND ((location.date_arrivee BETWEEN date_arr AND date_dep)
        OR (ADDDATE(location.date_arrivee, location.duree) BETWEEN date_arr AND date_dep)
        OR (date_arr BETWEEN location.date_arrivee AND ADDDATE(location.date_arrivee, location.duree))
        );
    END IF;
END //
DELIMITER ;


-- Procedure pour vérifier si un bien est libre à une date donnée
DROP PROCEDURE IF EXISTS verifie_location_possible;
CREATE PROCEDURE verifie_location_possible(
    IN bien_immo_id int(11),
    IN date_deb DATE,
    IN duree int(11),
    OUT possible boolean
)
BEGIN
    IF(SELECT COUNT(id) FROM location 
        WHERE bien_immobilier_id = bien_immo_id
        AND dates_superposees)
    
