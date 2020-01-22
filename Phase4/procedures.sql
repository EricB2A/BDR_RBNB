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

-- Procedure pour valider une location et invalider les locations chevauchantes
-- DROP PROCEDURE IF EXISTS valide_location;
-- CREATE PROCEDURE valide_location(
--     IN loc_id int(11)
-- )
-- BEGIN
-- 	DECLARE bien_immo int(11);
--     DECLARE date_arr DATE;
--     DECLARE date_dep DATE;
--     IF ((SELECT COUNT(id) FROM location WHERE id = loc_id) = 1) THEN
-- 		SET bien_immo = (SELECT bien_immobilier_id FROM location WHERE id = loc_id);
-- DROP PROCEDURE IF EXISTS valide_location_chevauchant;
-- CREATE PROCEDURE valide_location_chevauchant(
--     IN loc_id int(11)
-- )
-- BEGIN
--     IF (SELECT COUNT(id) FROM location
--         WHERE id = loc_id) = 1
--         THEN UPDATE location
--              SET estConfirmee = TRUE
--              WHERE id = loc_id;
--             UPDATE location
--             SET estConfirme = FALSE
--             WHERE estConfirme IS NULL
--             AND location.bien_immobilier_id = NEW.bien_immobilier_id
--             AND (
--             (location.date_arrivee > NEW.date_arrivee AND location.date_arrivee < (NEW.date_arrivee + NEW.duree))
--              OR (location.date_arrivee + duree > NEW.date_arrivee AND location.date_arrivee + duree < (NEW.date_arrivee + NEW.duree))
--              OR (location.date_arrivee < NEW.date_arrivee AND location.date_arrivee + location.duree > NEW.date_arrivee)
--         );
--     END IF;
-- END //

DELIMITER ;
