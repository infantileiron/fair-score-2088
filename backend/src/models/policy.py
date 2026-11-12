from sqlalchemy import String,Float,Integer,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class ScorePolicy(Base):
 __tablename__="score_policies"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 name:Mapped[str]=mapped_column(String,unique=True)
 threshold:Mapped[float]=mapped_column(Float)
 dataset_id:Mapped[str]=mapped_column(ForeignKey("candidate_datasets.id"))
 max_gap:Mapped[float]=mapped_column(Float)
 job_weights:Mapped[dict|None]=mapped_column(JSON,nullable=True,default=None)
 created_at:Mapped[str]=mapped_column(String)
