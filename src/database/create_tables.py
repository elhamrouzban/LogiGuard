
from src.database.connection import Base, engine
from src.database import orm_models  # noqa: F401


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")
