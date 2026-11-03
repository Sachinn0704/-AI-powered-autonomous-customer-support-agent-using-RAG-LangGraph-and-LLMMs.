import database
import models

def create_tables():
    database.Base.metadata.create_all(bind=database.engine)
    print("ResolveAI database tables created successfully!")

if __name__ == "__main__":
    create_tables()