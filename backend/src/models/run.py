from sqlalchemy import String,Float,Integer,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class AuditRun(Base):
 __tablename__="audit_runs"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 policy_id:Mapped[str]=mapped_column(ForeignKey("score_policies.id"))
 status:Mapped[str]=mapped_column(String)
 result:Mapped[dict]=mapped_column(JSON,default=dict)
 error:Mapped[str]=mapped_column(String,default="")
 created_at:Mapped[str]=mapped_column(String)
