import subprocess
import tempfile
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="EduVora Code Runner")


class RunRequest(BaseModel):
    language: str
    code: str
    test_cases: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
def run_code(payload: RunRequest):
    if payload.language != "python":
        return {"success": False, "error": "Only python is supported in this prototype"}

    syntax_error = False
    failed_tests = 0
    output = ""
    error = ""

    for case in payload.test_cases or [{"input": "", "expected_output": ""}]:
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=True) as f:
            f.write(payload.code)
            f.flush()
            proc = subprocess.run(
                ["python", f.name],
                input=str(case.get("input", "")),
                text=True,
                capture_output=True,
                timeout=3,
            )
            output = proc.stdout.strip()
            error = proc.stderr.strip()

            if proc.returncode != 0:
                syntax_error = True

            expected = str(case.get("expected_output", "")).strip()
            if not syntax_error and expected and output != expected:
                failed_tests += 1

    return {
        "success": (not syntax_error and failed_tests == 0),
        "output": output,
        "error": error,
        "syntax_error": syntax_error,
        "failed_tests": failed_tests,
    }
