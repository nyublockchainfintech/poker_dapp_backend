from fastapi import FastAPI
from test_pokerlib import MyTable
from pokerlib import PlayerSeats
import json

#TO START A SERVER WITH POETRY: poetry run python -m uvicorn dummy:app --reload

app = FastAPI()

gameStates = [] 

def update_game_state(currTable):
    currTableJson = json.dumps(currTable.__dict__)
    gameStates.append(currTableJson)


## test 
table = MyTable(
    _id=0,
    seats=PlayerSeats([None] * 9),
    buyin=100,
    small_blind=5,
    big_blind=10,
)

update_game_state(table)

@app.get("/")
async def read_game_state(skip: int = 0, limit: int = 2):
    return gameStates[skip : skip + limit]