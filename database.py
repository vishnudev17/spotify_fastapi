from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = "postgresql://musicapp:Palnar123@localhost:5432/fluttermusicapp"
DATABASE_URL = "postgresql://fastapi_spotify_db_user:SM5coznnzgqRvkZV7paBqOPaBDb2Do32@dpg-d20skbh5pdvs739db7kg-a.oregon-postgres.render.com/fastapi_spotify_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
