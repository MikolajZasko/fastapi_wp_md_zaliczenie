from fastapi import FastAPI, Request
from importlib.metadata import version
import json
import os
from pydantic import BaseModel

app = FastAPI()

STORAGE_FILE = "storage.json"

# helper function to load data from the JSON file
def load_storage() -> dict:
    if not os.path.exists(STORAGE_FILE):

        # return empty dict if file doesn't exist yet
        return {}  
    with open(STORAGE_FILE, "r") as f:
        try:
            # if works, return json contents
            return json.load(f)
        except json.JSONDecodeError:
            # if file is corrupted/empty, fallback to empty dict
            return {}  


# Helper function to save data back to the JSON file
def save_storage(data: dict):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.get("/")
def read_root():
    fastapi_version = version("fastapi")
    return {"fastapi_version": fastapi_version}

@app.get("/hello/{name}")
def read_root(name: str):
    return f"Hello {name}!"

@app.get("/query")
def read_root(request: Request):
    
    # convert to python dics
    params = dict(request.query_params)

    # create a result string
    result = ""

    for k ,v in params.items():
        result += f"'{k}' parameter with '{v}' value was queried. "

    return result

# define the class for input in POST /sum
class sum_list(BaseModel):
    list: list[int]

@app.post("/sum")
def sum_ints(sum_list: sum_list):

    # sum and return the result as a single int
    return sum(sum_list.list)