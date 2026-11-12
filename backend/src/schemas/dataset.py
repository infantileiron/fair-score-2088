from pydantic import BaseModel,Field,model_validator,field_validator
class Candidate(BaseModel):
 candidate_id:str=Field(min_length=1,max_length=60)
 group:str=Field(min_length=1,max_length=40)
 score:float=Field(ge=0,le=100,allow_inf_nan=False)
 qualified:int=Field(ge=0,le=1)
 job:str|None=Field(default=None,max_length=40)
 @field_validator("job")
 @classmethod
 def normalize_job(cls,value):
  if value is None: return None
  value=value.strip()
  return value or None
class DatasetInput(BaseModel):
 name:str=Field(min_length=2,max_length=100)
 source:str=Field(default="import.json",max_length=120)
 rows:list[Candidate]=Field(min_length=20,max_length=5000)
 @model_validator(mode="after")
 def quality(self):
  ids=[x.candidate_id for x in self.rows]
  if len(set(ids))!=len(ids): raise ValueError("候选ID重复")
  groups={x.group for x in self.rows}
  if len(groups)<2 or len(groups)>8: raise ValueError("需要2至8个复核组")
  return self
