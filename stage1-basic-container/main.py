from fastapi import FastAPI

app = FastAPI(title="Legendary Loot Tracker")


@app.get("/loot/latest")
def get_latest_loot():
    return {"item_name": "Wooden Sword", "source": "hardcoded (no database yet!)"}
