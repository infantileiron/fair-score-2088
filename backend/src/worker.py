import time,traceback
from pathlib import Path
import redis
from sqlalchemy import select
from src.config.settings import REDIS_URL
from src.config.database import Session
from src.models import AuditRun,ScorePolicy,CandidateDataset
from src.services.analysis import analyze
client=redis.Redis.from_url(REDIS_URL)
heartbeat=Path("/artifacts/worker-heartbeat")
def execute(id):
 with Session() as db:
  run=db.get(AuditRun,id)
  if not run or run.status not in ("queued","running"): return
  run.status="running";db.commit()
  try:
   policy=db.get(ScorePolicy,run.policy_id);data=db.get(CandidateDataset,policy.dataset_id)
   run.result=analyze(data.rows,policy.threshold,policy.max_gap);run.status="completed"
  except Exception as error: run.status="failed";run.error=str(error);traceback.print_exc()
  db.commit()
# Resume jobs persisted before a worker restart, including a queue handoff interrupted by a crash.
with Session() as db:
 for id in db.scalars(select(AuditRun.id).where(AuditRun.status.in_(["queued","running"]))): client.lpush("fair-score:queue",id)
while True:
 heartbeat.touch()
 job=client.brpop("fair-score:queue",timeout=1)
 if job: execute(job[1].decode())
