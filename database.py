import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

connection_string = f'postgresql+psycopg2://postgres.mlqbwnzpwfhsckdlnwia:{os.getenv("DB_PASSWORD")}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'

engine = create_engine(connection_string)

Session = sessionmaker(bind=engine)

def get_db():
    Base.metadata.create_all(bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()

'''Database Models are declared below.'''


from sqlalchemy import Column, Integer, String

class QuizData(Base):
    __tablename__='QuizData'
    quizID=Column(String,primary_key=True)
    ownerID=Column(String)
    totalAttempts=Column(Integer,default=0)
    topic=Column(String)
    syllabus=Column(String,default=None)
    number_of_questions=Column(Integer)

