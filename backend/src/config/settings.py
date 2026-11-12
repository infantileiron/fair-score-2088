import os
DATABASE_URL=os.getenv("DATABASE_URL","postgresql+psycopg://fair:fair-demo@db/fair")
REDIS_URL=os.getenv("REDIS_URL","redis://redis:6379/0")
JWT_SECRET=os.getenv("JWT_SECRET","development-only-change-this-key-32chars")
SEED_DEMO=os.getenv("SEED_DEMO","true").lower()=="true"
