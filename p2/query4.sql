WITH temp(HighPrice) AS (
    SELECT MAX(Currently)
    FROM Item)

SELECT Item.ItemID 
FROM Item, temp
WHERE Item.Currently = temp.HighPrice;