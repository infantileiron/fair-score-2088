import uuid,csv,io
from fastapi import HTTPException
from sqlalchemy import select
from src.models import AuditReport,GroupReview
from src.services.runs import require_completed
from src.services.exports import build_report_csv
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload,user):
 require_completed(db,payload.run_id)
 reviews=list(db.scalars(select(GroupReview).where(GroupReview.run_id==payload.run_id).order_by(GroupReview.created_at.desc())))
 if not reviews or reviews[0].decision!="accepted": raise HTTPException(409,"最新复核须为接受后才能归档")
 if db.scalar(select(AuditReport).where(AuditReport.run_id==payload.run_id)): raise HTTPException(409,"本次计算已归档")
 item=AuditReport(id=str(uuid.uuid4()),published_by=user["email"],created_at=now(),**payload.model_dump());db.add(item);db.commit();return serialize(item)
def export(db,id):
 report=db.get(AuditReport,id)
 if not report: raise HTTPException(404,"归档报告不存在")
 run=require_completed(db,report.run_id)
 return build_report_csv(run.result)
