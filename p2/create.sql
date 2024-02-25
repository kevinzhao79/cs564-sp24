DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Person;

CREATE TABLE Seller(
    SellerID text NOT NULL,
    ItemID int NOT NULL,
    Location text NOT NULL,
    Country text NOT NULL,
    Rating int NOT NULL,
    PRIMARY KEY (SellerID, ItemID),
    FOREIGN KEY (SellerID) REFERENCES Person(PersonID),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

CREATE TABLE Item(
    ItemID int PRIMARY KEY,
    Name text NOT NULL,
    BuyPrice real,
    FirstBid real NOT NULL,
    NumberOfBids int NOT NULL,
    Currently real NOT NULL DEFAULT 0.00,
    Started date NOT NULL,
    Ends date NOT NULL,
    Description text NOT NULL
);

CREATE TABLE Bid(
    BidderID text NOT NULL,
    ItemID int NOT NULL,
    Time text NOT NULL,
    Amount real NOT NULL,
    PRIMARY KEY (BidderID, ItemID, Time),
    FOREIGN KEY (BidderID) REFERENCES Person(PersonID),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

CREATE TABLE Category(
    ItemID int NOT NULL,
    Category text NOT NULL,
    PRIMARY KEY (ItemID, Category),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

CREATE TABLE Person(
    PersonID text NOT NULL PRIMARY KEY,
    NumItemsSelling int DEFAULT 0,
    NumItemsBidding int DEFAULT 0,
    Location text, 
    Rating int DEFAULT 0
);


