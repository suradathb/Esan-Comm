from pydantic import BaseModel
from typing import List

class Branch(BaseModel):
    BranchID: int
    BranchName: str
    Location: str
    ManagerName: str

class Product(BaseModel):
    ProductID: int
    ProductName: str
    Description: str
    Price: float

class BranchProduct(BaseModel):
    BranchProductID: int
    BranchID: int
    ProductID: int

class Table(BaseModel):
    TableID: int
    TableName: str
    TableStatus: str

class BranchTable(BaseModel):
    BranchTableID: int
    BranchID: int
    TableID: int

class User(BaseModel):
    UserID: int
    Username: str
    Password: str
    Role: str

class UserCreate(BaseModel):
    Username: str
    Password: str
    Role: str

class UserInDB(User):
    Password: str
    
class UserLogin(BaseModel):
    Username: str
    Password: str

class Customer(BaseModel):
    CustomerID: int
    CustomerName: str
    CustomerType: str

class Order(BaseModel):
    OrderID: int
    BranchID: int
    UserID: int
    CustomerID: int
    TableID: int
    OrderDate: str
    TotalAmount: float
    OrderType: str

class OrderItem(BaseModel):
    OrderItemID: int
    OrderID: int
    ProductID: int
    Quantity: int
    Price: float

class Payment(BaseModel):
    PaymentID: int
    OrderID: int
    PaymentDate: str
    Amount: float
    PaymentMethod: str

class Receipt(BaseModel):
    ReceiptID: int
    OrderID: int
    ReceiptDate: str
    ReceiptContent: str
