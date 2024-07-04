from fastapi import FastAPI

from src.routes import notes

app = FastAPI()

app.include_router(notes.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}
