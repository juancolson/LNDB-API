import json

from Main.searcher import find_light_novel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Main.detail import get_detail

application = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "http://knightshrestha.unaux.com",
]

application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@application.get("/search/{Search}")
async def light_novel_search(Search):
    if Search is not None:
        result_list = find_light_novel(Search)
        return result_list
    
@application.get("/detail/{Detail}")
async def light_novel_search(Detail):
    if Detail is not None:
        result = get_detail(Detail)
        return result
    