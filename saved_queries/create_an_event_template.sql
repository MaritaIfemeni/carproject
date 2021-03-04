CREATE EVENT rent_manager
ON SCHEDULE
EVERY 1 HOUR
COMMENT 'Manages expired rents and car status.'
DO
<insert stuff to do>;