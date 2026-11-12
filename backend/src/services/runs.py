import uuid
import redis
from fastapi import HTTPException
from src.models import ScorePolicy,AuditRun
from src.config.settings import REDIS_URL
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,policy_id):
 if not db.get(ScorePolicy,policy_id): raise HTTPException(404,"方案不存在")
 item=AuditRun(id=str(uuid.uuid4()),policy_id=policy_id,status="queued",result={},error="",created_at=now());db.add(item);db.commit()
 try: redis.Redis.from_url(REDIS_URL).lpush("fair-score:queue",item.id)
 except redis.RedisError:
  item.status="failed";item.error="计算队列不可用，请重新运行";db.commit();raise HTTPException(503,item.error)
 return serialize(item)
def require_completed(db,id):
 item=db.get(AuditRun,id)
 if not item: raise HTTPException(404,"计算记录不存在")
 if item.status!="completed": raise HTTPException(409,"计算尚未完成")
 return item
