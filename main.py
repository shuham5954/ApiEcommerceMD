from fastapi import FastAPI
from routes import logIn
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware  # Make sure

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:4200",  # Specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(logIn.router)

