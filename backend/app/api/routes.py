from fastapi import APIRouter, Depends, Header, HTTPException, Request
from ..core.db import get_db
from ..core.config import settings
from sqlalchemy.orm import Session
from ..models import PullRequest, PullRequestRisk, Base
from ..services.risk import compute_risk

router = APIRouter()

@router.get("/healthz")
async def health_check():
    return {"status": "ok"}

@router.get("/env")
async def env_info():
    from ..core.config import settings
    return {"env": settings.ENV, "app": settings.APP_NAME}

@router.post("/gitlab/webhook")
async def gitlab_webhook(
    request: Request,
    x_gitlab_token: str = Header(None),
    db: Session = Depends(get_db),
):
    # Simple token validation
    expected = settings.GITLAB_TOKEN
    if expected and x_gitlab_token != expected:
        raise HTTPException(status_code=401, detail="Invalid GitLab token")
    payload = await request.json()
    event_type = payload.get("object_kind")
    if event_type != "merge_request":
        return {"status": "ignored", "reason": "not a merge_request"}
    mr = payload.get("object_attributes", {})
    external_id = str(mr.get("iid"))
    title = mr.get("title", "")
    author_info = payload.get("user", {})
    author = author_info.get("username") or author_info.get("name") or "unknown"

    # Upsert PR (simplified)
    pr = db.query(PullRequest).filter(PullRequest.external_id == external_id).first()
    if not pr:
        pr = PullRequest(external_id=external_id, title=title, author=author)
        db.add(pr)
        db.flush()  # get pr.id
    else:
        pr.title = title
        pr.author = author

    # Fake features (later replace with real diff/complexity)
    changes_count = mr.get("changes_count")
    try:
        changes_float = float(changes_count) if changes_count is not None else 0.0
    except ValueError:
        changes_float = 0.0
    features = {
        "complexity_delta": min(changes_float / 100.0, 5.0),
        "file_hotness": 0.1,  # placeholder
        "sensitive_path": 0.0,
        "author_experience": 1.0,  # placeholder
    }
    risk = compute_risk(features)
    pr_risk = PullRequestRisk(pr_id=pr.id, score=risk["score"], level=risk["level"], details=risk["details"])
    db.add(pr_risk)
    db.commit()
    return {"status": "processed", "pr_id": pr.id, "risk": risk}
