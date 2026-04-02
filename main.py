from fastapi import FastAPI

app = FastAPI()


@app.run("/")
def greet():
    return ("Hello")

