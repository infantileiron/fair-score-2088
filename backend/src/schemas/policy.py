from pydantic import BaseModel,Field,model_validator
import math
class PolicyInput(BaseModel):
 name:str=Field(min_length=2,max_length=100)
 dataset_id:str
 threshold:float=Field(ge=0,le=100,allow_inf_nan=False)
 max_gap:float=Field(default=0.1,ge=0,le=1,allow_inf_nan=False)
 job_weights:dict[str,float]|None=None
 @model_validator(mode="after")
 def weights(self):
  if self.job_weights is None: return self
  if not self.job_weights: raise ValueError("岗位权重不能为空")
  clean={};total=0.0
  for raw,weight in self.job_weights.items():
   job=raw.strip()
   if not job: raise ValueError("岗位名称不能为空")
   if job in clean: raise ValueError("岗位名称重复")
   if isinstance(weight,bool) or not isinstance(weight,(int,float)) or not math.isfinite(weight) or weight<0: raise ValueError("岗位权重应为非负有限数")
   clean[job]=float(weight);total+=float(weight)
  if not math.isclose(total,1.0,rel_tol=0,abs_tol=1e-9): raise ValueError("岗位权重合计应为1")
  self.job_weights=clean
  return self
