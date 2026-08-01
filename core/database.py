from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from core.config import settings


#engine (connect to database)
print(f"DATABASE URL IS: {settings.SQLALCHEMY_DATABASE_URL}")

if settings.SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(url=settings.SQLALCHEMY_DATABASE_URL,
                           connect_args={'check_same_thread':False})
else:
    engine = create_engine(url=settings.SQLALCHEMY_DATABASE_URL)

#sessionlocal
sessionlocal = sessionmaker(bind=engine , autoflush=False , autocommit=False)

#create base
Base = declarative_base()

#access to db 
def get_db() :
    db = sessionlocal()
    try: 
        yield db
    finally: 
        db.close()    


