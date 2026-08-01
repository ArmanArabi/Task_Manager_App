from fastapi import FastAPI, Depends, Request, status
from contextlib import asynccontextmanager
from task.routs import router as task_router
from users.routes import router as user_router
from auth.jwt import get_authenticated_user
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime , timedelta
from core.exceptions import setup_exception_handlers


# APSschedule
async def heartbeat_task():
    print(f"💓 Heartbeat: Server is alive at {datetime.now().strftime('%H:%M:%S')}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Application startup')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=heartbeat_task, trigger='interval', seconds=10)
    scheduler.start()
    yield
    scheduler.shutdown()
    print('Application shutdown')


app = FastAPI(
    title='todo application',
    description='this is a webapp to manage daily task',
    lifespan=lifespan
)


# add routers
app.include_router(task_router) #prefix="/api/v1" 
app.include_router(user_router)


# add middleware in future


#Error handeling 
setup_exception_handlers(app)


@app.get("/")
def root():
    return {"message": "Welcome to Arman's Todo App!"}

@app.get('/private')
def private_route(user=Depends(get_authenticated_user) ) :
    print(user.id)
    return {'this is a private route'}

