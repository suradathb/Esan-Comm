from fastapi import APIRouter,HTTPException, Depends, status
from app.routers.db.db_posconnect import connect_to_database
from app.models.posesan_model import Branch,Product,BranchProduct,Table,BranchTable,User,UserCreate,UserLogin,Customer,Order,OrderItem,Payment,Receipt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from typing import List



router = APIRouter(
    prefix='/api/pos',
    tags=['POS Esan Software'],
    responses={404: {
        'message': 'Not found'
    }}
)
# Sample database (replace with your database logic)
users_db = {
    1: {
        "UserID": 1,
        "Username": "admin",
        "Password": "password",  # Password should be hashed, this is just for demonstration
        "Role": "admin"
    }
}
# Dependency for database connection
connection, cursor = connect_to_database()
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Token expiration time
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Function to create access token
# Function to get current user from JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to get user by username
def get_user(username: str):
    for user in users_db.values():
        if user["Username"] == username:
            return user
    return None

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["Password"]):
        return False
    return user

# CRUD Operations for Users
# Endpoint to create a new user
@router.post("/users/")
async def create_user(user: UserCreate):
    if not connection or not cursor:
        raise HTTPException(status_code=500, detail="Database connection error")

    # Insert the new user into the Users table
    query = "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)"
    values = (user.Username, user.Password, user.Role)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print("User created successfully")
        return {"message": "User created successfully"}
    except connection.Error as error:
        print("Error creating user:", error)
        raise HTTPException(status_code=500, detail="Error creating user")
    finally:
        cursor.close()
        connection.close()

@router.get("/users/", response_model=List[User])
async def read_users():
    query = "SELECT * FROM Users"
    cursor.execute(query)
    users = cursor.fetchall()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    # Convert the tuple results to dictionaries
    user_list = []
    for user in users:
        user_dict = {
            "UserID": user[0],
            "Username": user[1],
            "Password": user[2],
            "Role": user[3]
        }
        user_list.append(user_dict)

    return user_list

# Endpoint to update a user by ID
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    if not connection or not cursor:
        raise HTTPException(status_code=500, detail="Database connection error")

    # Update the user in the Users table
    query = "UPDATE Users SET Username = %s, Password = %s, Role = %s WHERE UserID = %s"
    values = (user.Username, user.Password, user.Role, user_id)

    try:
        cursor.execute(query, values)
        connection.commit()
        print("User updated successfully")
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {**user.dict(), "UserID": user_id}
    except connection.Error as error:
        print("Error updating user:", error)
        raise HTTPException(status_code=500, detail="Error updating user")
    finally:
        cursor.close()
        connection.close()

# Endpoint to delete a user by ID
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # Connect to the database
    connection, cursor = connect_to_database()
    
    if not connection or not cursor:
        raise HTTPException(status_code=500, detail="Database connection error")

    # Delete the user from the Users table
    query = "DELETE FROM Users WHERE UserID = %s"
    values = (user_id,)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print("User deleted successfully")
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except connection.Error as error:
        print("Error deleting user:", error)
        raise HTTPException(status_code=500, detail="Error deleting user")
    finally:
        cursor.close()
        connection.close()

# Token creation helper
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# API route for user login and token creation
@router.post("/login", response_model=User)
async def login_for_access_token(user: UserLogin):
    authenticated_user = authenticate_user(user.Username, user.Password)
    if not authenticated_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.Username}, expires_delta=access_token_expires)
    return {"UserID": authenticated_user["UserID"], "Username": authenticated_user["Username"], "Role": authenticated_user["Role"], "access_token": access_token, "token_type": "bearer"}

# Example of an authenticated API route
@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Endpoint for user login
@router.post("/login/")
async def user_login(user: UserLogin):
    # Connect to the database
    connection, cursor = connect_to_database()
    
    if not connection or not cursor:
        raise HTTPException(status_code=500, detail="Database connection error")

    # Check if the user exists and the password matches
    query = "SELECT * FROM Users WHERE Username = %s AND Password = %s"
    values = (user.Username, user.Password)
    
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except connection.Error as error:
        print("Error during login:", error)
        raise HTTPException(status_code=500, detail="Error during login")
    finally:
        cursor.close()
        connection.close()

# # CRUD Operations for Customers
# @router.post("/customers/")
# async def create_customer(customer: Customer, db = Depends(connect_to_database)):
#     query = "INSERT INTO Customers (CustomerName, CustomerType) VALUES (?, ?)"
#     values = (customer.CustomerName, customer.CustomerType)
#     db.execute(query, values)
#     db.commit()
#     return {"message": "Customer created successfully"}

