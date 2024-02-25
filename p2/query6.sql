SELECT COUNT(PersonID)
FROM Person 
WHERE NumItemsBidding > 0
AND NumItemsSelling > 0;