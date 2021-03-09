UPDATE rentacar_car
INNER JOIN rentacar_rent ON rentacar_car.carNumber = rentacar_rent.carNumber_id
SET rentacar_rent.expired = IF(rentacar_rent.endDate < now() - interval 1 DAY, 2,1)
WHERE rentacar_rent.expired = 1;