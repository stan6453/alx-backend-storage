-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE
ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE weight_factor INT;

  SELECT SUM(weight) INTO weight_factor FROM projects;

END //

DELIMITER ;
