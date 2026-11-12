import csv,io
GROUP_COLUMNS=["group","n","selected","qualified","tp","fp","fn","tn","selection_rate","tpr","fpr"]
JOB_COLUMNS=["record_type","group","job","weight","weight_sum","n","selected","qualified","tp","fp","fn","tn","selection_rate","tpr","fpr","weighted_selection_rate","weighted_selection_gap","comparable","note"]
def build_report_csv(result):
 """Render an archived run as CSV, using the same weighted result as the evidence page."""
 review=result.get("job_review");buf=io.StringIO()
 if not review:
  writer=csv.DictWriter(buf,GROUP_COLUMNS,extrasaction="ignore");writer.writeheader();writer.writerows(result["groups"])
  return "﻿"+buf.getvalue()
 writer=csv.DictWriter(buf,JOB_COLUMNS,extrasaction="ignore");writer.writeheader()
 weighted={g["group"]:g["weighted_selection_rate"] for g in review["groups"]}
 for group in result["groups"]:
  writer.writerow({**{k:group[k] for k in GROUP_COLUMNS},"record_type":"group","weighted_selection_rate":weighted.get(group["group"]),"weighted_selection_gap":review["weighted_selection_gap"],"comparable":review["comparable"],"note":review["reason"]})
 for job in review["jobs"]:
  for cell in job["groups"]:
   writer.writerow({"record_type":"job","group":cell["group"],"job":job["job"],"weight":job["weight"],"weight_sum":review["weight_sum"],"n":cell["n"],"selected":cell["selected"],"selection_rate":cell["selection_rate"],"comparable":True})
  for group in job["missing_groups"]:
   writer.writerow({"record_type":"job_missing","group":group,"job":job["job"],"weight":job["weight"],"weight_sum":review["weight_sum"],"comparable":False,"note":"该组缺少目标岗位，不补零、不重分权重"})
 writer.writerow({"record_type":"weighted_summary","weight_sum":review["weight_sum"],"weighted_selection_gap":review["weighted_selection_gap"],"comparable":review["comparable"],"note":review["reason"]})
 return "﻿"+buf.getvalue()
