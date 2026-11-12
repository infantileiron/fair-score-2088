from contextlib import asynccontextmanager
import logging
import redis
from fastapi import FastAPI
from sqlalchemy import text
from src.config.database import engine
from src.config.settings import REDIS_URL,SEED_DEMO
from src.middlewares.errors import ErrorMiddleware
from src.middlewares.audit import AuditMiddleware
from src.routes import auth,datasets,policies,runs,reviews,reports,audit
@asynccontextmanager
async def lifespan(app):
 if SEED_DEMO:
  try:
   from scripts.seed_demo import seed
   seed()
  except Exception: logging.exception("demo seed failed")
 yield
app=FastAPI(title="衡尺 · 筛选公平复核",lifespan=lifespan)
app.add_middleware(AuditMiddleware)
app.add_middleware(ErrorMiddleware)
for module in (auth,datasets,policies,runs,reviews,reports,audit): app.include_router(module.router)
@app.get("/health")
def health():
 with engine.connect() as db: db.execute(text("SELECT 1"))
 redis.Redis.from_url(REDIS_URL).ping()
 return {"status":"ok"}
