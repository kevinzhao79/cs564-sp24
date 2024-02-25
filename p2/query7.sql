SELECT COUNT(DISTINCT(C.Category))
FROM Category as C JOIN Bid as B ON (C.ItemID = B.ItemID)
WHERE B.Amount > 100;