
#TABLETION
CREATE TABLE Person (
    ID INT,
    Email VARCHAR(30) NOT NULL,
    Named VARCHAR(25) NOT NULL,
    DateofBirth DATE NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    Address VARCHAR(30) NOT NULL,
    DateJoined DATE NOT NULL,
    IsEmployee CHAR(1) DEFAULT 'N',
    PRIMARY KEY (ID),
    CHECK (IsEmployee IN ('Y' , 'N'))
);

CREATE TABLE Customer (
    CustomerID INT,
    Username VARCHAR(20) NOT NULL,
    Userpass VARCHAR(20) NOT NULL,
    HasMembership CHAR(1) DEFAULT 'N',
    PRIMARY KEY (CustomerID),
    FOREIGN KEY (CustomerID)
        REFERENCES Person (ID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    CHECK (HasMembership IN ('Y' , 'N'))
);
    
CREATE TABLE Employee (
    ID INT NOT NULL,
    EmployeeID INT,
    Supervisor INT,
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (Supervisor)
        REFERENCES Employee (EmployeeID)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (ID)
        REFERENCES Person (ID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);
                
CREATE TABLE Item (
    ItemID INT,
    Quantity INT NOT NULL,
    Price DEC(9 , 2 ) NOT NULL,
    ItemType VARCHAR(15) NOT NULL,
    Seller VARCHAR(15) NOT NULL,
    ItemDesc VARCHAR(100),
    PRIMARY KEY (ItemID)
);

CREATE TABLE ShoppingCart (
    CustomerID INT,
    ItemID INT,
    Quantity INT NOT NULL,
    PRIMARY KEY (CustomerID , ItemID),
    FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ItemID)
        REFERENCES Item (ItemID)
        ON DELETE CASCADE ON UPDATE CASCADE
    #CHECK (Quantity < Item.Quantity)
);

CREATE TABLE WishList (
    CustomerID INT,
    ItemID INT,
    PRIMARY KEY (CustomerID , ItemID),
    FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ItemID)
        REFERENCES Item (ItemID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Orders (
    OrderNum INT,
    CustomerID INT,
    OrderDate DATE NOT NULL,
    Completed CHAR(1) DEFAULT 'N',
    PRIMARY KEY (OrderNum),
    FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    CHECK (Completed IN ('Y' , 'N'))
);

CREATE TABLE OrderedItems (
	OrderID INT,
    ItemID INT,
    Quantity INT,
    PRIMARY KEY (OrderID, ItemID),
    FOREIGN KEY (OrderID)
		REFERENCES Orders (OrderNum)
        ON DELETE NO ACTION ON UPDATE CASCADE,
	FOREIGN KEY (ItemID)
		REFERENCES Item (ItemID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE Payment (
    OrderID INT,
    CardNum VARCHAR(16) NOT NULL,
    CVS INT(3) NOT NULL,
    CardComp VARCHAR(10) NOT NULL,
    CardType VARCHAR(10) NOT NULL,
    CardExp DATE NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID)
        REFERENCES Orders (OrderNum)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE Shipment (
    OrderID INT,
    Address VARCHAR(30) NOT NULL,
    Details VARCHAR(30),
    Fee INT NOT NULL,
    Company VARCHAR(10) NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID)
        REFERENCES Orders (OrderNum)
        ON DELETE NO ACTION ON UPDATE CASCADE
);
    
CREATE TABLE Returnment (
    OrderID INT,
    ItemID INT,
    Quantity INT,
    Comments VARCHAR(100) NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID)
        REFERENCES Orders (OrderNum)
        ON DELETE NO ACTION ON UPDATE CASCADE,
	FOREIGN KEY (ItemID)
		REFERENCES OrderedItems (ItemID)
        ON DELETE NO ACTION ON UPDATE CASCADE
	#CHECK (Quantity < OrderedItems.Quantity)
);
                
CREATE TABLE Reviews (
    CustomerID INT,
    ItemID INT,
    Ratings INT NOT NULL,
    Comments VARCHAR(100) NOT NULL,
    PRIMARY KEY (CustomerID, ItemID),
    FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (ItemID)
        REFERENCES OrderedItems (ItemID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
	CHECK(Ratings IN('1', '2', '3', '4', '5'))
);


#INSERTIONS
INSERT INTO	Person VALUES('368192', 'bob.builder@gmail.com', 'Bobby', '1998-11-30', '9179179170', 'Linden', '2018-11-23', 'N');
INSERT INTO	Person VALUES('251059', 'billy.cat@gmail.com', 'Billy', '1996-03-11', '9179179171', 'Queens', '2018-01-24', 'N');
INSERT INTO	Person VALUES('592134', 'sam.televi@gmail.com', 'James', '1992-05-14', '9179179172', 'Ithaca', '2017-09-01', 'N');
INSERT INTO	Person VALUES('845523', 'mars.nasa@gmail.com', 'Tenmond', '2001-11-25', '9179179173', 'Stony', '2017-03-26', 'Y');
INSERT INTO	Person VALUES('359803', 'plane.wire@gmail.com', 'Rayzin', '1967-10-12', '9179179174', 'Ithaca', '2018-01-27', 'Y');
INSERT INTO	Person VALUES('432591', 'thom.sanjr@gmail.com', 'Thomsan', '1912-02-07', '4545454545', 'Hurst', '2015-05-15', 'Y');

INSERT INTO Customer VALUES('368192', 'Bob999', 'password', 'N');
INSERT INTO Customer VALUES('251059', 'Billy899', 'wordpass', 'N');
INSERT INTO Customer VALUES('592134', 'Samm333', 'secretive', 'Y');

INSERT INTO Employee VALUES('432591', '7645', NULL);
INSERT INTO Employee VALUES('845523', '1265', '7645');
INSERT INTO Employee VALUES('359803', '4552', '7645');

INSERT INTO Item VALUES('1233', '500', '123.00', 'IPhone X', 'Apple', 'A fancy phone');
INSERT INTO Item VALUES('18332', '90', '90.00', 'Soccer Ball', 'Tottenham', 'A ball that wins nothing');
INSERT INTO Item VALUES('81234', '200', '10.00', 'Diamond', 'PewDiePie', NULL);

INSERT INTO ShoppingCart VALUES('368192', '1233', '400');
INSERT INTO ShoppingCart VALUES('251059', '18332', '10');
INSERT INTO ShoppingCart VALUES('592134', '81234', '50');

INSERT INTO WishList VALUES('368192', '1233');
INSERT INTO WishList VALUES('251059', '18332');
INSERT INTO WishList VALUES('592134', '81234');

INSERT INTO Orders VALUES('4444', '368192', '2018-11-25', 'Y');
INSERT INTO Orders VALUES('21344', '251059', '2019-04-08', 'N');
INSERT INTO Orders VALUES('332', '592134', '2012-08-10', 'Y');

INSERT INTO OrderedItems VALUES('4444', '1233', '5');
INSERT INTO OrderedItems VALUES('4444', '18332', '10');
INSERT INTO OrderedItems VALUES('21344', '18332', '10');
INSERT INTO OrderedItems VALUES('332', '18332', '20');

INSERT INTO Payment VALUES('4444', '1234567891235674', '315', 'Chase', 'Debit', '2018-11-25');
INSERT INTO Payment VALUES('21344', '1234567891234567', '474', 'MasterCard', 'Credit', '2018-11-25');
INSERT INTO Payment VALUES('332', '6123456789123456', '908', 'Discover', 'Credit', '2018-11-25');

INSERT INTO Shipment VALUES('4444', '100 Circle Rd', 'Fragile', '10', 'USPS');
INSERT INTO Shipment VALUES('21344', '101 Circle Rd', 'Fragile', '5', 'UPS');
INSERT INTO Shipment VALUES('332', '102 Circle Rd', NULL, '3', 'FEDEX');

INSERT INTO Returnment VALUES('4444', '18332', '5', 'Balls are broken');

INSERT INTO Reviews VALUES('368192', '1233', '2', 'It would not turn on');
INSERT INTO Reviews VALUES('592134', '18332', '5', 'It\'s pretty good');
