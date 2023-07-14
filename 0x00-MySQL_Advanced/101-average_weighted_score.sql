-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DROP procedure IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE
ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE weight_factor INT;

  SELECT SUM(weight) INTO weight_factor FROM projects;

  UPDATE users INNER JOIN corrections
  ON users.id = corrections.user_id
  SET average_score = (
    SELECT SUM(score * ((SELECT weight FROM projects WHERE projects.id = corrections.project_id)/weight_factor))
    FROM corrections
    WHERE corrections.user_id = users.id
  )
  WHERE corrections.user_id = users.id;

END //

DELIMITER ;
