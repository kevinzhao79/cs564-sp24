WITH temp(ItemID, NumCategories) AS (
    SELECT ItemID, COUNT(ItemID)
    FROM Category
    GROUP BY ItemID
)

SELECT COUNT(ItemID) 
FROM temp 
WHERE NumCategories = 4;