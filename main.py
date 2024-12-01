import os
import uvicorn
from fastapi import FastAPI, Depends

from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    insert,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session

DB_URL = "postgresql+psycopg://" + os.environ['DB_URL']

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/items")
def get_items(
    db: Session = Depends(get_db),
) -> list[str]:
    return [x.title for x in db.query(Books).all()]


@app.get("/add_item")
def hello(
    title: str,
    db: Session = Depends(get_db),
) -> str:
    q = insert(Books).values(title=title)
    db.execute(q)
    db.commit()
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
