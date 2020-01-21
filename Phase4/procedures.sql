-- Procedure d'annulation des réservations passées
DELIMITER //
CREATE PROCEDURE cancel_location_passed()
BEGIN
    UPDATE location
    SET estConfirmee = false
    WHERE location.date_debut < NOW()
    AND location.estConfirmee IS NULL;
END //

DELIMITER ;

-- Procedure 

