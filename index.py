# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float, Table, JSON
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship

# DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"

# # Initialize FastAPI
# app = FastAPI()

# # Database setup
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# # Models
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password_hash = Column(String, nullable=False)


# class Screen(Base):
#     __tablename__ = "screens"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     poster_url = Column(String, nullable=True)
#     num_seats = Column(Integer, nullable=False)


# class ScreenLayout(Base):
#     __tablename__ = "screen_layouts"
#     id = Column(Integer, primary_key=True, index=True)
#     screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
#     row = Column(String, nullable=False)
#     column = Column(Integer, nullable=False)
#     is_vip = Column(Boolean, default=False)
#     screen = relationship("Screen", back_populates="layouts")


# Screen.layouts = relationship("ScreenLayout", back_populates="screen")


# class Booking(Base):
#     __tablename__ = "bookings"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
#     movie_id = Column(Integer, nullable=False)
#     seats = Column(JSON, nullable=False)  # Stores an array of seat numbers
#     total_price = Column(Float, nullable=False)
#     user = relationship("User")
#     screen = relationship("Screen")


# # Create all tables
# Base.metadata.create_all(bind=engine)


# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # FastAPI Endpoints
# @app.post("/users/")
# def create_user(user: dict, db: SessionLocal = Depends(get_db)):
#     new_user = User(
#         name=user["name"],
#         email=user["email"],
#         password_hash=user["password_hash"],
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.post("/screens/")
# def create_screen(screen: dict, db: SessionLocal = Depends(get_db)):
#     new_screen = Screen(
#         name=screen["name"],
#         poster_url=screen.get("poster_url"),
#         num_seats=screen["num_seats"],
#     )
#     db.add(new_screen)
#     db.commit()
#     db.refresh(new_screen)
#     return new_screen


# @app.post("/screen_layouts/")
# def create_screen_layout(layout: dict, db: SessionLocal = Depends(get_db)):
#     new_layout = ScreenLayout(
#         screen_id=layout["screen_id"],
#         row=layout["row"],
#         column=layout["column"],
#         is_vip=layout.get("is_vip", False),
#     )
#     db.add(new_layout)
#     db.commit()
#     db.refresh(new_layout)
#     return new_layout


# @app.post("/bookings/")
# def create_booking(booking: dict, db: SessionLocal = Depends(get_db)):
#     total_price = calculate_price(booking["seats"])
#     new_booking = Booking(
#         user_id=booking["user_id"],
#         screen_id=booking["screen_id"],
#         movie_id=booking["movie_id"],
#         seats=booking["seats"],
#         total_price=total_price,
#     )
#     db.add(new_booking)
#     db.commit()
#     db.refresh(new_booking)
#     return new_booking


# def calculate_price(seats):
#     # Example: Assume regular seats cost $10, VIP seats cost $20
#     return len(seats) * 10  # Adjust pricing logic if needed


# # Run the server using Uvicorn
# # Command: uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
