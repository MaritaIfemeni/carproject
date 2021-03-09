CREATE EVENT rent_manager
ON SCHEDULE
EVERY 1 HOUR
COMMENT 'Manages expired rents and car status.'
DO
UPDATE rentacar_car
INNER JOIN rentacar_rent ON rentacar_car.carNumber = rentacar_rent.carNumber_id
SET rentacar_rent.expired = IF(rentacar_rent.endDate < now(), 1,0), rentacar_car.status = IF(rentacar_rent.endDate < now(), 2,1)
WHERE rentacar_rent.startDate < now() AND rentacar_rent.expired < 1;