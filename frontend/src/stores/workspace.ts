import {listDatasets} from '../api/datasets';import {listPolicies} from '../api/policies';import {listRuns} from '../api/runs';import {listReviews} from '../api/reviews';import {listReports} from '../api/reports';import {listAudit} from '../api/audit';
export async function loadWorkspace(){const [datasets,policies,runs,reviews,reports,audit]=await Promise.all([listDatasets(),listPolicies(),listRuns(),listReviews(),listReports(),listAudit()]);return {datasets,policies,runs,reviews,reports,audit}}
export type Workspace=Awaited<ReturnType<typeof loadWorkspace>>;
