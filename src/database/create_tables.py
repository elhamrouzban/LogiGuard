from src.database.connection import Base, engine
from src.database.orm_models import Order, Prediction


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")