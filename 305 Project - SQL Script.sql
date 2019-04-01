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
    PRIMARY KEY(OrderNum));

CREATE TABLE Customer(
	CustomerID INT,
    Username VARCHAR(20),
    Userpass VARCHAR(20),
    PRIMARY KEY(CustomerID));
    
CREATE TABLE Employee(
	EmployeeID INT,
    DateJoined DATE,
    PRIMARY KEY(EmployeeID),
    FOREIGN KEY(Supervisor) REFERENCES Employee(EmployeeID));
