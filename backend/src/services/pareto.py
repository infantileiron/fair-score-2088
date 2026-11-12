from src.services.metrics import group_metrics,gap,job_review
def weighted_selection_gap(rows,threshold,weights):
 return job_review(rows,threshold,weights)["weighted_selection_gap"]
def threshold_frontier(rows,weights=None):
 points=[]
 for threshold in range(0,101,5):
  groups=group_metrics(rows,threshold)
  correct=sum(g["tp"]+g["tn"] for g in groups)
  selection_gap=gap([g["selection_rate"] for g in groups])
  if weights is not None: selection_gap=weighted_selection_gap(rows,threshold,weights)
  points.append({"threshold":threshold,"accuracy":correct/len(rows),"selection_gap":selection_gap})
 for p in points:
  p["pareto"]=p["selection_gap"] is not None and not any(q["selection_gap"] is not None and q["accuracy"]>=p["accuracy"] and q["selection_gap"]<=p["selection_gap"] and (q["accuracy"]>p["accuracy"] or q["selection_gap"]<p["selection_gap"]) for q in points)
 return points
