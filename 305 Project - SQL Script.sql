
CREATE TABLE Person(
	ID INT, #ID here is customer id since everyone will have cutomer account
	Email VARCHAR(30),
    Named VARCHAR(25),
    Dob DATE,
    Phone VARCHAR(10),
    Address VARCHAR(30),
    DateJoined DATE,
    IsEmployee CHAR(1),
    PRIMARY KEY(ID),
    CHECK (IsEmployee IN('Y', 'N')));

CREATE TABLE Customer(
	CustomerID INT,
    Username VARCHAR(20),
    Userpass VARCHAR(20),
    HasMembership CHAR(1),
    PRIMARY KEY(CustomerID),
    FOREIGN KEY(CustomerID) REFERENCES Person(ID) 
		ON DELETE CASCADE
        ON UPDATE CASCADE,
	CHECK (HasMembership IN('Y', 'N')));
    
CREATE TABLE Employee(
	ID INT,
	EmployeeID INT,
    Supervisor INT,
    PRIMARY KEY(EmployeeID),
    FOREIGN KEY(Supervisor) REFERENCES Employee(EmployeeID) 
		ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY(ID) REFERENCES Person(ID) 
		ON DELETE CASCADE 
        ON UPDATE CASCADE);
                
CREATE TABLE Item(
	ItemID INT,
    Quantity INT,
	Price DEC(9,2),
	ItemType VARCHAR(15),
	Seller VARCHAR(15),
	PRIMARY KEY(ItemID));

CREATE TABLE ShoppingCart(
	CustomerID INT,
    ItemID INT,
	Quantity INT,
	PRIMARY KEY(CustomerID, ItemID),
	FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID) 
		ON DELETE CASCADE
        ON UPDATE CASCADE,
	FOREIGN KEY(ItemID) REFERENCES Item(ItemID) 
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    CHECK (Quantity < Item.Quantity));

CREATE TABLE WishList(
	CustomerID INT,
    ItemID INT,
	PRIMARY KEY(CustomerID, ItemID),
	FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID) 
		ON DELETE CASCADE
        ON UPDATE CASCADE,
	FOREIGN KEY(ItemID) REFERENCES Item(ItemID) 
		ON DELETE CASCADE
        ON UPDATE CASCADE);

CREATE TABLE Orders(
	CustomerID INT,
	OrderNum INT,
    OrderDate DATE,
    Completed CHAR(1) DEFAULT 'N',
    PRIMARY KEY(OrderNum),
    FOREIGN KEY(CustomerID) REFERENCES Person(ID),
    CHECK (Completed IN('Y', 'N')));
                                                
CREATE TABLE Payment(
	OrderID INT,
	CardNum INT(16),
    CVS INT(3),
    CardType VarChar(10),
    CardExp DATE,
    PRIMARY KEY(OrderID),
    FOREIGN KEY(OrderID) REFERENCES Orders(OrderNum));

CREATE TABLE Shipment(
	OrderID INT,
	Address VarChar(30),
    Details VarChar(30),
    Fee INT,
    Company VarChar(10),
    PRIMARY KEY(OrderID),
    FOREIGN KEY(OrderID) REFERENCES Orders(OrderNum));
    
CREATE TABLE Returnment(
	OrderID INT,
    PRIMARY KEY(OrderID),
    FOREIGN KEY(OrderID) REFERENCES Orders(OrderNum));
                                            
CREATE TABLE Reviews(
	CustomerID INT,
	OrderID INT,
	Ratings INT,
	PRIMARY KEY(OrderID),
	FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY(OrderID) REFERENCES Orders(OrderNum));