import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select, text

# --- CONFIGURATION & MODELS ---
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "myapp")

DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL, echo=False)


class Loot(SQLModel):
    item_name: str = Field(index=True)
    rarity: str
    finder_name: str


class LootCreate(Loot, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dropped_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Legendary Loot Tracker", lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/loot/", response_model=Loot)
def record_loot(loot: Loot, session: Session = Depends(get_session)):
    loot_create = LootCreate.model_validate(loot)
    session.add(loot_create)
    session.commit()
    session.refresh(loot_create)
    return loot


@app.get("/loot/latest")
def get_latest_loot(session: Session = Depends(get_session)):
    statement = select(LootCreate).order_by(LootCreate.dropped_at.desc())
    latest = session.exec(statement).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No loot found yet.")
    return {"item_name": latest.item_name, "source": "database"}


@app.get("/loot/", response_model=List[Loot])
def list_all_loot(session: Session = Depends(get_session)):
    results = session.exec(select(LootCreate)).all()
    return [Loot.model_validate(result) for result in results]
