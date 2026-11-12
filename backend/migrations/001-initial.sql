-- Schema is created from versioned SQLAlchemy metadata during demo seed.
-- Production rollout: generate reviewed ALTER migrations before changing existing tables.
-- Natural keys: users.email, candidate_datasets.name, score_policies.name, audit_reports.run_id.
CREATE INDEX IF NOT EXISTS ix_audit_runs_status ON audit_runs(status);
