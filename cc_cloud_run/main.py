from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from typing import Annotated
import datetime

app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/template")

# init firestore client
db = firestore.Client()
votes_collection = db.collection("votes")


@app.get("/")
async def read_root(request: Request):
    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

    # stream all votes; count tabs / spaces votes, and get recent votes
    # Retrieve all votes from Firestore
    votes = votes_collection.stream()
    vote_data = [v.to_dict() for v in votes]
    
    # Counting votes
    tabs_count = sum(1 for v in vote_data if v.get("team") == "TABS")
    spaces_count = sum(1 for v in vote_data if v.get("team") == "SPACES")
    
    # Sorting votes
    recent_votes = sorted(vote_data, key=lambda x: x.get("time_cast", ""), reverse=True)[:5]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "tabs_count": tabs_count,
        "spaces_count": spaces_count,
        "recent_votes": recent_votes
    })


@app.post("/")
async def create_vote(team: Annotated[str, Form()]):
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")

    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

    # create a new vote document in firestore
    votes_collection.add({
        "team": team,
        "time_cast": datetime.datetime.utcnow().isoformat()
    })
    
    return {"detail": "Vote recorded successfully!"}

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================