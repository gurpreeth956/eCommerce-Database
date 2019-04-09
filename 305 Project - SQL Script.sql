
#TABLETION

CREATE TABLE Person (
    ID INT,
    Email VARCHAR(30) NOT NULL,
    Named VARCHAR(25) NOT NULL,
    Dob DATE NOT NULL,
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
        ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (HasMembership IN ('Y' , 'N'))
);
    
CREATE TABLE Employee (
    ID INT,
    EmployeeID INT,
    Supervisor INT,
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (Supervisor)
        REFERENCES Employee (EmployeeID)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (ID)
        REFERENCES Person (ID)
        ON DELETE CASCADE ON UPDATE CASCADE
);
                
CREATE TABLE Item (
    ItemID INT,
    Quantity INT NOT NULL,
    Price DEC(9 , 2 ) NOT NULL,
    ItemType VARCHAR(15) NOT NULL,
    Seller VARCHAR(15) NOT NULL,
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
        ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (Quantity < Item.Quantity)
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
    CustomerID INT,
    OrderNum INT NOT NULL,
    OrderDate DATE NOT NULL,
    Completed CHAR(1) DEFAULT 'N',
    PRIMARY KEY (OrderNum),
    FOREIGN KEY (CustomerID)
        REFERENCES Person (ID),
    CHECK (Completed IN ('Y' , 'N'))
);

CREATE TABLE Payment (
    OrderID INT,
    CardNum INT(16) NOT NULL,
    CVS INT(3) NOT NULL,
    CardType VARCHAR(10) NOT NULL,
    CardExp DATE NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID)
        REFERENCES Orders (OrderNum)
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
);
    
CREATE TABLE Returnment (
    OrderID INT,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID)
        REFERENCES Orders (OrderNum)
);
                
CREATE TABLE Reviews (
    CustomerID INT,
    OrderID INT,
    Ratings INT NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (CustomerID)
        REFERENCES Customer (CustomerID),
    FOREIGN KEY (OrderID)
        REFERENCES Orders (OrderNum)
);

#INSERTIONS
INSERT INTO	Person VALUES('368192', 'bob.builder@gmail.com', 'Bobby', '1998-11-30', '9179179170', 'Linden', '2018-11-23', 'N');
INSERT INTO	Person VALUES('251059', 'billy.cat@gmail.com', 'Billy', '1996-03-11', '9179179171', 'Queens', '2018-01-24', 'N');
INSERT INTO	Person VALUES('592134', 'sam.televi@gmail.com', 'James', '1992-05-14', '9179179172', 'Ithaca', '2017-09-01', 'N');
INSERT INTO	Person VALUES('845523', 'mars.nasa@gmail.com', 'Tenmond', '2001-11-25', '9179179173', 'Stony', '2017-03-26', 'Y');
INSERT INTO	Person VALUES('359803', 'plane.wire@gmail.com', 'Rayzin', '1967-10-12', '9179179174', 'Ithaca', '2018-01-27', 'Y');
INSERT INTO	Person VALUES('432591', 'thom.sanjr@gmail.com', 'Thomsan', '1912-02-07', '4545454545', 'Hurst', '2015-05-15', 'Y')