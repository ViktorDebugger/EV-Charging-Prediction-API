import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect

class Database:
    def __init__(self, db_path: str = "app/database/database.db"):
        self.db_path = db_path
        if os.path.exists(db_path):
            self.engine = create_engine(f'sqlite:///{self.db_path}')
            self.inspector = inspect(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        else:
            print("Database file does not exist!")
        
database = Database()