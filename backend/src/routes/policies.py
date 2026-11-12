from fastapi import APIRouter,Depends
from sqlalchemy import select
from src.config.database import db_session
from src.controllers.auth import current_user,writer,admin
from src.models import ScorePolicy
from src.schemas.policy import PolicyInput
from src.services import policies as service
from src.utils.serialization import rows
router=APIRouter(prefix="/policies")
@router.get("")
def listing(db=Depends(db_session),user=Depends(current_user)): return rows(db.scalars(select(ScorePolicy).order_by(ScorePolicy.created_at.desc())))
@router.post("")
def create(payload:PolicyInput,db=Depends(db_session),user=Depends(writer)): return service.create(db,payload)
