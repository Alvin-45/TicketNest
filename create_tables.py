from app.database import engine
from app.models import Base  # Import the Base object that contains all models

# Create all tables defined in the models
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
