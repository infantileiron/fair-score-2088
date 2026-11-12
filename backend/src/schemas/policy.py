from pydantic import BaseModel,Field
class PolicyInput(BaseModel):
 name:str=Field(min_length=2,max_length=100)
 dataset_id:str
 threshold:float=Field(ge=0,le=100,allow_inf_nan=False)
 max_gap:float=Field(default=0.1,ge=0,le=1,allow_inf_nan=False)
