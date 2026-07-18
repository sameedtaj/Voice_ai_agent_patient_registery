from typing import Any

from pydantic import BaseModel, Field


class VapiToolCall(BaseModel):
    id: str
    name: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class VapiMessage(BaseModel):
    type: str
    call: dict[str, Any] = Field(default_factory=dict)
    toolCallList: list[VapiToolCall] = Field(default_factory=list)
    artifact: dict[str, Any] = Field(default_factory=dict)


class VapiWebhook(BaseModel):
    message: VapiMessage
