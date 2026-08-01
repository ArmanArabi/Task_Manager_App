import pytest
from core.database import create_engine, sessionmaker, get_db, Base
from sqlalchemy import StaticPool
from fastapi.testclient import TestClient
from main import app
from faker import Faker
from users.models import User_model, User_type
from task.models import Task_model
from auth.jwt import generate_access_token


SQLALCHEMY_DATABASE_URL ='sqlite:///:memory:'
print(f"DEBUG: DATABASE URL IS: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(url=SQLALCHEMY_DATABASE_URL , 
                       connect_args={'check_same_thread':False},
                       poolclass=StaticPool)

testsessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope='session')
def db_session():
    db = testsessionlocal()
    try: 
        yield db
    finally: 
        db.close()    
        

@pytest.fixture(scope='function', autouse=True)
def override_dependencies(db_session) :
    def get_test_db():
        yield db_session
    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope='session', autouse=True) 
def tear_up_down_db() :
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
        

@pytest.fixture(scope='function') 
def anon_client():
    client = TestClient(app)
    yield client


# in this client, build new client instead of use anon_client, because of  mutation risk !!!
@pytest.fixture(scope='function')
def auth_client(db_session) :
    client = TestClient(app)
    user = db_session.query(User_model).filter_by(username='test_user').one()
    access_token = generate_access_token(user_id = user.id)
    client.headers.update({'Authorization':f'Bearer {access_token} '})
    yield client   
    
@pytest.fixture(scope='session', autouse=True)
def generate_mock_data(db_session, tear_up_down_db):
    fake = Faker()
    user = User_model(username='test_user',
                      user_type=User_type.USER)
    user.set_password('Abcd#123')
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f'USER:{user.username}--- ID:{user.id} added')
    
    task_list = []
    for _ in range(10):
        task_list.append( 
            Task_model(
            title = fake.sentence(nb_words=10) ,
            description = fake.text() ,
            is_completed = fake.boolean() ,
            user_id = user.id
        ) )
    db_session.add_all(task_list)
    db_session.commit()
    print(f'added 10 task for user id:{user.id}')
     


@pytest.fixture(scope='function')
def random_task(db_session) :
    user = db_session.query(User_model).filter_by(username='test_user').one()
    task = db_session.query(Task_model).filter_by(user_id=user.id).first()
    return task