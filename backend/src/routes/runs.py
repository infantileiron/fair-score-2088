from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from src.config.database import db_session
from src.controllers.auth import current_user,writer
from src.models import AuditRun
from src.schemas.run import RunInput
from src.services import runs as service
from src.utils.serialization import serialize,rows
router=APIRouter(prefix="/runs")
@router.get("")
def listing(db=Depends(db_session),user=Depends(current_user)): return rows(db.scalars(select(AuditRun).order_by(AuditRun.created_at.desc())))
@router.get("/{id}")
def detail(id:str,db=Depends(db_session),user=Depends(current_user)):
 item=db.get(AuditRun,id)
 if not item: raise HTTPException(404,"计算记录不存在")
 return serialize(item)
@router.post("")
def create(payload:RunInput,db=Depends(db_session),user=Depends(writer)): return service.create(db,payload.policy_id)
