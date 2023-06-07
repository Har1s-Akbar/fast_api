from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import verify_user
from  ..schemas import VoteCreate
from ..models import  Post,Vote

router = APIRouter()

@router.post("/vote")
def vote(vote:VoteCreate,db:Session = Depends(get_db), current_user: int = Depends(verify_user)):
    post = db.query(Post).filter(vote.post_id == Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post you are trying to vote on does not exist")
    vote_query = db.query(Vote).filter(vote.post_id == Vote.posts_id, Vote.user_id == current_user.id)
    vote_exist = vote_query.first()
    if vote.dir ==1:
        if vote_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'post with such id already has a vote')
        else:
            new_vote = Vote(posts_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added the vote"}
    else:
        if not vote_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "successfully deleted"}