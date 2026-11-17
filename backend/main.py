from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, model_validator
from .engine import DECK,simulate,calculate_ev

ROOT=Path(__file__).resolve().parent.parent
app=FastAPI(title='Poker AI Pro Advanced V1',version='1.0.0')
app.mount('/static',StaticFiles(directory=ROOT/'frontend'),name='static')

class Request(BaseModel):
    hero:list[str]
    board:list[str]=Field(default_factory=list)
    ranges:list[str]=Field(default_factory=lambda:['random'])
    pot:float=Field(ge=0,default=0)
    call:float=Field(ge=0,default=0)
    iterations:int=Field(ge=100,le=20000,default=2000)
    seed:int|None=None
    @model_validator(mode='after')
    def validate_state(self):
        if len(self.hero)!=2 or len(self.board) not in (0,3,4,5):raise ValueError('Hero needs 2 cards; board must have 0, 3, 4, or 5 cards')
        cards=self.hero+self.board
        if any(c not in DECK for c in cards) or len(set(cards))!=len(cards):raise ValueError('Cards must be valid and unique')
        if not 1<=len(self.ranges)<=8:raise ValueError('Provide 1–8 opponents for a 9-handed table')
        return self

@app.get('/')
def index():return FileResponse(ROOT/'frontend'/'index.html')

@app.post('/api/analyze')
def analyze(req:Request):
    try:
        sim=simulate(req.hero,req.board,req.ranges,req.iterations,req.seed)
        ev=calculate_ev(sim['equity'],req.pot,req.call)
        return {'simulation':sim,'ev':ev,'opponents':len(req.ranges),'disclaimer':'Equity simulation and simplified EV, not a GTO solver or guaranteed winning recommendation.'}
    except ValueError as exc:raise HTTPException(status_code=422,detail=str(exc))
