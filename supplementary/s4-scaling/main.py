import os
import socket
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Optional

import redis
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select, text

HOSTNAME = socket.gethostname()

# --- 1. CONFIGURATION & MODELS ---
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "myapp")

DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

engine = create_engine(DB_URL, echo=False)
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


class Loot(SQLModel):
    item_name: str = Field(index=True)
    rarity: str  # e.g., Common, Rare, Legendary
    finder_name: str


class LootCreate(Loot, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dropped_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )


# --- 2. DATABASE INITIALIZATION ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Legendary Loot Tracker", lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


# --- 3. THE "INTERESTING" LOGIC (CACHE ASIDE PATTERN) ---


@app.post("/loot/", response_model=Loot)
def record_loot(loot: Loot, session: Session = Depends(get_session)):
    loot_create = LootCreate.model_validate(loot)

    session.add(loot_create)
    session.commit()
    session.refresh(loot_create)

    # Invalidate the cache because the "latest" has changed
    cache.delete("latest_loot_name")
    return loot


@app.get("/loot/latest")
def get_latest_loot(session: Session = Depends(get_session)):
    # 1. Try to get from Redis Cache first
    cached_name = cache.get("latest_loot_name")
    if cached_name:
        return {"item_name": cached_name, "source": "cache (lightning fast!)", "served_by": HOSTNAME,}

    # 2. If not in cache, hit Postgres
    # Artificial delay to simulate a "heavy" production query
    statement = select(LootCreate).order_by(LootCreate.dropped_at.desc())
    latest = session.exec(statement).first()

    if not latest:
        raise HTTPException(status_code=404, detail="No loot found yet.")

    # 3. Store in Redis for next time (expires in 30 seconds)
    cache.set("latest_loot_name", latest.item_name, ex=30)

    return {"item_name": latest.item_name, "source": "database (slow & steady)", "served_by": HOSTNAME,}


@app.get("/loot/", response_model=List[Loot])
def list_all_loot(session: Session = Depends(get_session)):
    return session.exec(select(Loot)).all()
