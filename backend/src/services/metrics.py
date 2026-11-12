import math
def wilson(k,n,z=1.959963984540054):
 if n==0: return None
 p=k/n;d=1+z*z/n
 center=(p+z*z/(2*n))/d
 half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
 return [0.0 if k==0 else max(0,center-half),1.0 if k==n else min(1,center+half)]
def group_metrics(rows,threshold):
 result=[]
 for name in sorted({r["group"] for r in rows}):
  subset=[r for r in rows if r["group"]==name]
  tp=sum(r["score"]>=threshold and r["qualified"]==1 for r in subset)
  fp=sum(r["score"]>=threshold and r["qualified"]==0 for r in subset)
  positives=sum(r["qualified"] for r in subset);n=len(subset);negatives=n-positives
  result.append({"group":name,"n":n,"selected":tp+fp,"qualified":positives,"tp":tp,"fp":fp,"fn":positives-tp,"tn":negatives-fp,"selection_rate":(tp+fp)/n,"selection_ci":wilson(tp+fp,n),"tpr":tp/positives if positives else None,"fpr":fp/negatives if negatives else None,"tpr_ci":wilson(tp,positives),"fpr_ci":wilson(fp,negatives),"small_sample":n<30})
 return result
def gap(values):
 valid=[v for v in values if v is not None]
 return max(valid)-min(valid) if len(valid)>1 else None
def check_weights(weights):
 """Normalise policy job weights; they must be non-negative and sum to one."""
 if not weights: raise ValueError("岗位权重不能为空")
 cleaned={};total=0.0
 for name,weight in weights.items():
  if not isinstance(name,str) or not name.strip(): raise ValueError("岗位名称不能为空")
  key=name.strip()
  if key in cleaned: raise ValueError("岗位名称重复")
  if isinstance(weight,bool) or not isinstance(weight,(int,float)) or not math.isfinite(weight) or weight<0: raise ValueError("岗位权重应为非负有限数")
  cleaned[key]=float(weight);total+=float(weight)
 if not math.isclose(total,1.0,rel_tol=0,abs_tol=1e-9): raise ValueError("岗位权重合计应为1")
 return cleaned
def job_of(row):
 value=row.get("job")
 return value.strip() if isinstance(value,str) else ""
def job_review(rows,threshold,weights):
 """Compare groups on the policy's common job weights without re-normalising.

 Job-level counts and rates are kept for every group/job cell that exists. A missing
 job field, or a target job absent from any group, makes the whole weighted comparison
 incomparable: no zero fill and no weight redistribution.
 """
 weights=check_weights(weights)
 groups=sorted({r["group"] for r in rows})
 missing_job_rows=sum(1 for r in rows if not job_of(r))
 jobs=[];reasons=[]
 for job,weight in weights.items():
  cells=[];missing=[]
  for group in groups:
   subset=[r for r in rows if r["group"]==group and job_of(r)==job]
   n=len(subset)
   if n==0:
    missing.append(group);continue
   selected=sum(1 for r in subset if r["score"]>=threshold)
   cells.append({"group":group,"n":n,"selected":selected,"selection_rate":selected/n})
  jobs.append({"job":job,"weight":weight,"groups":cells,"missing_groups":missing})
  if missing: reasons.append("、".join(missing)+"缺少目标岗位「"+job+"」")
 if missing_job_rows: reasons.append("样本中"+str(missing_job_rows)+"条记录缺少岗位字段")
 comparable=not missing_job_rows and not any(job["missing_groups"] for job in jobs)
 weighted_groups=[]
 for group in groups:
  rate=None;contributions=[]
  if comparable:
   for job in jobs:
    cell=next(c for c in job["groups"] if c["group"]==group)
    contributions.append({"job":job["job"],"weight":job["weight"],"selection_rate":cell["selection_rate"],"contribution":job["weight"]*cell["selection_rate"]})
   rate=sum(c["contribution"] for c in contributions)
  weighted_groups.append({"group":group,"weighted_selection_rate":rate,"contributions":contributions})
 weighted_gap=gap([g["weighted_selection_rate"] for g in weighted_groups]) if comparable else None
 return {"enabled":True,"weights":weights,"weight_sum":round(sum(weights.values()),12),"comparable":comparable,"reason":"；".join(reasons),"missing_job_rows":missing_job_rows,"jobs":jobs,"groups":weighted_groups,"weighted_selection_gap":weighted_gap}
