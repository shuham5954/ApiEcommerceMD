from fastapi import FastAPI
from routes import logIn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(logIn.router)

