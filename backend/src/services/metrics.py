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
