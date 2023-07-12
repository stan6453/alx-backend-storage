-- a SQL script that creates a trigger that decreases the quantity of an item after adding a new order.

DELIMITER $$

CREATE TRIGGER decreases_item
AFTER INSERT ON orders FOR EACH ROW
BEGIN
  UPDATE items SET quantity = ((SELECT items.quantity from items where items.name = NEW.item_name) - NEW.number)
  WHERE NEW.item_name = items.name
END$$

DELIMITER;