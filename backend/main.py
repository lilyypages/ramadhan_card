import os
from fastapi import FastAPI
from sqlalchemy import create_backend, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ambil URL Database dari Environment Variable
DATABASE_URL = os.getenv("DATABASE_URL") # Link dari Neon.tech tadi

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabel Pesan
class WishDB(Base):
    __tablename__ = "wishes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    message = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/wishes")
def post_wish(wish: Wish):
    db = SessionLocal()
    new_wish = WishDB(name=wish.name, message=wish.message)
    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)
    return new_wish