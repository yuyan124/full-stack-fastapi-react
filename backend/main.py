import uvicorn
from app import create_app
from app.providers.log import init_logging

# logger = init_logging()
app = create_app()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=10000)
