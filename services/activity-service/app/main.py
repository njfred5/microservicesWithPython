import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

from app.infrastructure.rabbitmq_publisher import publish_notification

app = FastAPI(title="activity-service")

USER_SERVICE = "http://localhost:8001"
GAME_SERVICE = "http://localhost:8002"
activities_db = []
class ActivityCreate(BaseModel):
    user_id: str
    game_id: str
    action: str
    duration_minutes: int | None = None
async def validate_user(user_id: str):
    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{USER_SERVICE}/v1/users/{user_id}")
                if resp.status_code == 404:
                    raise HTTPException(status_code=404, detail="User not found")
                resp.raise_for_status()
                return resp.json()
        except httpx.RequestError:
            if attempt == 2:
                raise HTTPException(status_code=503, detail="user-service unreachable")
async def enrich_game(game_id: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{GAME_SERVICE}/v1/games/{game_id}")
            if resp.status_code == 200:
                return resp.json()
            return None
    except httpx.RequestError:
        return None
@app.post("/v1/activities", status_code=201)
async def create_activity(data: ActivityCreate):
    user = await validate_user(data.user_id)
    game = await enrich_game(data.game_id)
    activity = {
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "action": data.action,
        "duration_minutes": data.duration_minutes,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "game": game,
    }
    activities_db.append(activity)

    game_title = game["title"] if game else data.game_id
    username = user.get("username", data.user_id) if user else data.user_id

    try:
        publish_notification(
            user_id=data.user_id,
            message=f"{username} just {data.action} {game_title}",
        )
    except Exception:
        pass
    return activity
@app.get("/v1/activities")
async def list_activities(limit: int = 20, offset: int = 0):
    page = activities_db[offset: offset + limit]
    return {"items": page, "total": len(activities_db), "limit": limit, "offset": offset}
@app.get("/v1/activities/user/{user_id}")
async def user_activities(user_id: str, limit: int = 20, offset: int = 0):
    filtered = [a for a in activities_db if a["user_id"] == user_id]
    page = filtered[offset: offset + limit]
    return {"items": page, "total": len(filtered), "limit": limit, "offset": offset}
@app.get("/health")
async def health():
    return {"status": "ok", "service": "activity-service"}