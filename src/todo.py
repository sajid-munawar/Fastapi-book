from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

from fastapi import FastAPI, Depends
from typing import Annotated

DB_URL = "postgresql://neondb_owner:dn9UwfKZeIq2@ep-wandering-king-a5g0m4ci.us-east-2.aws.neon.tech/neondb?sslmode=require"


class Base(DeclarativeBase):
  pass

class Todos(Base):
  __tablename__='todos'
  id:Mapped[int] = mapped_column(primary_key=True)
  title:Mapped[str] = mapped_column(String(200))
  is_completed:Mapped[bool] = mapped_column(default=False)

# Enable connection pooling with pessimistic testing
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Exception occurred: {e}")
    finally:
        db.close()

app = FastAPI()

@app.get("/hello")
def add_data(db: Annotated[Session, Depends(get_db)]):

    # Now you can use db as a session object to query the database and do other operations
    # i.e: db.query(User).filter(User.name == "test").first() where User is a SQLAlchemy ORM model

    return {"message": "Hello from FastAPI with SQLAlchemy DB Injection"}
  
@app.get("/todos")
def get_todos(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(Todos).all()
    return {"todos": todos}
  
@app.post("/todos")
def create_todo(title: str, db: Annotated[Session, Depends(get_db)]):
    todo = Todos(title=title)
    db.add(todo)
    db.commit()
    return {"todo": todo}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}

@app.patch("/todos/{todo_id}")
def update_todo(todo_id: int, title: str, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    todo.title = title
    db.commit()
    return {"todo": todo}