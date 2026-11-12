from sqlalchemy import String,Float,Integer,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class GroupReview(Base):
 __tablename__="group_reviews"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 run_id:Mapped[str]=mapped_column(ForeignKey("audit_runs.id"))
 note:Mapped[str]=mapped_column(String)
 decision:Mapped[str]=mapped_column(String)
 author:Mapped[str]=mapped_column(String)
 created_at:Mapped[str]=mapped_column(String)