# @router.get("/customers/", response_model=List[Customer])
# async def read_customers(db = Depends(connect_to_database)):
#     query = "SELECT * FROM Customers"
#     return db.fetch_all(query)

# # CRUD Operations for Products
# @router.post("/products/")
# async def create_product(product: Product, db = Depends(connect_to_database)):
#     query = "INSERT INTO Products (ProductName, Description, Price) VALUES (?, ?, ?)"
#     values = (product.ProductName, product.Description, product.Price)
#     db.execute(query, values)
#     db.commit()
#     return {"message": "Product created successfully"}

# @router.get("/products/", response_model=List[Product])
# async def read_products(db = Depends(connect_to_database)):
#     query = "SELECT * FROM Products"
#     return db.fetch_all(query)

# # CRUD Operations for Orders
# @router.post("/orders/")
# async def create_order(order: Order, db = Depends(connect_to_database)):
#     query = "INSERT INTO Orders (BranchID, UserID, CustomerID, TableID, OrderDate, TotalAmount, OrderType) VALUES (?, ?, ?, ?, ?, ?, ?)"
#     values = (order.BranchID, order.UserID, order.CustomerID, order.TableID, order.OrderDate, order.TotalAmount, order.OrderType)
#     db.execute(query, values)
#     db.commit()
#     return {"message": "Order created successfully"}

# @router.get("/orders/", response_model=List[Order])
# async def read_orders(db = Depends(connect_to_database)):
#     query = "SELECT * FROM Orders"
#     return db.fetch_all(query)

# # CRUD Operations for Order Items
# @router.post("/orderitems/")
# async def create_order_item(order_item: OrderItem, db = Depends(connect_to_database)):
#     query = "INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price) VALUES (?, ?, ?, ?)"
#     values = (order_item.OrderID, order_item.ProductID, order_item.Quantity, order_item.Price)
#     db.execute(query, values)
#     db.commit()
#     return {"message": "Order item created successfully"}

# @router.get("/orderitems/", response_model=List[OrderItem])
# async def read_order_items(db = Depends(connect_to_database)):
#     query = "SELECT * FROM OrderItems"
#     return db.fetch_all(query)

# # CRUD Operations for Payments
# @router.post("/payments/")
# async def create_payment(payment: Payment, db = Depends(connect_to_database)):
#     query = "INSERT INTO Payments (OrderID, PaymentDate, Amount, PaymentMethod) VALUES (?, ?, ?, ?)"
#     values = (payment.OrderID, payment.PaymentDate, payment.Amount, payment.PaymentMethod)
#     db.execute(query, values)
#     db.commit()
#     return {"message": "Payment created successfully"}

# @router.get("/payments/", response_model=List[Payment])
# async def read_payments(db = Depends(connect_to_database)):
#     query = "SELECT * FROM Payments"
#     return db.fetch_all(query)

# # CRUD Operations for Receipts
# @router.post("/receipts/")
# async def create_receipt(receipt: Receipt, db = Depends(connect_to_database)):
#     query = "INSERT INTO Receipts (OrderID, ReceiptDate, ReceiptContent) VALUES (?, ?, ?)"
#     values = (receipt.OrderID, receipt.ReceiptDate, receipt.ReceiptContent)
#     db.execute(query, values)
#     db.commit()
#     return {"message": "Receipt created successfully"}

# @router.get("/receipts/", response_model=List[Receipt])
# async def read_receipts(db = Depends(connect_to_database)):
#     query = "SELECT * FROM Receipts"
#     return db.fetch_all(query)

# # CRUD Operations for Branches
# @router.post("/branches/")
# async def create_branch(branch: Branch, db = Depends(connect_to_database)):
#     query = "INSERT INTO Branches (BranchName, Location, ManagerName) VALUES (?, ?, ?)"
#     values = (branch.BranchName, branch.Location, branch.ManagerName)
#     db.execute(query, values)
#     db.commit()
#     return {"message": "Branch created successfully"}

# @router.get("/branches/", response_model=List[Branch])
# async def read_branches(db = Depends(connect_to_database)):
#     query = "SELECT * FROM Branches"
#     return db.fetch_all(query)

# # Similarly, implement CRUD operations for other tables: BranchProducts, BranchTables