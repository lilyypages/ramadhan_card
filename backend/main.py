import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Ambil URL Database dari Environment Variable (Nanti kita setting)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabel di Database
class WishDB(Base):
    __tablename__ = "wishes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    message = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Backend Lebaran Aktif! Cek /docs untuk API"}
    
# Middleware CORS agar Vercel bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class WishSchema(BaseModel):
    name: str
    message: str

# Ambil data
@app.get("/api/wishes")
def get_wishes():
    db = SessionLocal()
    wishes = db.query(WishDB).order_by(WishDB.id.desc()).all()
    db.close()
    return wishes

# Simpan data
@app.post("/api/wishes")
def post_wish(wish: WishSchema):
    db = SessionLocal()
    new_wish = WishDB(name=wish.name, message=wish.message)
    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)
    db.close()
    return new_wish

# Port khusus Hugging Face
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)