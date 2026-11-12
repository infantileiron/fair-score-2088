export interface Candidate {candidate_id:string; group:string; score:number; qualified:number; job?:string|null}
export interface Dataset {id:string;name:string;source:string;rows:Candidate[];created_at:string}
export interface Policy {id:string;name:string;dataset_id:string;threshold:number;max_gap:number;job_weights?:Record<string,number>|null;created_at:string}
export interface GroupMetric {group:string;n:number;selected:number;qualified:number;tp:number;fp:number;fn:number;tn:number;selection_rate:number;selection_ci:[number,number];tpr:number|null;fpr:number|null;small_sample:boolean}
export interface JobCell {group:string;n:number;selected:number;selection_rate:number}
export interface JobRow {job:string;weight:number;groups:JobCell[];missing_groups:string[]}
export interface WeightedContribution {job:string;weight:number;selection_rate:number;contribution:number}
export interface WeightedGroup {group:string;weighted_selection_rate:number|null;contributions:WeightedContribution[]}
export interface JobReview {enabled:boolean;weights:Record<string,number>;weight_sum:number;comparable:boolean;reason:string;missing_job_rows:number;jobs:JobRow[];groups:WeightedGroup[];weighted_selection_gap:number|null}
export interface Frontier {threshold:number;accuracy:number;selection_gap:number|null;pareto:boolean}
export interface Result {n:number;threshold:number;groups:GroupMetric[];selection_gap:number|null;overall_selection_gap?:number|null;tpr_gap:number|null;fpr_gap:number|null;accuracy:number;max_gap:number;exceeds_gap:boolean|null;frontier:Frontier[];warnings:string[];checksum:string;job_review?:JobReview|null}
export interface Run {id:string;policy_id:string;status:string;result:Result;error:string;created_at:string}
export interface Review {id:string;run_id:string;note:string;decision:string;author:string;created_at:string}
export interface Report {id:string;run_id:string;title:string;published_by:string;created_at:string}
export interface Audit {id:string;actor:string;action:string;status:number;created_at:string}
export interface User {email:string;role:string}
