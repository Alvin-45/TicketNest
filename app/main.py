# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from app.database import SessionLocal
# from app.models import User
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# class UserCreate(BaseModel):
#     name: str
#     email: str

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/register/")
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     # Check if the user already exists
#     existing_user = db.query(User).filter(User.name == user.name).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")
    
#     # Create a new user
#     db_user = User(name=user.name, email=user.email,password=user.password)
#     db.add(db_user)
#     db.commit()  
#     db.refresh(db_user)  
    
#     return {"name": db_user.name, "email": db_user.email}

# @app.get("/users/")
# async def get_users(db: Session = Depends(get_db)):
#     users = db.query(User).all()  # Fetch all users from the database
#     return [{"name": user.name, "email": user.email,"password":user.password} for user in users]

# @app.get("/login")
# async def login_user(email: str,password:str, db: Session = Depends(get_db)):
#    user = db.query(User).filter(User.email == email, User.password == password).first()
#  if user:
#         return {"name": user.name, "email": user.email}
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

# # class UserLoginRequest(BaseModel):
# #     email: str

# # @app.post("/login/")
# # async def login_user(request: UserLoginRequest, db: Session = Depends(get_db)):
# #     user = db.query(User).filter(User.email == request.email).first()

# #     if user:
# #         return {"name": user.name, "email": user.email}
# #     else:
# #         raise HTTPException(status_code=404, detail="User not found")

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import User
from fastapi.middleware.cors import CORSMiddleware
from app.models import Movie  # Ensure this import is present
from app.models import Seat  # Adjust the path according to your project structure


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class UserCreate(BaseModel):
    name: str
    email: str
    password: str  # Added password to the model

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create a new user
    db_user = User(name=user.name, email=user.email, password=user.password)  # Make sure to include the password
    db.add(db_user)
    db.commit()  
    db.refresh(db_user)  
    
    return {"name": db_user.name, "email": db_user.email}

@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  # Fetch all users from the database
    return [{"name": user.name, "email": user.email, "password": user.password} for user in users]

@app.get("/login")
async def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.password == password).first()  # Corrected filter

    if user:
        return {"name": user.name, "email": user.email}
    else:
        raise HTTPException(status_code=404, detail="User not found")

class SeatBookingRequest(BaseModel):
    emailid: str
    movie_name:str
    seatnumber: int  # List of seat status ("available", "selected", "booked")

@app.post("/book-seats/")
async def book_seats(request: SeatBookingRequest, db: Session = Depends(get_db)):
    # Check if the movie exists
    movie = db.query(Movie).filter(Movie.movie_name == request.movie_name).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Loop through the requested seats and check if they are already booked
    # for seatnumber in request.seatnumber:
        seat = db.query(Seat).filter(Seat.movie_name == request.movie_name, Seat.seatnumber == request.seatnumber).first()
        
        # If seat exists and already booked, raise an error
        if seat and seat.emailid:
            raise HTTPException(status_code=400, detail=f"Seat {seat_number} is already booked for this movie")
        
        # If seat does not exist, create a new seat for booking
        if not seat:
            seat = Seat(
                movie_name="got",
                seatnumber=request.seatnumber,
                emailid=request.emailid,  # Assign the user's email to the seat
                status="booked"
            )
            db.add(seat)
    print("Commit successful")
    # Commit the transaction to save new bookings to the database
    db.commit()
    


    return {"message": "Seats successfully booked", "seatnumber": request.seatnumber,"success":True}

    