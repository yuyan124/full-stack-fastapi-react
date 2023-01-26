import uvicorn
from app import carete_app

app = carete_app()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=10000, debug=True)
