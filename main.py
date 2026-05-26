from fastapi import FastAPI
import uvicorn
from database import engine, Base
from routers.users import router

app = FastAPI()
# class User(BaseModel):
#     name: str
#     age: int

app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Hello Anton Python Developer!"}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
