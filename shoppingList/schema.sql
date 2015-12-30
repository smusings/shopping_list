ALTER TABLE item
ADD price INTEGER

ALTER TABLE item
ADD user_id INTEGER

UPDATE item SET price='0' WHERE price is NULL