from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from src.database import get_db
from src.classes.poll import Poll
from src.classes.poll_option import PollOption
from src.classes.vote import Vote
from src.controllers.polls import PollCtrl
from src.controllers.votes import VoteCtrl
from src.api.authorization import get_current_user


router = APIRouter()


class PollOptionOut(BaseModel):
    option_id: str
    option_text: str
    votes: int


class PollOut(BaseModel):
    poll_id: str
    question: str
    is_closed: bool
    allow_multi_votes: bool
    options: List[PollOptionOut]


class PollCreate(BaseModel):
    question: str
    options: List[str]
    allow_multi_votes: bool = False


@router.get("/", response_model=List[PollOut])
def list_polls(db: Session = Depends(get_db)):
    polls = db.query(Poll).filter(Poll.deleted.is_(False)).all()
    out = []
    for p in polls:
        opts = []
        for o in p.options:
            vote_count = db.query(Vote).filter(Vote.poll_option_id == o.option_id, Vote.deleted.is_(False)).count()
            opts.append(PollOptionOut(option_id=o.option_id, option_text=o.option_text, votes=vote_count))
        out.append(PollOut(poll_id=p.poll_id, question=p.question, is_closed=p.is_closed, allow_multi_votes=p.allow_multi_votes, options=opts))
    return out


@router.post("/", response_model=PollOut)
def create_poll(payload: PollCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # create poll using controller
    new_poll = PollCtrl.create(db=db, question=payload.question, owner_id=current_user.user_id, options=payload.options, allow_multi_votes=payload.allow_multi_votes)
    # build response
    opts = []
    for o in new_poll.options:
        vote_count = db.query(Vote).filter(Vote.poll_option_id == o.option_id, Vote.deleted.is_(False)).count()
        opts.append(PollOptionOut(option_id=o.option_id, option_text=o.option_text, votes=vote_count))
    return PollOut(poll_id=new_poll.poll_id, question=new_poll.question, is_closed=new_poll.is_closed, allow_multi_votes=new_poll.allow_multi_votes, options=opts)


class VotePayload(BaseModel):
    poll_option_id: str


@router.post("/{poll_id}/vote")
def vote_on_poll(poll_id: str, payload: VotePayload, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        vote = VoteCtrl.create(db=db, poll_option_id=payload.poll_option_id, user_id=current_user.user_id)
        return {"vote_id": vote.vote_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
