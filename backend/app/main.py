from app import errors
from fastapi import FastAPI
import uvicorn


def create_app() -> FastAPI:
    app = FastAPI()
    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=10000)
