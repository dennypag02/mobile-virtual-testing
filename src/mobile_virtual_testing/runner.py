from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class StepResult:
    id: str
    action: str
    status: str
    message: str = ""


class FakeProvider:
    """Deterministic provider used to qualify orchestration and evidence handling."""

    name = "fake"
    version = "1"

    def execute_step(self, step: dict[str, Any]) -> StepResult:
        action = step["action"]
        step_id = step["id"]

        if action not in {"launch", "tap", "text", "swipe", "wait", "screenshot", "terminate"}:
            return StepResult(step_id, action, "error", f"unsupported action: {action}")

        return StepResult(step_id, action, "passed")


def run_request(request: dict[str, Any], provider: FakeProvider | None = None) -> dict[str, Any]:
    provider = provider or FakeProvider()
    started = datetime.now(timezone.utc).isoformat()

    results = [provider.execute_step(step) for step in request["steps"]]
    status = "passed" if all(result.status == "passed" for result in results) else "failed"
    finished = datetime.now(timezone.utc).isoformat()

    artifacts: list[dict[str, str]] = []
    if request["evidence"].get("device_logs", False):
        artifacts.append({"kind": "device_log", "path": "evidence/device.log"})
    if request["evidence"].get("app_logs", True):
        artifacts.append({"kind": "app_log", "path": "evidence/app.log"})
    if request["evidence"].get("screenshots", False):
        artifacts.append({"kind": "screenshot", "path": "evidence/final.png"})

    return {
        "version": "1",
        "request_id": request["request_id"],
        "run_id": str(uuid4()),
        "status": status,
        "provider": {"name": provider.name, "version": provider.version, "host": "in-process"},
        "device": {"platform": "fake", "identifier": "fake-1"},
        "steps": [
            {
                "id": result.id,
                "action": result.action,
                "status": result.status,
                "message": result.message,
            }
            for result in results
        ],
        "assertions": [],
        "artifacts": artifacts,
        "started_at": started,
        "finished_at": finished,
    }
