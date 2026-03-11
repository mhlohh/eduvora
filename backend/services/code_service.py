import httpx
from backend.core.config import settings


async def run_code_in_sandbox(language: str, code: str, test_cases: list[dict]):
    payload = {"language": language, "code": code, "test_cases": test_cases}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(f"{settings.code_runner_url}/run", json=payload)
        response.raise_for_status()
        return response.json()
