import hashlib,json,math
from src.services.metrics import group_metrics,gap,job_review
from src.services.pareto import threshold_frontier
def analyze(rows,threshold,max_gap,weights=None):
 if len(rows)<20: raise ValueError("样本至少20条")
 if not math.isfinite(threshold) or not 0<=threshold<=100: raise ValueError("阈值应在0至100")
 if len({r["group"] for r in rows})<2: raise ValueError("至少两个复核组")
 groups=group_metrics(rows,threshold)
 overall_gap=gap([g["selection_rate"] for g in groups])
 review=job_review(rows,threshold,weights) if weights is not None else None
 selection_gap=review["weighted_selection_gap"] if review is not None else overall_gap
 result={"threshold":threshold,"n":len(rows),"groups":groups,"selection_gap":selection_gap,"tpr_gap":gap([g["tpr"] for g in groups]),"fpr_gap":gap([g["fpr"] for g in groups]),"accuracy":sum(g["tp"]+g["tn"] for g in groups)/len(rows),"exceeds_gap":None if selection_gap is None else selection_gap>max_gap,"max_gap":max_gap,"frontier":threshold_frontier(rows,weights),"checksum":hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),"warnings":["模拟数据仅作回顾性统计。差异不能直接解释为歧视或因果。","区间为逐组Wilson区间，未作多重比较校正；样本稀少及标签偏差需要人工复核。","同一阈值用于全部组；Pareto前沿供复核讨论，不自动推荐招聘决策。"]}
 if review is not None:
  result["overall_selection_gap"]=overall_gap
  result["job_review"]=review
 return result
