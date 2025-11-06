from fastapi import APIRouter, Depends, Header, HTTPException, Request
from ..core.db import get_db
from ..core.config import settings
from sqlalchemy.orm import Session
from ..models import PullRequest, PullRequestRisk, Base
from ..services import (
    analyze_complexity,
    detect_dependency_changes,
    detect_code_duplication,
    analyze_test_coverage,
    scan_security_vulnerabilities,
    analyze_collaboration,
    compute_risk
)

router = APIRouter()

@router.get("/healthz")
async def health_check():
    return {"status": "ok"}

@router.get("/env")
async def env_info():
    from ..core.config import settings
    return {"env": settings.ENV, "app": settings.APP_NAME}

@router.post("/analyze/complexity")
async def analyze_code_complexity(request: Request):
    """Analyze code complexity for a given code snippet."""
    payload = await request.json()
    code = payload.get("code", "")
    language = payload.get("language", "python")
    
    if not code:
        raise HTTPException(status_code=400, detail="Code snippet is required")
    
    result = analyze_complexity(code, language)
    return {"status": "success", "result": result}

@router.post("/analyze/test-coverage")
async def analyze_test_coverage_endpoint(request: Request):
    """Analyze test coverage changes between baseline and PR."""
    payload = await request.json()
    baseline_coverage = payload.get("baseline_coverage", {})
    pr_coverage = payload.get("pr_coverage", {})
    
    if not baseline_coverage or not pr_coverage:
        raise HTTPException(status_code=400, detail="Both baseline_coverage and pr_coverage are required")
    
    result = analyze_test_coverage(baseline_coverage, pr_coverage)
    return {"status": "success", "result": result}

@router.post("/analyze/dependency-changes")
async def detect_dependency_changes_endpoint(request: Request):
    """Detect dependency changes between baseline and PR."""
    payload = await request.json()
    baseline_deps = payload.get("baseline_deps", {})
    pr_deps = payload.get("pr_deps", {})
    
    if not baseline_deps or not pr_deps:
        raise HTTPException(status_code=400, detail="Both baseline_deps and pr_deps are required")
    
    result = detect_dependency_changes(baseline_deps, pr_deps)
    return {"status": "success", "result": result}

@router.post("/analyze/security-scan")
async def scan_security_vulnerabilities_endpoint(request: Request):
    """Scan code for security vulnerabilities and code defects."""
    payload = await request.json()
    code = payload.get("code", "")
    language = payload.get("language", "python")
    
    if not code:
        raise HTTPException(status_code=400, detail="Code snippet is required")
    
    result = scan_security_vulnerabilities(code, language)
    return {"status": "success", "result": result}

@router.post("/analyze/code-duplication")
async def detect_code_duplication_endpoint(request: Request):
    """Detect duplicate code fragments in the given code."""
    payload = await request.json()
    code = payload.get("code", "")
    language = payload.get("language", "python")
    min_lines = payload.get("min_lines", 3)
    
    if not code:
        raise HTTPException(status_code=400, detail="Code snippet is required")
    
    result = detect_code_duplication(code, language, min_lines)
    return {"status": "success", "result": result}

@router.post("/analyze/collaboration")
async def analyze_collaboration_endpoint(request: Request):
    """Analyze PR comments for collaboration efficiency."""
    payload = await request.json()
    comments = payload.get("comments", [])
    
    if not comments:
        raise HTTPException(status_code=400, detail="Comments list is required")
    
    result = analyze_collaboration(comments)
    return {"status": "success", "result": result}

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
