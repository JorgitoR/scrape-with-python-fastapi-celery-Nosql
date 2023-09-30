from fastapi import FastAPI

from . import (config)

settings = config.get_setting()


app = FastAPI()

@app.get("/")
def read_index():
    return "Hello world 2"


"""
>> uvicorn app.main:app --reload
"""