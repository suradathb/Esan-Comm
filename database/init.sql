-- Pos EsanSoftware
USE esanposdb

CREATE TABLE Branches (
    BranchID INT AUTO_INCREMENT PRIMARY KEY,
    BranchName VARCHAR(255),
    Location VARCHAR(255),
    ManagerName VARCHAR(255)
);

CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255),
    Description TEXT,
    Price DECIMAL(10, 2)
);

CREATE TABLE BranchProducts (
    BranchProductID INT AUTO_INCREMENT PRIMARY KEY,
    BranchID INT,
    ProductID INT,
    FOREIGN KEY (BranchID) REFERENCES Branches(BranchID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Tables (
    TableID INT AUTO_INCREMENT PRIMARY KEY,
    TableName VARCHAR(255),
    TableStatus VARCHAR(50)
);

CREATE TABLE BranchTables (
    BranchTableID INT AUTO_INCREMENT PRIMARY KEY,
    BranchID INT,
    TableID INT,
    FOREIGN KEY (BranchID) REFERENCES Branches(BranchID),
    FOREIGN KEY (TableID) REFERENCES Tables(TableID)
);
-- Create Users table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255),
    Password VARCHAR(255),
    Role VARCHAR(50)
);
-- Create Customers table
CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerName VARCHAR(255),
    CustomerType VARCHAR(50)
);
CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    BranchID INT,
    UserID INT,
    CustomerID INT,
    TableID INT,
    OrderDate DATETIME,
    TotalAmount DECIMAL(10, 2),
    OrderType VARCHAR(50),
    FOREIGN KEY (BranchID) REFERENCES Branches(BranchID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (TableID) REFERENCES Tables(TableID)
);

CREATE TABLE OrderItems (
    OrderItemID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    Price DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    PaymentDate DATETIME,
    Amount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

CREATE TABLE Receipts (
    ReceiptID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ReceiptDate DATETIME,
    ReceiptContent TEXT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- Insert sample data into Users table
INSERT INTO Users (Username, Password, Role) VALUES
('user1', 'password1', 'Staff'),
('user2', 'password2', 'Manager');

-- Insert sample data into Customers table
INSERT INTO Customers (CustomerName, CustomerType) VALUES
('Customer A', 'Regular'),
('Customer B', 'VIP');

-- 1 Insert Sample Branches:
INSERT INTO Branches (BranchName, Location, ManagerName) VALUES
('Branch A', 'Location A', 'Manager A'),
('Branch B', 'Location B', 'Manager B');
-- 2 Insert Sample Products:
INSERT INTO Products (ProductName, Description, Price) VALUES
('Product A', 'Description of Product A', 10.99),
('Product B', 'Description of Product B', 15.99),
('Product C', 'Description of Product C', 20.99);

-- 3 Associate Products with Branches:
-- For Branch A
INSERT INTO BranchProducts (BranchID, ProductID) VALUES
(1, 1), -- Product A
(1, 2); -- Product B

-- For Branch B
INSERT INTO BranchProducts (BranchID, ProductID) VALUES
(2, 2), -- Product B
(2, 3); -- Product C

-- 4 Insert Sample Tables:
INSERT INTO Tables (TableName, TableStatus) VALUES
('Table 1', 'Available'),
('Table 2', 'Occupied');

-- 5 Associate Tables with Branches:
-- For Branch A
INSERT INTO BranchTables (BranchID, TableID) VALUES
(1, 1), -- Table 1
(1, 2); -- Table 2

-- For Branch B
INSERT INTO BranchTables (BranchID, TableID) VALUES
(2, 1); -- Table 1


-- 6 Insert Sample Customers:
INSERT INTO Customers (CustomerName, CustomerType) VALUES
('Customer 1', 'Regular'),
('Customer 2', 'VIP');

-- 7 Insert Sample Users:
INSERT INTO Users (Username, Password, Role) VALUES
('User A', 'password', 'Staff'),
('User B', 'password', 'Manager');

-- 8 Insert Sample Orders:
INSERT INTO Orders (BranchID, UserID, CustomerID, TableID, OrderDate, TotalAmount, OrderType) VALUES
(1, 1, 1, 1, '2024-02-12 10:00:00', 26.98, 'Dine-in'),
(2, 2, 2, 1, '2024-02-12 11:00:00', 36.98, 'Takeaway');

-- 9 Insert Sample Order Items:
-- For Order 1 (Branch A)
INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price) VALUES
(1, 1, 2, 21.98), -- Product A x2
(1, 2, 1, 5.00);   -- Product B x1

-- For Order 2 (Branch B)
INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price) VALUES
(2, 2, 2, 31.98), -- Product B x2
(2, 3, 1, 5.00);   -- Product C x1

-- 10  Insert Sample Payments:
INSERT INTO Payments (OrderID, PaymentDate, Amount, PaymentMethod) VALUES
(1, '2024-02-12 10:30:00', 26.98, 'Cash'),
(2, '2024-02-12 11:30:00', 36.98, 'Card');

-- 11 Insert Sample Receipts:
INSERT INTO Receipts (OrderID, ReceiptDate, ReceiptContent) VALUES
(1, '2024-02-12 10:45:00', 'Receipt content for Order 1'),
(2, '2024-02-12 11:45:00', 'Receipt content for Order 2');
