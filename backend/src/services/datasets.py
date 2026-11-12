from fastapi import HTTPException
from sqlalchemy import select
from src.models import CandidateDataset
from src.utils.time import now
from src.utils.serialization import serialize
import uuid
def create(db,payload):
 if db.scalar(select(CandidateDataset).where(CandidateDataset.name==payload.name)): raise HTTPException(409,"数据集名称已存在")
 item=CandidateDataset(id=str(uuid.uuid4()),name=payload.name,source=payload.source,rows=[r.model_dump() for r in payload.rows],created_at=now());db.add(item);db.commit();return serialize(item)
def require(db,id):
 item=db.get(CandidateDataset,id)
 if not item: raise HTTPException(404,"数据集不存在")
 return item
