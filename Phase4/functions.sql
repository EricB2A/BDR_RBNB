use airbnb;

-- Fonction qui vérifie si deux périodes se chevauchent
DROP FUNCTION IF EXISTS dates_surperposees;
DELIMITER //
CREATE FUNCTION dates_surperposees(date1 DATE, date2 DATE, duree1 int, duree2 int)
RETURN boolean
DECLARE reponse boolean
    IF (date1 BETWEEN date2 AND ADDDATE(date2, duree2)
        OR ADDDATE(date1, duree1) BETWEEN date2 AND ADDDATE(date2, duree2)
        OR date2 BETWEEN date1 AND ADDDATE(date1, duree1)) THEN
        SET reponse = TRUE;
    ELSE
        SET reponse = FALSE;
    END IF;
RETURN reponse;
END //

-- Vérifie si une location a déjà lieu dans l'intervalle donnée.
DROP FUNCTION IF EXISTS location_est_occupe;
CREATE FUNCTION location_est_occupe(
    bien_id INT,
    starting_date DATE,
    duration INT
)
RETURNS BOOL
READS SQL DATA
BEGIN
    RETURN EXISTS(
        SELECT l.id FROM location as l
        WHERE l.bien_immobilier_id = bien_id
        AND ((l.date_arrivee BETWEEN starting_date AND DATE_ADD(starting_date, INTERVAL duration DAY)
        OR (DATE_ADD(l.date_arrivee, INTERVAL duration DAY) BETWEEN starting_date AND DATE_ADD(starting_date, INTERVAL duration DAY) ))
        AND l.estConfirme = 1)
    );
END //

DELIMITER ;

