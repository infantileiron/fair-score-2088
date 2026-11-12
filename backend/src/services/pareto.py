from src.services.metrics import group_metrics,gap
def threshold_frontier(rows):
 points=[]
 for threshold in range(0,101,5):
  groups=group_metrics(rows,threshold)
  correct=sum(g["tp"]+g["tn"] for g in groups)
  points.append({"threshold":threshold,"accuracy":correct/len(rows),"selection_gap":gap([g["selection_rate"] for g in groups])})
 for p in points:
  p["pareto"]=not any(q["accuracy"]>=p["accuracy"] and q["selection_gap"]<=p["selection_gap"] and (q["accuracy"]>p["accuracy"] or q["selection_gap"]<p["selection_gap"]) for q in points)
 return points
