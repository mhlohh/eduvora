import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.core.db import get_db
from backend.models.models import User, CodeSubmission
from backend.schemas.schemas import CodeRunRequest
from backend.services.code_service import run_code_in_sandbox

router = APIRouter(prefix="/api/code", tags=["code"])


@router.post("/run")
async def run_code(payload: CodeRunRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await run_code_in_sandbox(payload.language, payload.code, payload.test_cases)

    syntax_errors = 1 if result.get("syntax_error") else 0
    logic_errors = result.get("failed_tests", 0)
    execution_success = bool(result.get("success"))

    row = CodeSubmission(
        user_id=current_user.id,
        course_id=payload.course_id,
        language=payload.language,
        code=payload.code,
        result=json.dumps(result),
        syntax_errors=syntax_errors,
        logic_errors=logic_errors,
        attempts=1,
        execution_success=execution_success,
    )
    db.add(row)
    db.commit()

    ai_feedback = "Great work." if execution_success else "Review failing test cases and edge conditions."

    return {
        "execution": result,
        "tracking": {
            "syntax_errors": syntax_errors,
            "logic_errors": logic_errors,
            "attempts": 1,
            "execution_success": execution_success,
        },
        "ai_feedback": ai_feedback,
    }
