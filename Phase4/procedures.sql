use airbnb;

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

DELIMITER ;

-- Procedure pour valider une location et invalider les locations chevauchantes
DROP PROCEDURE IF EXISTS valide_location_chevauchant;
DELIMITER //
CREATE PROCEDURE valide_location_chevauchant(
    IN loc_id int(11)
)
BEGIN
    UPDATE location AS t1
    INNER JOIN location as t2
    ON t1.bien_immobilier_id = t2.bien_immobilier_id
    SET t1.estConfirme = IF(t1.id = 11, TRUE, FALSE)
    WHERE t1.estConfirme IS NULL
    AND t2.id = 11
    AND ( dates_superposees(t1.date_arrivee, t2.date_arrivee, t1.duree, t2.duree) IS TRUE
    );
END //

DELIMITER ;
