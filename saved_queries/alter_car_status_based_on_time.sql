UPDATE rentacar_car
INNER JOIN rentacar_rent ON rentacar_car.carNumber = rentacar_rent.carNumber_id
SET rentacar_car.status = IF(rentacar_rent.endDate < now(), 0,1), rentacar_rent.expired = IF(rentacar_rent.endDate < now(), 1,0)
WHERE rentacar_rent.startDate < now()