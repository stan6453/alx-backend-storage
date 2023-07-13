-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE
ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE weight_factor INT;

  SELECT SUM(weight) INTO weight_factor FROM projects;

  SELECT
  ( 
    UPDATE users SET average_score = (
    SELECT SUM(score * ((SELECT weight FROM projects WHERE projects.id = corrections.project_id)/weight_factor)) FROM corrections WHERE corrections.user_id = users.user_id
  )
  WHERE id = user_id;) FROM users;

END //

DELIMITER ;