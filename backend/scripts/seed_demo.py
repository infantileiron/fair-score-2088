import random,json
from sqlalchemy import select,func,text,inspect
from src.config.database import Base,engine,Session
from src.models import User,CandidateDataset,ScorePolicy,AuditRun,GroupReview,AuditReport
from src.utils.security import hash_password
from src.utils.time import now
from src.services.analysis import analyze
def ensure_columns():
 """Add nullable columns for pre-existing databases; new installs get them from create_all."""
 Base.metadata.create_all(engine)
 if "job_weights" in {c["name"] for c in inspect(engine).get_columns("score_policies")}: return
 with engine.begin() as db: db.execute(text("ALTER TABLE score_policies ADD COLUMN job_weights JSON"))
def seed():
 ensure_columns()
 with Session() as db:
  for role in ("admin","analyst","viewer"):
   if not db.get(User,role): db.add(User(id=role,email=role+"@hengchi.demo",password=hash_password("Review2026!"),role=role))
  rng=random.Random(2203)
  observations=[]
  for i in range(800):
   group="评估组A" if i%2==0 else "评估组B"
   skill=rng.gauss(66,15);score=max(0,min(100,skill+rng.gauss(0,9)-(5 if group=="评估组B" else 0)))
   observations.append({"candidate_id":f"HC-{i+1:04}","group":group,"score":round(score,2),"qualified":int(skill>=63)})
  # Post-stratified sample: each group is ahead within every job, but group B's job mix
  # leans on the high-rate job, so the overall and job-weighted selection trends conflict.
  job_rows=[];serial=1
  compositions={
   "评估组A":(("研发",10,7),("运营",30,18),("设计",160,88)),
   "评估组B":(("研发",160,109),("运营",30,17),("设计",10,5)),
  }
  for group,spec in compositions.items():
   for job,n,selected in spec:
    for i in range(n):
     score=round(65.0+35.0*(i+0.5)/selected,2) if i<selected else round(0.5+64.4*(i-selected+0.5)/(n-selected),2)
     job_rows.append({"candidate_id":f"HC-J{serial:04}","group":group,"job":job,"score":score,"qualified":int((i%3)!=0)});serial+=1
  if not db.get(CandidateDataset,"demo-data"): db.add(CandidateDataset(id="demo-data",name="2026秋季统一测评·匿名样本",source="hengchi_candidates_202611.json",rows=observations,created_at=now()));db.flush()
  if not db.get(CandidateDataset,"demo-job-data"): db.add(CandidateDataset(id="demo-job-data",name="2026秋季统一测评·岗位构成样本",source="hengchi_candidates_202611_jobs.json",rows=job_rows,created_at=now()));db.flush()
  if not db.get(ScorePolicy,"demo-policy"): db.add(ScorePolicy(id="demo-policy",name="统一分数线65·回顾性复核",threshold=65,dataset_id="demo-data",max_gap=0.1,job_weights=None,created_at=now()));db.flush()
  if not db.get(ScorePolicy,"demo-weighted-policy"): db.add(ScorePolicy(id="demo-weighted-policy",name="统一分数线65·岗位加权复核",threshold=65,dataset_id="demo-job-data",max_gap=0.1,job_weights={"研发":0.6,"运营":0.3,"设计":0.1},created_at=now()));db.flush()
  if not db.get(AuditRun,"demo-run"): db.add(AuditRun(id="demo-run",policy_id="demo-policy",status="completed",result=analyze(observations,65,0.1),error="",created_at=now()));db.flush()
  if not db.get(AuditRun,"demo-weighted-run"): db.add(AuditRun(id="demo-weighted-run",policy_id="demo-weighted-policy",status="completed",result=analyze(job_rows,65,0.1,{"研发":0.6,"运营":0.3,"设计":0.1}),error="",created_at=now()));db.flush()
  if not db.get(GroupReview,"demo-review"): db.add(GroupReview(id="demo-review",run_id="demo-run",note="标签取自统一测评，已记录组间样本分母。下一轮核验标签偏差，不用于自动招聘决策。",decision="accepted",author="analyst@hengchi.demo",created_at=now()));db.flush()
  if not db.get(GroupReview,"demo-weighted-review"): db.add(GroupReview(id="demo-weighted-review",run_id="demo-weighted-run",note="岗位构成不同，总体入选率与岗位加权结果方向相反；已核对岗位分母与权重。",decision="accepted",author="analyst@hengchi.demo",created_at=now()));db.flush()
  if not db.get(AuditReport,"demo-report"): db.add(AuditReport(id="demo-report",run_id="demo-run",title="秋季筛选·回顾性公平复核",published_by="admin@hengchi.demo",created_at=now()))
  if not db.get(AuditReport,"demo-weighted-report"): db.add(AuditReport(id="demo-weighted-report",run_id="demo-weighted-run",title="秋季筛选·岗位加权复核",published_by="admin@hengchi.demo",created_at=now()))
  db.commit()
  return {m.__tablename__:db.scalar(select(func.count()).select_from(m)) for m in (User,CandidateDataset,ScorePolicy,AuditRun,GroupReview,AuditReport)}
if __name__=="__main__": print(json.dumps(seed(),ensure_ascii=False))
