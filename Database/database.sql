#TABLETION
CREATE TABLE Person (
    ID INT,
    Email VARCHAR(50) NOT NULL,
    Named VARCHAR(30) NOT NULL,
    DateofBirth DATE NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    DateJoined DATE NOT NULL,
    IsEmployee CHAR(1) DEFAULT 'N',
    PRIMARY KEY (ID)
);

CREATE TABLE Customer (
    CustomerID INT,
    Userpass VARCHAR(30) NOT NULL,
    HasMembership CHAR(1) DEFAULT 'N',
    PRIMARY KEY (CustomerID),
    FOREIGN KEY (CustomerID)
        REFERENCES Person (ID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);
    
CREATE TABLE Employee (
    ID INT NOT NULL,
    EmployeeEmail VARCHAR(50) NOT NULL,
    Supervisor VARCHAR(50),
    Userpass VARCHAR(30) NOT NULL,
    PRIMARY KEY (EmployeeEmail),
    FOREIGN KEY (Supervisor)
        REFERENCES Employee (EmployeeEmail)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (ID)
        REFERENCES Person (ID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);
                
CREATE TABLE Item (
    ItemID INT,
    Quantity INT NOT NULL,
    Price DEC(9 , 2) NOT NULL,
    ItemType VARCHAR(30) NOT NULL,
    Seller VARCHAR(30) NOT NULL,
    ItemDesc VARCHAR(200),
    Category VARCHAR(30) NOT NULL,
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

CREATE TABLE Discount (
	DiscountID INT,
    DiscountPercent DEC(2, 2),
    Valid CHAR(1) DEFAULT 'N',
    PRIMARY KEY (DiscountID)
);

CREATE TABLE Orders (
    OrderNum INT,
    CustomerID INT,
    OrderDate DATE NOT NULL,
    Completed CHAR(1) DEFAULT 'N',
    OrderName VARCHAR(30) NOT NULL,
    OrderEmail VARCHAR(50) NOT NULL,
    PRIMARY KEY (OrderNum),
    FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID)
        ON DELETE NO ACTION ON UPDATE CASCADE
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
    CardName VARCHAR(20) NOT NULL,
    CardNum VARCHAR(16) NOT NULL,
    CardComp VARCHAR(20) NOT NULL,
    CardExp DATE NOT NULL,
    Address1 VARCHAR(200) NOT NULL,
    Address2 VARCHAR(200),
    State VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Zip VARCHAR(5) NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID)
        REFERENCES Orders (OrderNum)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE Shipment (
    OrderID INT,
    Address1 VARCHAR(200) NOT NULL,
    Address2 VARCHAR(200),
    State VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Zip VARCHAR(5) NOT NULL,
    Fee INT NOT NULL,
    Company VARCHAR(20) NOT NULL,
    ShipName VARCHAR(20) NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID)
        REFERENCES Orders (OrderNum)
        ON DELETE NO ACTION ON UPDATE CASCADE
);
    
CREATE TABLE Returnment (
    OrderID INT,
    ItemID INT,
    Quantity INT,
    Comments VARCHAR(200) NOT NULL,
    Approval CHAR(1),
    PRIMARY KEY (OrderID , ItemID),
    FOREIGN KEY (OrderID)
        REFERENCES OrderedItems (OrderID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (ItemID)
        REFERENCES OrderedItems (ItemID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE Reviews (
    CustomerID INT,
    ItemID INT,
    Ratings INT NOT NULL,
    Comments VARCHAR(200) NOT NULL,
    PRIMARY KEY (CustomerID, ItemID),
    FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (ItemID)
        REFERENCES Item (ItemID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE Addresses (
	CustomerID INT,
    Address1 VARCHAR(200) NOT NULL,
    Address2 VARCHAR(200),
    State VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Zip VARCHAR(5) NOT NULL,
    PRIMARY KEY (CustomerID, Address1, State, Country, Zip),
	FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE Cards (
	CustomerID INT,
    CardName VARCHAR(20) NOT NULL,
    CardNum VARCHAR(16) NOT NULL,
    CardComp VARCHAR(20) NOT NULL,
    CardExp DATE NOT NULL,
    PRIMARY KEY (CustomerID, CardName, CardNum, CardComp, CardExp),
	FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID)
        ON DELETE NO ACTION ON UPDATE CASCADE
);


#Constraints
DELIMITER $
#Person IsEmployee
CREATE TRIGGER Insert_IsEmployee_Y_Or_N BEFORE INSERT ON Person 
FOR EACH ROW
BEGIN
    IF NEW.IsEmployee NOT IN ('Y', 'N')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'IsEmployee must be Y or N';
    END IF;
END$

CREATE TRIGGER UPDATE_IsEmployee_Y_Or_N BEFORE UPDATE ON Person 
FOR EACH ROW
BEGIN
    IF NEW.IsEmployee NOT IN ('Y', 'N')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'IsEmployee must be Y or N';
    END IF;
END$

#Customer HasMembership
CREATE TRIGGER Insert_HasMembership_Y_Or_N BEFORE INSERT ON Customer 
FOR EACH ROW
BEGIN
    IF NEW.HasMembership NOT IN ('Y', 'N')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'HasMembership must be Y or N';
    END IF;
END$

CREATE TRIGGER Update_HasMembership_Y_Or_N BEFORE UPDATE ON Customer 
FOR EACH ROW
BEGIN
    IF NEW.HasMembership NOT IN ('Y', 'N')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'HasMembership must be Y or N';
    END IF;
END$

#ShoppingCart Quantity
CREATE TRIGGER Insert_Quantity_ShoppingCart BEFORE INSERT ON ShoppingCart 
FOR EACH ROW
BEGIN
	DECLARE x INT;
	SET x = (SELECT i.Quantity From ITEM i WHERE i.ItemID = New.ItemID);
    IF NEW.Quantity > x
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'The quantity must be less than the quantity of the item';
    END IF;
END$

CREATE TRIGGER Update_Quantity_ShoppingCart BEFORE UPDATE ON ShoppingCart 
FOR EACH ROW
BEGIN
	DECLARE x INT;
	SET x = (SELECT i.Quantity From ITEM i WHERE i.ItemID = New.ItemID);
    IF NEW.Quantity > x
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'The quantity must be less than the quantity of the item';
    END IF;
END$

#Orders Completed
CREATE TRIGGER Insert_Completed_Y_Or_N BEFORE INSERT ON Orders
FOR EACH ROW
BEGIN
    IF NEW.Completed NOT IN ('Y', 'N')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Completed must be Y or N';
    END IF;
END$

CREATE TRIGGER Update_Completed_Y_Or_N BEFORE UPDATE ON Orders
FOR EACH ROW
BEGIN
    IF NEW.Completed NOT IN ('Y', 'N')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Completed must be Y or N';
    END IF;
END$

#Returnment Quantity
CREATE TRIGGER Insert_Quantity_Returnment BEFORE INSERT ON Returnment 
FOR EACH ROW
BEGIN
	DECLARE x INT;
	SET x = (SELECT o.Quantity From OrderedItems o WHERE o.OrderID = New.OrderID AND o.ItemID = NEW.ItemID);
    IF NEW.Quantity > x
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'The quantity must be less than the quantity of the ordered item';
    END IF;
END$

CREATE TRIGGER Update_Quantity_Returnment BEFORE UPDATE ON Returnment 
FOR EACH ROW
BEGIN
	DECLARE x INT;
	SET x = (SELECT o.Quantity From OrderedItems o WHERE o.OrderID = New.OrderID AND o.ItemID = NEW.ItemID);
    IF NEW.Quantity > x
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'The quantity must be less than the quantity of the ordered item';
    END IF;
END$

#Returnment Approval
CREATE TRIGGER Insert_Approval BEFORE INSERT ON Returnment
FOR EACH ROW
BEGIN
    IF NEW.Approval NOT IN ('Y', 'N', NULL)
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Completed must be Y, N, or NULL';
    END IF;
END$

CREATE TRIGGER Update_Approval BEFORE UPDATE ON Returnment
FOR EACH ROW
BEGIN
    IF NEW.Approval NOT IN ('Y', 'N', NULL)
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Updated Approval must be Y, N, or NULL';
    END IF;
END$

#Review Ratings
CREATE TRIGGER Insert_Ratings_1_to_5 BEFORE INSERT ON Reviews
FOR EACH ROW
BEGIN
    IF NEW.Ratings NOT IN ('1', '2', '3', '4', '5')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Rating not 1-5';
    END IF;
END$

CREATE TRIGGER Update_Ratings_1_to_5 BEFORE UPDATE ON Reviews
FOR EACH ROW
BEGIN
    IF NEW.Ratings NOT IN ('1', '2', '3', '4', '5')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Rating not 1-5';
    END IF;
END$

#Disount Valid
CREATE TRIGGER Insert_Valid_Y_Or_N BEFORE INSERT ON Discount 
FOR EACH ROW
BEGIN
    IF NEW.Valid NOT IN ('Y', 'N')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Valid must be Y or N';
    END IF;
END$

CREATE TRIGGER Update_Valid_Y_Or_N BEFORE UPDATE ON Discount 
FOR EACH ROW
BEGIN
    IF NEW.Valid NOT IN ('Y', 'N')
    THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Valid must be Y or N';
    END IF;
END$
DELIMITER ;


#INSERTIONS
INSERT INTO	Person VALUES('368192', 'bob.builder@gmail.com', 'Bobby', '1998-11-30', '9179179170', '2018-11-23', 'N');
INSERT INTO	Person VALUES('251059', 'billy.cat@gmail.com', 'Billy', '1996-03-11', '9179179171', '2018-01-24', 'N');
INSERT INTO	Person VALUES('592134', 'sam.televi@gmail.com', 'James', '1992-05-14', '9179179172', '2017-09-01', 'N');
INSERT INTO	Person VALUES('845523', 'mars.nasa@gmail.com', 'Tenmond', '2001-11-25', '9179179173', '2017-03-26', 'Y');
INSERT INTO	Person VALUES('359803', 'plane.wire@gmail.com', 'Rayzin', '1967-10-12', '9179179174', '2018-01-27', 'Y');
INSERT INTO	Person VALUES('432591', 'thom.sanjr@gmail.com', 'Thomsan', '1912-02-07', '4545454545', '2015-05-15', 'Y');
INSERT INTO Person VALUES('1', 'gsingh@gmail.com', 'Gur Singh', '1999-01-20', '1234567890', '2019-05-01', 'Y');

INSERT INTO Customer VALUES('368192', 'password', 'N');
INSERT INTO Customer VALUES('251059', 'wordpass', 'N');
INSERT INTO Customer VALUES('592134', 'secretive', 'Y');

INSERT INTO Employee VALUES('432591', 'test@g.com', NULL, 'pass');
INSERT INTO Employee VALUES('845523', 'num2@g.com', 'test@g.com', 'pass');
INSERT INTO Employee VALUES('359803', 'some@g.com', NULL, 'pass');
INSERT INTO Employee VALUES('1', '1111@g.com', NULL, 'secure');

INSERT INTO Item VALUES('1233', '500', '123.00', 'IPhone X', 'Apple', 'A fancy phone', 'Phone');
INSERT INTO Item VALUES('18332', '90', '90.00', 'Soccer Ball', 'Tottenham', 'A ball that wins nothing', 'Sports');
INSERT INTO Item VALUES('81234', '200', '10.00', 'Diamond', 'PewDiePie', NULL, 'Gamnig');
INSERT INTO Item VALUES('1', '20', '50.00', 'Sweater', 'Adidas', 'A gray sweater that will keep you warm and stylish', 'Sweater');
INSERT INTO Item VALUES('2', '8', '80.00', 'Bayern Jersey', 'Adidas', 'A Bayern Munich home jersey from 2017-2018 season', 'Sports');
INSERT INTO Item VALUES('3', '5', '120.00', 'Soccer Cleets', 'Nike', 'Black and gold soccer cleets that are durable', 'Sports');
INSERT INTO Item VALUES('4', '30', '30.00', 'Jeans', 'Calvin Klein', 'Awesome light blue jeans from an awesome company', 'Pants');
INSERT INTO Item VALUES('5', '20', '40.00', 'Shirt', 'Nike', 'A nice white shirt with a black logo, just do it.', 'Shirt');
INSERT INTO Item VALUES('6', '3', '180.00', 'Ultra Boost', 'Adidas', 'Gray ultraboost that are good for running and style', 'Shoes');

INSERT INTO ShoppingCart VALUES('368192', '1233', '5');
INSERT INTO ShoppingCart VALUES('251059', '18332', '2');
INSERT INTO ShoppingCart VALUES('592134', '81234', '50');

INSERT INTO WishList VALUES('368192', '1233');
INSERT INTO WishList VALUES('251059', '18332');
INSERT INTO WishList VALUES('592134', '81234');

INSERT INTO Discount VALUES('7878', '0.10', 'Y');
INSERT INTO Discount VALUES('5454', '0.05', 'N');

INSERT INTO Orders VALUES('4444', '368192', '2018-11-25', 'Y', 'Bobby', 'bob.builder@gmail.com');
INSERT INTO Orders VALUES('21344', '251059', '2019-04-08', 'N', 'Billy', 'billy.cat@gmail.com');
INSERT INTO Orders VALUES('332', '592134', '2012-08-10', 'Y', 'NotJames', 'notjames@gmail.com');

INSERT INTO OrderedItems VALUES('4444', '1233', '5');
INSERT INTO OrderedItems VALUES('4444', '18332', '10');
INSERT INTO OrderedItems VALUES('21344', '18332', '10');
INSERT INTO OrderedItems VALUES('332', '18332', '20');

INSERT INTO Payment VALUES('4444', 'Bobby', '1234567891235674', 'Chase', '2018-11-25', 'First', 'Second', 'NY', 'USA', '11117');
INSERT INTO Payment VALUES('21344', 'Billy', '1234567891234567', 'MasterCard', '2018-11-25', 'One', 'Two', 'CAL', 'USA', '22222');
INSERT INTO Payment VALUES('332', 'James', '6123456789123456', 'Discover', '2018-11-25', 'First', 'Second', 'NY', 'USA', '33333');

INSERT INTO Shipment VALUES('4444', 'First', 'Second', 'NY', 'USA', '11117', '10', 'USPS', 'Bill1');
INSERT INTO Shipment VALUES('21344', 'Queens', 'City', 'NY', 'USA', '33633', '5', 'UPS', 'Bill2');
INSERT INTO Shipment VALUES('332', 'Sacremento', NULL, 'Cal', 'USA', '11117', '3', 'FEDEX', 'Bill');

INSERT INTO Returnment VALUES('4444', '1233', '4', 'Balls are broken', NULL);

INSERT INTO Reviews VALUES('368192', '1233', '2', 'It would not turn on');
INSERT INTO Reviews VALUES('592134', '18332', '5', 'It\'s pretty good');

#INSERT INTO Cards VALUES('7', 'Gurppp', '1111111111', 'VISA', '2020-11-25');
#INSERT INTO Cards VALUES('7', 'NotGurp', '1111111111', 'VISA', '2021-01-15');
