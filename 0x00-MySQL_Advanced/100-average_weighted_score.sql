-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE
ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
  DECLARE weight_factor INT;

  SELECT SUM(weight) INTO weight_factor FROM projects;

  UPDATE users SET average_score = (
    SELECT SUM(score * ((SELECT weight FROM projects WHERE projects.id = corrections.project_id)/weight_factor)) FROM corrections WHERE corrections.user_id = user_id
  )
  WHERE id = user_id;

END //

DELIMITER ;
