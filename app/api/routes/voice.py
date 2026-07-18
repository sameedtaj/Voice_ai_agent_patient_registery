import json
import logging
import secrets
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request

from app.api.dependencies import DbSession
from app.core.config import settings
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voice", tags=["Voice"])
logger = logging.getLogger(__name__)


def verify_vapi(authorization: str | None, x_vapi_secret: str | None) -> None:
    expected = settings.vapi_webhook_secret
    if not expected:
        return
    bearer = authorization.removeprefix("Bearer ").strip() if authorization else None
    supplied = bearer or x_vapi_secret
    if not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Invalid webhook credentials")


def extract_tool_calls(message: dict[str, Any]) -> list[dict[str, Any]]:
    calls = message.get("toolCallList") or []
    if calls:
        return calls
    extracted = []
    for item in message.get("toolWithToolCallList") or []:
        call = item.get("toolCall", {})
        extracted.append(
            {"id": call.get("id"), "name": item.get("name"), "parameters": call.get("parameters", {})}
        )
    return extracted


async def process_webhook(request: Request, db: DbSession, authorization: str | None, x_vapi_secret: str | None):
    verify_vapi(authorization, x_vapi_secret)
    body = await request.json()
    message = body.get("message", {})
    message_type = message.get("type")
    call = message.get("call") or {}
    call_id = call.get("id")

    if message_type == "tool-calls":
        results = []
        service = VoiceService(db)
        for tool_call in extract_tool_calls(message):
            name = tool_call.get("name", "")
            tool_call_id = tool_call.get("id", "")
            try:
                output = service.run_tool(name, tool_call.get("parameters") or {}, call_id)
            except Exception as exc:
                logger.exception("voice_tool_failed name=%s call_id=%s", name, call_id)
                output = {"success": False, "message": "The request could not be completed. Please try again."}
            results.append(
                {"name": name, "toolCallId": tool_call_id, "result": json.dumps(output, default=str)}
            )
        return {"results": results}

    if message_type == "end-of-call-report":
        artifact = message.get("artifact") or {}
        service = VoiceService(db)
        service.save_call_summary(
            {
                "call_id": call_id,
                "caller_phone": (message.get("customer") or call.get("customer") or {}).get("number"),
                "status": "ended",
                "transcript": artifact.get("transcript") or message.get("transcript"),
                "collected_payload": message.get("analysis") or artifact.get("messages"),
            },
            call_id,
        )
    return {"received": True}


@router.post("/tools")
async def voice_tools(
    request: Request,
    db: DbSession,
    authorization: str | None = Header(default=None),
    x_vapi_secret: str | None = Header(default=None),
):
    return await process_webhook(request, db, authorization, x_vapi_secret)


@router.post("/webhook")
async def voice_webhook(
    request: Request,
    db: DbSession,
    authorization: str | None = Header(default=None),
    x_vapi_secret: str | None = Header(default=None),
):
    return await process_webhook(request, db, authorization, x_vapi_secret)
