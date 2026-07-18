from typing import Any

from sqlalchemy.orm import Session

from app.services.voice_service import VoiceService


def handle_tool(db: Session, name: str, parameters: dict[str, Any], call_id: str | None = None) -> dict:
    return VoiceService(db).run_tool(name, dict(parameters), call_id)
