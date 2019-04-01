CREATE TABLE Person(
	Email VARCHAR(30),
    Named VARCHAR(25),
    Dob DATE,
    Phone VARCHAR(10),
    Address VARCHAR(30),
    PRIMARY KEY(Email));
    
CREATE TABLE Orders(
	OrderNum INT,
    OrderDt DATE, 
    PRIMARY KEY(OrderNum)
    );
    
