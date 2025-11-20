from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/product_app"

engine = create_engine(
    DATABASE_URL,
    echo=True,             # optional: prints SQL statements
    pool_pre_ping=True     # keeps connection alive
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
