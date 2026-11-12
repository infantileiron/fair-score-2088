from sqlalchemy import String,Float,Integer,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class AuditReport(Base):
 __tablename__="audit_reports"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 run_id:Mapped[str]=mapped_column(ForeignKey("audit_runs.id"),unique=True)
 title:Mapped[str]=mapped_column(String)
 published_by:Mapped[str]=mapped_column(String)
 created_at:Mapped[str]=mapped_column(String)
