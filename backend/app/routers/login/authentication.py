from fastapi import APIRouter,HTTPException, Depends, status
from app.models.authen import UserBase,UserCreate,User
from app.routers.db.db_connection import connect_to_database
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi.middleware.cors import CORSMiddleware


router = APIRouter(
    prefix='/api/auth',
    tags=['Authentication'],
    responses={404: {
        'message': 'Not found'
    }}
)

connection, cursor = connect_to_database()
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Function to create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "your-secret-key", algorithm="HS256")
    return encoded_jwt
# User CRUD operations
@router.post("/users/", response_model=User)
def create_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    query = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
    values = (user.username, user.email, hashed_password)
    cursor.execute(query, values)
    connection.commit()
    user_id = cursor.lastrowid
    return {**user.dict(), "user_id": user_id}

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    query = "SELECT user_id, username, email FROM Users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    user_id, username, email = result
    return {"user_id": user_id, "username": username, "email": email}

# User authentication
@router.post("/login/")
def login(username: str, password: str):
    query = "SELECT user_id, password_hash FROM Users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if not result or not pwd_context.verify(password, result[1]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user_id, _ = result
    access_token  = create_access_token(data={"sub":user_id})
    return {"access_token": access_token, "token_type": "bearer"}

# User registration
@router.post("/register/", response_model=User)
def register(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    query = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
    values = (user.username, user.email, hashed_password)
    cursor.execute(query, values)
    connection.commit()
    user_id = cursor.lastrowid
    return {**user.dict(), "user_id": user_id}

