from sqlalchemy import String,Float,Integer,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class CandidateDataset(Base):
 __tablename__="candidate_datasets"
 id:Mapped[str]=mapped_column(String,primary_key=True)
 name:Mapped[str]=mapped_column(String,unique=True)
 source:Mapped[str]=mapped_column(String)
 rows:Mapped[list]=mapped_column(JSON)
 created_at:Mapped[str]=mapped_column(String)
