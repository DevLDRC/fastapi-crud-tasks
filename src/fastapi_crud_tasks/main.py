from fastapi import FastAPI
from fastapi_crud_tasks.routes import auth, items
from fastapi_crud_tasks.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title='FastapiCrudTasks')

app.include_router(auth.route)
app.include_router(items.route)


@app.get("/")
def index():
    return {"Hello": "World"}
